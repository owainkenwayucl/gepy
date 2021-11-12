#!/usr/bin/env python3

import gepy.executor as ge

jobs = ge.qstat_joblist(filter='*')
total_running_jobs = 0
for a in jobs:
    if 'r' in a.stateblock:
        total_running_jobs = total_running_jobs + a.slots

print(str(total_running_jobs) + ' slots worth of running jobs.')