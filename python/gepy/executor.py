def run(command):
    import subprocess
    return subprocess.run(command, capture_output=True, encoding='UTF-8')
    
def qstat_joblist(filter=None):
    import xml.etree.ElementTree as xml
    import gepy
    
    qstat_command = ['/opt/sge/bin/lx-amd64/qstat', '-xml']
    if (filter != None):
        qstat_command.append('-u')
        qstat_command.append(filter)

    job_text = run(qstat_command).stdout

    tree = xml.fromstring(job_text)

    jobs = []

    for child in tree:
        for subchild in child:
            status = subchild.attrib['state']
            jid = subchild.find('JB_job_number').text
            prio = subchild.find('JAT_prio').text
            name = subchild.find('JB_name').text
            owner = subchild.find('JB_owner').text
            stateblock = subchild.find('state').text
            if (status == 'pending'):
                timeblock = subchild.find('JB_submission_time').text
            else:
                timeblock = subchild.find('JAT_start_time').text
            slots = subchild.find('slots').text
            try:
                taskinfo = subchild.find('tasks').text
            except AttributeError as err:
                taskinfo = None
            temp_job = gepy.queue_job(status, jid, prio, name, owner, stateblock, timeblock, slots, taskinfo)
            jobs.append(temp_job)

    return jobs

# This is a horrible kludge because qstat -j is horrid
def qstat_job(job_id):
    jobs = []
    temp_jobs = qstat_joblist(filter="*")

    job_id = str(job_id).split('.')[0] # remove task info

    for a in temp_jobs:
        if str(a.jid) == str(job_id):
            jobs.append(a)

    return jobs

# Shockingly, qsub does not have xml output.
def qsub(jobscript, depend=None):
    import tempfile
    import os

    temp_script, path = tempfile.mkstemp(prefix='gepy_script', text=True, suffix='.sh')
    with open(temp_script, 'w') as ts:
        ts.write(jobscript)

    command = ['qsub']
    if depend != None:
        command.append('-hold_jid')
        command.append(str(depend))

    command.append(path)

    status = run(command)

    if (status.returncode == 0):
        job_id = status.stdout.split()[2]
        os.remove(path)
        split_id = job_id.split('.')

        # Return job_id, task info
        if len(split_id) == 1:
            return job_id,'' # maybe we should return a job object?
        else:
            return split_id[0],split_id[1]
    else:
        raise ValueError(status.stderr)

def qdel(job_id):
    status = run(['qdel', str(job_id)])

    return status.returncode