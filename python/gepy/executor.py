def run(command):
    import subprocess
    return subprocess.run(command, capture_output=True, encoding='UTF-8')
    
def qstat_joblist(filter='*'):
    import xml.etree.ElementTree as xml
    import gepy
    
    job_text = run(['/opt/sge/bin/lx-amd64/qstat', '-xml','-u', filter]).stdout

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