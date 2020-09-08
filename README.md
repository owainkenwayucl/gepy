# gepy

This module is me looking at ways to talk to the Grid Engine Scheduler with Python.  It's basically a sketch of how things might work at this point and you probably shouldn't touch it.

The idea is that some future service will present JupyterHub/Lab as a front end to HPC at UCL and some future well designed version of this thing should allow users to do job control through Python, with something like:

```python
import gepy.job

my_job = job(name='My Job', length='120')
my_job.make_parallel(job.mpi, 1024)
my_job.modules.add('lammps')
my_job.add_parallel_command('lmp_default -in myfile.in')
my_job.submit()
```

Hopefully there'd also be tools for inspecting the status of the user's jobs and retrieving the output etc.