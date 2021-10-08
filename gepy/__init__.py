class parallel_command:

    def __init__(self, binary='/usr/bin/hostname', args=[]):
        self.binary = binary
        self.args = args

    def expand(self):
        text = '# GEPY Parallel command.\n'
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
        text = '# GEPY serial command.\n'
        text = text + self.binary
        for a in self.args:
            text = text + ' ' + args
        text = text + '\n'
        return text

class user_script:

    def __init__(self, script=''):
        self.script = script   

    def expand(self):
        text = '# User supplied shell code.\n'
        text = text + self.script + '\n'
        text = text + '# End user supplied shell code.\n'
        return text

class job:

    def __init__(self, name='gepy_job', memory=1024, length=60, location='.'):
        self.name = name
        self.memory = memory
        self.length = length
        self.location = location
        self.modules = []
        self.workload = []

    def get_job_script(self):
        import math
        script = '#!/bin/bash -l\n'
        script = script + '#$ -N ' + self.name + '\n'
        script = script + '#$ -l mem=' + str(self.memory) + 'M\n'
        hrs = math.floor(self.length/60)
        mins = self.length%60
        script = script + '#$ -l h_rt=' + str(hrs) + ':' + str(mins) + ':00 \n'

        if (self.location == '.'):
            script = script + '#$ -cwd\n'
        else:
            script = script + '#$ -wd ' + self.location + '\n'

        for a in self.modules:
            script = script + 'module load ' + a + '\n'

        for a in self.workload:
            script = script + a.expand() + '\n'

        return script

        

