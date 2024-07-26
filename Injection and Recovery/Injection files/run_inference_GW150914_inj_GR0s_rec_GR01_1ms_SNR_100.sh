#!/bin/sh

NPROCS=30
WORK_DIR=/mnt/NAS/SMALL_THEORY/francesco.crescimbeni/src/Ringdown/Golden_Simulations

OMP_NUM_THREADS=1 \
pycbc_inference --verbose \
    --use-mpi \
    --seed 257 \
    --config-file ${WORK_DIR}/inference_config_GW150914_inj_GR0s_rec_GR01_1ms_SNR_100.ini \
    --output-file ${WORK_DIR}/samples_GW150914_inj_GR0s_rec_GR01_1ms_SNR_100.hdf \
    --nprocesses ${NPROCS} \
    --force