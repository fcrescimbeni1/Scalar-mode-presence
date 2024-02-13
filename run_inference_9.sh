#!/bin/sh

NPROCS=40
WORK_DIR=/mnt/NAS/SMALL_THEORY/francesco.crescimbeni/src/Ringdown/Injection_Tests_II

OMP_NUM_THREADS=12 \
pycbc_inference --verbose \
    --use-mpi \
    --seed 257 \
    --config-file ${WORK_DIR}/inference_config_9.ini \
    --output-file ${WORK_DIR}/samples_9.hdf \
    --nprocesses ${NPROCS} \
    --force