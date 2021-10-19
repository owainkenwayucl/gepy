import gepy
import gepy.executor

import xml.etree.ElementTree as ET


jobs=gepy.executor.run(['/opt/sge/bin/lx-amd64/qstat', '-xml','-u', '*']).stdout
root = ET.fromstring(jobs)

js = gepy.executor.qstat_joblist()

for a in js:
    print(a.status, a.jid, a.prio, a.name, a.owner, a.stateblock, a.timeblock, a.slots, a.taskinfo)
