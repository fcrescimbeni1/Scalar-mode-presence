#!/usr/bin/bash

#source PATH_TO_VIRTUALENV/bin/activate

pycbc_create_injections --verbose \
                        --config-file GW150914_inject_GR0s_1ms_SNR_100.ini \
                        --ninjections 1 \
                        --seed 10 \
                        --output-file GW150914_inject_GR0s_1ms_SNR_100.hdf \
                        --variable-params-section variable_params \
                        --static-params-section static_params \
                        --dist-section prior \
                        --force
