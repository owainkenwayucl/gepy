#/usr/bin/env python3

# This script does a test of a particular nvidia compiler on Myriad

import sys
import os
import time
import gepy
import gepy.executor

compiler_module = 'compilers/nvhpc/21.11'
repo = 'https://github.com/UCL-RITS/pi_examples.git'

if (len(sys.argv) > 1):
    compiler_module = sys.argv[1]

print('Generating job scripts for compiler module: ' + compiler_module)

template_job = gepy.job(name='nvtest')
template_job.modules.append('personal-modules')
template_job.modules.append('testing-modules')
template_job.modules.append(compiler_module)
template_job.add_resource('gpu','1')

tmp_dir = 'nvtest_'+str(time.time())
os.mkdir(tmp_dir)

template_job.location=os.getcwd() + '/' + tmp_dir

status = executor.run('git clone ' + repo + ' ' + tmp_dir + '/pi_examples')

if (status.returncode != 0):
    sys.exit('Error cloning repo: ' + status.stderr)

template_job.workload.append(gepy.serial_command('cd ', ['pi_examples']))

# Right, that's the repo cloned and a template job created.

doconc_job = copy.deepcopy(template_job)
cudaf_job = copy.deepcopy(template_job)
openmp_job = copy.deepcopy(template_job)
openacc_job = copy.deepcopy(template_job)

# do concurrent test

doconc_job.workload.append(gepy.serial_command('cd ', ['fortran_do_concurrent_pi_dir']))
doconc_job.workload.append(gepy.serial_command('make ', ['clean']))
doconc_job.workload.append(gepy.serial_command('make ', ['nvhpc']))
doconc_job.workload.append(gepy.serial_command('./pi', []))
doconc_job.name = template_job.name + 'doconc'

# cuda fortran test

cudaf_job.workload.append(gepy.serial_command('cd ', ['cudafortran_pi_dir']))
cudaf_job.workload.append(gepy.serial_command('make ', ['clean']))
cudaf_job.workload.append(gepy.serial_command('make ', []))
cudaf_job.workload.append(gepy.serial_command('./pi', []))
cudaf_job.name = template_job.name + 'cudaf'

# openmp fortran test

openmp_job.workload.append(gepy.serial_command('cd ', ['fortran_omp_pi_dir']))
openmp_job.workload.append(gepy.serial_command('make ', ['clean']))
openmp_job.workload.append(gepy.serial_command('make ', ['nvhpc_offload']))
openmp_job.workload.append(gepy.serial_command('./pi_gpu', []))
openmp_job.name = template_job.name + 'openmp'

# openacc fortran test

openacc_job.workload.append(gepy.serial_command('cd ', ['fortran_openacc_pi_dir']))
openacc_job.workload.append(gepy.serial_command('make ', ['clean']))
openacc_job.workload.append(gepy.serial_command('make ', ['-f' 'Makefile.myriad', 'pi']))
openacc_job.workload.append(gepy.serial_command('./pi', []))
openacc_job.name = template_job.name + 'openacc'

print('Submitting jobs')

j,t = gepy.executor.qsub(doconc_job.get_job_script())
j,t = gepy.executor.qsub(cudaf.get_job_script())
j,t = gepy.executor.qsub(openmp_job.get_job_script())
j,t = gepy.executor.qsub(openacc_job.get_job_script())

print('Done')