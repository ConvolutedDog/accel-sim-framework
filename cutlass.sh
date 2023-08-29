# cutlass
./util/job_launching/run_simulations.py -B cutlass_wmma_64x64x64 -C RTX2080Ti-VISUAL -T ./hw_run/traces/device-0/11.0/ -N myTest-cutlass_wmma_64x64x64
./util/job_launching/run_simulations.py -B cutlass_wmma_128x128x128 -C RTX2080Ti-VISUAL -T ./hw_run/traces/device-0/11.0/ -N myTest-cutlass_wmma_128x128x128
./util/job_launching/run_simulations.py -B cutlass_wmma_256x256x256 -C RTX2080Ti-VISUAL -T ./hw_run/traces/device-0/11.0/ -N myTest-cutlass_wmma_256x256x256
./util/job_launching/run_simulations.py -B cutlass_wmma_512x512x512 -C RTX2080Ti-VISUAL -T ./hw_run/traces/device-0/11.0/ -N myTest-cutlass_wmma_512x512x512
./util/job_launching/run_simulations.py -B cutlass_wmma_1024x1024x1024 -C RTX2080Ti-VISUAL -T ./hw_run/traces/device-0/11.0/ -N myTest-cutlass_wmma_1024x1024x1024
./util/job_launching/run_simulations.py -B cutlass_sgemm_64x64x64 -C RTX2080Ti-VISUAL -T ./hw_run/traces/device-0/11.0/ -N myTest-cutlass_sgemm_64x64x64
./util/job_launching/run_simulations.py -B cutlass_sgemm_128x128x128 -C RTX2080Ti-VISUAL -T ./hw_run/traces/device-0/11.0/ -N myTest-cutlass_sgemm_128x128x128
./util/job_launching/run_simulations.py -B cutlass_sgemm_256x256x256 -C RTX2080Ti-VISUAL -T ./hw_run/traces/device-0/11.0/ -N myTest-cutlass_sgemm_256x256x256
./util/job_launching/run_simulations.py -B cutlass_sgemm_512x512x512 -C RTX2080Ti-VISUAL -T ./hw_run/traces/device-0/11.0/ -N myTest-cutlass_sgemm_512x512x512
./util/job_launching/run_simulations.py -B cutlass_sgemm_1024x1024x1024 -C RTX2080Ti-VISUAL -T ./hw_run/traces/device-0/11.0/ -N myTest-cutlass_sgemm_1024x1024x1024

# vectorSparse
./util/job_launching/run_simulations.py -B vectorSparse -C RTX2080Ti-VISUAL -T ./hw_run/traces/device-0/11.0/ -N myTest-vectorSparse
