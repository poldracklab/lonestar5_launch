#!/usr/bin/env python

# launch script for stampede
# deals with both command files for parametric launcher and with single commands

import argparse
import sys,os
from tempfile import *
import subprocess
import math

MAXCORES=4104
MAXNODES=171

# set up argument args

def launch_slurm_ls5 (serialcmd='', script_name='', runtime='01:00:00',
    jobname='launch', projname='', queue='normal', email=False, qsubfile='',
    keepqsubfile=False, ignoreuser=False, test=False, parser=[], c=[], max_cores_per_node=None,
    verbose=0, hold=[], outfile=[], cwd=[], nodes=0, use_hyperthreading=True):

    if use_hyperthreading:
        ncores_per_node = 48
    else:
        ncores_per_node = 24

    if max_cores_per_node is None:
        max_cores_per_node = ncores_per_node
    elif int(max_cores_per_node) > ncores_per_node:
        print("Requested max cores per node (%s) exceeds available cores per node (%d)." \
            % (max_cores_per_node, ncores_per_node))
        if use_hyperthreading is False:
            print("Enabling hyperthreading (--ht) would double the available cores per node.")
        sys.exit()

    max_cores_per_node = int(max_cores_per_node)

    if len(serialcmd) > 0:
        print('sorry, serial mode is not currently supported')
        sys.exit(1)
        #parametric = 0
        #print('Running serial command: '+cmd)
        #nnodes = 1
        #parenv = '1way'
        #queue = 'serial'
    elif script_name:
        parametric = 1
        print('Submitting parametric job file: ' + script_name)
        try:
            f = open(script_name,'r')
        except:
            print('%s does not exist -e!' % script_name)
            sys.exit(0)
        script_cmds = f.readlines()
        f.close()
        ncmds = len(script_cmds)
        print('found %d commands' % ncmds)
        # need to check for empty lines
        for s in script_cmds:
            if s.strip() == '':
                print('command file contains empty lines - please remove them first')
                sys.exit()
        if not nodes:
            nodes = math.ceil(float(ncmds)/float(max_cores_per_node))
            print('Number of compute nodes not specified - estimating as %d' % nodes)
    
        if int(nodes) > MAXNODES:
            print('Warning # of nodes exceeds max allowed (%d), reducing requested nodes to %d.' \
                    % (nodes, MAXNODES))
            nodes=MAXNODES

    else:
        print('ERROR: you must either specify a script name (using -s) or a command to run\n\n')
        sys.exit()
    
    if not qsubfile:
        qsubfile,qsubfilepath = mkstemp(prefix=jobname+"_",dir='.',suffix='.slurm',text=True)
        os.close(qsubfile)

    total_cores = max_cores_per_node*int(nodes)

    print('Outputting qsub commands to %s' % qsubfilepath)
    qsubfile = open(qsubfilepath,'w')
    qsubfile.write('#!/bin/bash\n#\n')
    qsubfile.write('# SLURM control file automatically created by launch\n')
    if parametric == 1:
        qsubfile.write('#SBATCH -N %d\n'%int(nodes))
    else:
        print('sorry - serial mode is not currently supported')
        sys.exit(1)
        #qsubfile.write('# Launching single command: %s\n#\n#\n'%cmd)
        
    qsubfile.write('#SBATCH -J %s       # Job Name\n'%jobname)
    qsubfile.write('#SBATCH -o {0}.o%j # Name of the output file (eg. myMPI.oJobID)\n'.format(jobname))
    qsubfile.write('#SBATCH -p %s\n' % queue)
    qsubfile.write('#SBATCH -t %s\n' % runtime)
    qsubfile.write('#SBATCH -n %d\n' % total_cores) #ncmds)

    if type(hold) is str: 
        qsubfile.write("#SBATCH -d afterok")
        qsubfile.write(":{0}".format(int(hold)))
        qsubfile.write('\n')

    if projname != "":
        qsubfile.write("#SBATCH -A {0}\n".format(projname))

    try:
        waitfor
    except:
        waitfor = None
    if waitfor:
        qsubfile.write('#SBATCH -d %d\n' % waitfor)

    
    qsubfile.write('#----------------\n# Job Submission\n#----------------\n')
    #qsubfile.write('umask 2\n\n')
    
    if not parametric:
        # currently not supported...
        qsubfile.write('\n\nset -x                   # Echo commands, use "set echo" with csh\n')
        qsubfile.write(cmd+'\n')
    
    else:
        #qsubfile.write('module load launcher\n')
    
        qsubfile.write('export LAUNCHER_PLUGIN_DIR=$LAUNCHER_DIR/plugins\n')
        qsubfile.write('export LAUNCHER_RMI=SLURM\n')
        qsubfile.write('export LAUNCHER_JOB_FILE=%s\n'%script_name)
    
        #qsubfile.write('cd $WORKDIR\n')
        #qsubfile.write('echo " WORKING DIR:   $WORKDIR/"\n')
        qsubfile.write('$LAUNCHER_DIR/paramrun\n')
    
        qsubfile.write('echo " "\necho " Parameteric Job Complete"\necho " "\n')
        
    qsubfile.close()
    
    jobid = None
    if not test:
        process = subprocess.Popen('sbatch %s' % qsubfilepath, shell=True, stdout=subprocess.PIPE)
        for line in process.stdout:
            print(line.strip())
            
            if line.find('Submitted batch job') == 0:
                jobid=int(line.strip().split(' ')[3])
        process.wait()
    
    if not keepqsubfile:
        print('Deleting qsubfile: %s'%qsubfilepath)
        os.remove(qsubfilepath)
    return jobid

