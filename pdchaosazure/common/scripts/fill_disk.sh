#!/bin/bash

echo Input configuration: duration="$input_duration" seconds, size="$input_size" megabytes, path="$input_path"
echo Filling disk with "$input_size" megabytes of random data for "$input_duration" seconds.

# 'nohup' stands for "no hangup" allows the process to continue running even if a user has logged off (or "hung up")
# 'dd' is convert and copy file command - see the manpage to see how it works: https://linux.die.net/man/1/dd
nohup dd if=/dev/urandom of=$input_path bs=1M count=$input_size iflag=fullblock
sleep $input_duration

echo Cleaning up file at "$input_path" ...
rm "$input_path"
echo Cleaned up.