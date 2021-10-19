import gepy
import gepy.executor

js = gepy.executor.qstat_joblist('*')

for a in js:
    print(a.status, a.jid, a.prio, a.name, a.owner, a.stateblock, a.timeblock, a.slots, a.taskinfo)
