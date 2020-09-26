#!/bin/bash

echo Adding a network discipline that delays traffic at "${input_delay}"+-"${input_jitter}"ms on interface "$input_network_interface" for "$input_duration" seconds.
sudo tc qdisc add dev "$input_network_interface" root netem delay "${input_delay}"ms "${input_jitter}"ms
sleep "$input_duration"

echo Removing network discipline ...
sudo tc qdisc del dev "$input_network_interface" root
echo Removed network discipline.