# gepy

This module is me looking at ways to talk to the Grid Engine Scheduler with Python.  It's basically a sketch of how things might work at this point and you probably shouldn't touch it.

The idea is that some future service will present JupyterHub/Lab as a front end to HPC at UCL and some future well designed version of this thing should allow users to do job control through Python, with something like:

```python
>>> import gepy.job
>>> my_job = job(name='My Job', length='120')
>>> my_job.make_parallel(job.mpi, 160)
>>> my_job.modules.add('lammps')
>>> my_job.add_parallel_command('lmp_default -in myfile.in')
>>> print(myjob.get_job_script)
#!/bin/bash
#$ -N MyJob
#$ -l mem=1024M
#$ -l h_rt=2:0:0
#$ -cwd
#$ -pe mpi 160

module load lammps
gerun lmp_default -in myfile.in
>>> my_job.submit()
>>> my_job.id
123242
>>> print(my_job.status())
Queue Waiting
>>> 
```

Hopefully there'd also be tools for inspecting the status of the user's jobs and retrieving the output etc.

## MSc Project

In the summer of 2021, Bowen Zheng, a CDT MSc student completed an MSc project, supervised by me, exploring this idea.  You can see his code and efforts here: https://github.com/SC2020-zbw/MSc_project