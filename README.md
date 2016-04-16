# lonestar5_launch

interface to the parametric launcher on TACC/lonestar5

Running `launch` creates a `job` that executes a bunch of `tasks` listed in a `parallel script` in parallel using some number of available `cores` on some requested `nodes`. (see *definitions*)

## load module

      module use /corral-repl/utexas/poldracklab/users/wtriplet/external/ls5_launch
      module load poldracklaunch

## definitions
* _parallel script_: the text file that contains a list of commands (see: _tasks_) to execute in parallel. File should contain only commands and their arguments, without empty lines, comments, or anything else but commands. No interpretation is done on this parallel script, so any shell variables (i.e. `$SCRATCH` or `$WORK`) should be replaced by their values before going into the parallel script.
* _task_: a command being executed. basically a single line in the _parallel_script_.
* _job_: the execution of all of the _tasks_ in the _parallel_script_. 
* _node_: a host upon which commands are launched in parallel. Hostnames look like `nidXXXXX` where `XXXXX` is numeric identifier. A node has 64 GB of memory, 24 physical cores (48 logical cores with hyperthreading), and no hard disk or swap. Per-user `$SCRATCH`, `$HOME`, and `$WORK` folders are available, and `corral-repl` is also mounted.
* _core_: a CPU (need to get the specs here i guess)
* ???

## usage
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

## usage notes

1. Lonestar 5's smallest allocation unit is a node (w/ 64 GB ram, 24 physical cores, 48 logical cores, no swap). So using `-N 1 -n 1` is functionally the same as `-N 1 -n 24`.
2. `launch` doesn't free allocated any nodes until the last task finishes. If the runtimes for each task are likely to vary significantly in a predictable way, it may be worth breaking them up into separate `launch` jobs.
3. If the parallel script contains a few number of tasks than there are cores, and you request a single node, you may see error messages that look like `grep: invalid max count`. This is due to an issue in the underlying parametric launcher system and (from what I can tell) is a cosmetic issue and is not causing the tasks or job to fail.
4. `launch` assumes that the tasks are not threaded, and that they will use 1 core each. If any of the tasks run threaded, there's nothing stopping them from trainwrecking the core usage. Maybe the commands (tasks) provide a way to specify the number of threads to use, and that would help manage the resources a bit better.

## notes on defaults

if `-N` is not provided, and `-n` is, the number of nodes will be computed such that all tasks will run simultaenously. Likewise, if `-n` is not provided and `-N` is, the maximum number of cores available will be requested. This is currently 24 or with `--ht` it will be 48.

If more cores per node are requested than available, the program will print an error message and stop; however is more nodes are requested than allowed, the program will reduce the requested number of nodes to the max allowed. 


