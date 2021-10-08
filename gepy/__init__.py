class job:

    def __init__(self, name='gepy_job', memory=1024, length=60, location='.'):
        self.name = name
        self.memory = memory
        self.length = length
        self.location = location
        self.modules = []
        self.script = ''

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

        script = script + self.script + '\n'

        return script

        

