#!/bin/bash

# Take input
duration=$input_duration
echo Input configuration: duration="$duration" seconds

number_of_parallel_procs=$(cat /proc/cpuinfo | awk "/^processor/{print $3}" | wc -l)

# Execute
echo Stressing CPU with "$number_of_parallel_procs" processes for "$duration" seconds

# Run md5sum calculation $number_of_parallel_procs times. Each md5sum calculation runs parallelized in its own process (P0)
seq $number_of_parallel_procs | xargs -P0 -n1 timeout $duration md5sum /dev/zero