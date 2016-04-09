# lonestar5_launch
udpates to parametric launcher on TACC/lonestar5

# behavior
```
usage: launch [-h] [-s SCRIPT_NAME] [-r RUNTIME] [-j JOBNAME] [-A PROJNAME]
              [-d DIRECTORY] [-q QUEUE] [-m EMAIL] [-f QSUBFILE] [-w WAITPROC]
              [--ht] [-k] [-u] [-t] [-i HOLD] [-N NODES]
              [-n MAX_CORES_PER_NODE]

process SLURM job.

optional arguments:
  -h, --help            show this help message and exit
  -s SCRIPT_NAME, --script SCRIPT_NAME
                        name of parallel script to run
  -r RUNTIME, --runtime RUNTIME
                        maximum runtime for job
  -j JOBNAME, --jobname JOBNAME
                        job name
  -A PROJNAME, --projname PROJNAME
                        name of project
  -d DIRECTORY, --cwd DIRECTORY
                        name of working directory
  -q QUEUE, --queue QUEUE
                        name of queue
  -m EMAIL, --email EMAIL
                        email address for notification
  -f QSUBFILE, --qsubfile QSUBFILE
                        name of qsub file
  -w WAITPROC, --waitproc WAITPROC
                        process to wait for
  --ht                  use hyperthreading (new default: FALSE, old default: TRUE)
  -k, --keepqsubfile    keep qsub file
  -u, --ignoreuser      ignore ~/.launch_user
  -t, --test            do not actually launch job
  -i HOLD, --hold_jid HOLD
                        wait for this job id to complete before launching
  -N NODES, --nodes NODES
                        request that a minimum number of nodes be allocated to
                        this job
  -n MAX_CORES_PER_NODE, --max-cores-per-node MAX_CORES_PER_NODE
                        request that a maximum number of cores be used per
                        node (for memorys sake) [ NEW ]
```

# defaults

if `-N` is not provided, and `-n` is, the number of nodes will be computed such that all jobs will run simultaenously. Likewise, if `-n` is not provided and `-N` is, the maximum number of cores available will be requested. This is currently 24 or with `--ht` it will be 48.

If more cores per node are requested than available, the program will print an error message and stop; however is more nodes are requested than allowed, the program will reduce the requested number of nodes to the max allowed. 

