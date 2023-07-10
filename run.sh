#!/bin/bash

# vectorSparse
# cxx: 7.5.0
# apps: util/job_launching/apps/define-all-apps.yml
# traces: hw_run/traces/device-0/11.0/spmm_benchmark/
# cfg: gpu-simulator/gpgpu-sim/configs/tested-cfgs/SM75_RTX2080_Ti/gpgpusim.config
make vectorSparse -C ./gpu-app-collection/src
./util/tracer_nvbit/run_hw_trace.py -B vectorSparse -D 0
./util/job_launching/run_simulations.py -B vectorSparse -C RTX2080Ti-SASS -T ./hw_run/traces/device-0/11.0/ -N myTest-202307102012
./util/job_launching/monitor_func_test.py -v -N myTest-202307102012
./util/job_launching/run_simulations.py -B vectorSparse -C RTX2080Ti-PTX -T ./hw_run/traces/device-0/11.0/ -N myTest-202307102018
./util/job_launching/monitor_func_test.py -v -N myTest-202307102018


