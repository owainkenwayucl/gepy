import gepy

def lammps_job(inputfile=None, logfile='log.lammps', cores=1, name='gepy_lammps_job', memory='4G', length=120, location='.', platform='basic', smt=False, gpus=None):
    r = gepy.job(self, name=name, memory=memory, length=length, location=location)
    r.make_parallel(mode='mpi', slots=cores)
    r.enable_blank_env()
    r.modules.append('gcc-libs/4.9.2')
    r.modules.append('compilers/intel/2018')
    r.modules.append('mpi/intel/2018')
    r.modules.append('lammps/7Aug19/'+ platform +'/intel-2018')
    if not gpus==None:
        r.add_resource('gpu', str(gpus))

    if smt:
        r.enable_smt()
        r.workload.append(gepy.serial_command(binary='export', args=['OMP_NUM_THREADS=2']))

    if platform=='basic':
        run_args=[]
    elif platform=='userintel':
        run_args=['-sf', 'intel']
    elif platform=='gpu':
        if gpus==None:
            raise ValueError('Asked for GPU LAMMPS but did not ask for GPUs.')
        else:
            run_args=['-sf', '-gpu', '-pk', 'gpu', str(gpus)]
    else:
        raise ValueError('Invalid LAMMPS build type:' + platform)

    run_args.append('-in', inputfile, '-log', logfile)

    r.workload.append(gepy.parallel_command(binary='lmp_default', args=run_args))

    return r