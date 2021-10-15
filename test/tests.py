import gepy
test_job = gepy.job(name="test")
test_job.workload.append(gepy.serial_command())
test_job.workload.append(gepy.user_script('echo HELLO'))
test_job.workload.append(gepy.parallel_command(binary='lmp_any', args=['-in', 'in.lammps']))
test_job.modules.append('lammps')
test_job.make_parallel(mode='mpi', slots='12')
print(test_job.get_job_script())
test_job.make_parallel(mode='mpi', slots=13)
print(test_job.get_job_script())
test_job.make_serial()
print(test_job.get_job_script())
test_job.make_parallel(mode='smp', slots='12')
print(test_job.get_job_script())
try:
    test_job.make_parallel(mode='mpi', slots='12')
except ValueError as err:
    print('Expected ValueError chainging parallel mode :)')

