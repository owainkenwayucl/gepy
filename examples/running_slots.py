#!/usr/bin/env python3

import gepy.executor as ge

jobs = ge.qstat_joblist(filter='*')
total_running_slots = 0
total_running_tasks = 0
total_jobs = len(jobs)
for a in jobs:
    if 'r' in a.stateblock:
        total_running_slots = total_running_slots + a.slots
        total_running_tasks = total_running_tasks + 1

print(str(total_running_slots) + ' slots worth of running tasks.')
print(str(total_running_tasks) + ' running tasks.')
print(str(total_jobs) + ' jobs in queue.')
