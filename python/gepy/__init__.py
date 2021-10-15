class parallel_command:

    def __init__(self, binary='/usr/bin/hostname', args=[]):
        self.binary = binary
        self.args = args

    def expand(self):
        text = '\n# GEPY Parallel command.\n'
        text = text + 'gerun' + ' ' + self.binary
        for a in self.args:
            text = text + ' ' + a
        text = text + '\n'
        return text

class serial_command:

    def __init__(self, binary='/usr/bin/hostname', args=[]):
        self.binary = binary
        self.args = args

    def expand(self):
        text = '\n# GEPY serial command.\n'
        text = text + self.binary
        for a in self.args:
            text = text + ' ' + args
        text = text + '\n'
        return text

class user_script:

    def __init__(self, script=''):
        self.script = script   

    def expand(self):
        text = '\n# User supplied shell code.\n'
        text = text + self.script + '\n'
        text = text + '# End user supplied shell code.\n'
        return text

class job:

    def __init__(self, name='gepy_job', memory=1024, length=60, location='.'):
        import math
        self.name = name
        self.resources = {}
        self.add_resource('mem',memory)
        hrs = str(math.floor(length/60))
        mins = str(length%60)
        if len(mins) == 1:
            mins = '0' + mins
        self.add_resource('h_rt',hrs + ':' + mins + ':00')
        self.location = location
        self.modules = []
        self.workload = []
        self.parallel = False
        self.slots = 1
        self.parallel_mode = ''

    def make_parallel(self, mode='smp', slots=1):
        if (not self.parallel):
            self.parallel = True
            self.slots = slots
            self.parallel_mode = mode
        else:
            if (self.parallel_mode == mode):
                self.slots = slots
            else:
                # The goal here is to provent someone trying to do a hybrid run by making SMP then MPI or vice versa.
                raise ValueError('Cannot change parallel mode from ' + self.parallel_mode + ' to ' + mode + '.')

    def make_serial(self):
        self.parallel = False
        self.parallel_mode = ''
        self.slots = 1

    def add_resource(self,name,value):
        self.resources[name] = str(value)

    def get_job_script(self):
        import math
        script = '#!/bin/bash -l\n'
        script = script + '# Job script generated by GEPY (https://github.com/owainkenwayucl/gepy)\n'
        script = script + '#$ -N ' + self.name + '\n'

        if (self.parallel):
            script = script + '#$ -pe ' + str(self.parallel_mode) + ' ' + str(self.slots) + '\n'

        for a in self.resources.keys():
            script = script + '#$ -l ' + str(a) + '=' + str(self.resources[a]) + '\n'

        if (self.location == '.'):
            script = script + '#$ -cwd\n'
        else:
            script = script + '#$ -wd ' + self.location + '\n'

        for a in self.modules:
            script = script + 'module load ' + a + '\n'

        for a in self.workload:
            script = script + a.expand() + '\n'

        return script

        

