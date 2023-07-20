#!/bin/bash

# vectorSparse
# cxx: 7.5.0
# apps: util/job_launching/apps/define-all-apps.yml
# traces: hw_run/traces/device-0/11.0/spmm_benchmark/
# cfg: gpu-simulator/gpgpu-sim/configs/tested-cfgs/SM75_RTX2080_Ti/gpgpusim.config
make vectorSparse -C ./gpu-app-collection/src
# every time execute run_hw_trace, you must bash && conda activate accel-sim && source ./gpu-app-collection/src/setup_environment
export LD_LIBRARY_PATH=/home/yangjianchao/Github/sputnik/build/sputnik/:$LD_LIBRARY_PATH
./util/tracer_nvbit/run_hw_trace.py -B vectorSparse -D 0
# every time execute run_simulations, you must source ./gpu-simulator/setup_environment.sh
./util/job_launching/run_simulations.py -B vectorSparse -C RTX2080Ti-SASS -T ./hw_run/traces/device-0/11.0/ -N myTest-202307102012
./util/job_launching/monitor_func_test.py -v -N myTest-202307102012
./util/job_launching/run_simulations.py -B vectorSparse -C RTX2080Ti-PTX -T ./hw_run/traces/device-0/11.0/ -N myTest-202307102018
./util/job_launching/monitor_func_test.py -v -N myTest-202307102018

# cutlass-bench
# cxx: 7.5.0
# apps: util/job_launching/apps/define-all-apps.yml
# traces: hw_run/traces/device-0/11.0/spmm_benchmark/
# cfg: gpu-simulator/gpgpu-sim/configs/tested-cfgs/SM75_RTX2080_Ti/gpgpusim.config
make cutlass -C ./gpu-app-collection/src
# every time execute run_hw_trace, you must bash && conda activate accel-sim && source ./gpu-app-collection/src/setup_environment
./util/tracer_nvbit/run_hw_trace.py -B cutlass_5_trace -D 0
# every time execute run_simulations, you must source ./gpu-simulator/setup_environment.sh
./util/job_launching/run_simulations.py -B cutlass_5_trace -C RTX2080Ti-SASS -T ./hw_run/traces/device-0/11.0/ -N myTest-202307102012
./util/job_launching/monitor_func_test.py -v -N myTest-202307102012
./util/job_launching/run_simulations.py -B cutlass_5_trace -C RTX2080Ti-PTX -T ./hw_run/traces/device-0/11.0/ -N myTest-202307102018
./util/job_launching/monitor_func_test.py -v -N myTest-202307102018





git add .vscode/settings.json
git commit -m "Delete settings.json"
git add get-accel-sim-traces.py
git commit -m "Update get-accel-sim-traces.py"
git add gpu-simulator/format-code.sh
git commit -m "Update format-code.sh"
git add gpu-simulator/setup_environment.sh
git commit -m "Update setup_environment.sh"
git add run.sh
git commit -m "Update run.sh"
git add travis.sh
git commit -m "Update travis.sh"
git add util/accelwattch/accelwattch_hw_profiler/collate_power.sh
git commit -m "Update collate_power.sh"
git add util/accelwattch/accelwattch_hw_profiler/gen_hw_perf_csv.py
git commit -m "Update gen_hw_perf_csv.py"
git add util/accelwattch/accelwattch_hw_profiler/gen_hw_power_csv.py
git commit -m "Update gen_hw_power_csv.py"
git add util/accelwattch/accelwattch_hw_profiler/profile_ubench_power.sh
git commit -m "Update profile_ubench_power.sh"
git add util/accelwattch/accelwattch_hw_profiler/profile_validation_perf.sh
git commit -m "Update profile_validation_perf.sh"
git add util/accelwattch/accelwattch_hw_profiler/profile_validation_power.sh
git commit -m "Update profile_validation_power.sh"
git add util/accelwattch/check_job_status.sh
git commit -m "Update check_job_status.sh"
git add util/accelwattch/check_job_status_all.sh
git commit -m "Update check_job_status_all.sh"
git add util/accelwattch/collect_power_reports.sh
git commit -m "Update collect_power_reports.sh"
git add util/accelwattch/collect_power_reports_all.sh
git commit -m "Update collect_power_reports_all.sh"
git add util/accelwattch/gen_sim_power_csv.py
git commit -m "Update gen_sim_power_csv.py"
git add util/accelwattch/launch_jobs.sh
git commit -m "Update launch_jobs.sh"
git add util/accelwattch/launch_jobs_all.sh
git commit -m "Update launch_jobs_all.sh"
git add util/hw_stats/clean_hw_data.sh
git commit -m "Update clean_hw_data.sh"
git add util/hw_stats/get_hw_data.sh
git commit -m "Update get_hw_data.sh"
git add util/hw_stats/get_posted_hw_stats.py
git commit -m "Update get_posted_hw_stats.py"
git add util/hw_stats/run_hw.py
git commit -m "Update run_hw.py"
git add util/hw_stats/to-install.sh
git commit -m "Update to-install.sh"
git add util/job_launching/apps/define-all-apps.yml
git commit -m "Update define-all-apps.yml"
git add util/job_launching/get_stats.py
git commit -m "Update get_stats.py"
git add util/plotting/correlate_and_publish.sh
git commit -m "Update correlate_and_publish.sh"
git add util/plotting/merge-stats.py
git commit -m "Update merge-stats.py"
git add util/plotting/plot-correlation.py
git commit -m "Update plot-correlation.py"
git add util/plotting/plot-get-stats.py
git commit -m "Update plot-get-stats.py"
git add util/plotting/plot-public.sh
git commit -m "Update plot-public.sh"
git add util/tracer_nvbit/generate-turing-traces.sh
git commit -m "Update generate-turing-traces.sh"
git add util/tracer_nvbit/generate-volta-traces.sh
git commit -m "Update generate-volta-traces.sh"
git add util/tracer_nvbit/install_nvbit.sh
git commit -m "Update install_nvbit.sh"
git add util/tracer_nvbit/run_hw_trace.py
git commit -m "Update run_hw_trace.py"
git add util/tracer_nvbit/tracer_tool/format-code.sh
git commit -m "Update format-code.sh"
git add util/tracer_nvbit/tracer_tool/traces-processing/Makefile
git commit -m "Update Makefile"
git add util/tuner/GPU_Microbenchmark/Makefile
git commit -m "Update Makefile"
git add util/tuner/GPU_Microbenchmark/format-code.sh
git commit -m "Update format-code.sh"
git add util/tuner/GPU_Microbenchmark/output.file
git commit -m "Delete output.file"
git add util/tuner/GPU_Microbenchmark/run_all.sh
git commit -m "Update run_all.sh"
git add util/tuner/tuner.py
git commit -m "Update tuner.py"