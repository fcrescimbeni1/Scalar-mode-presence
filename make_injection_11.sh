#!/usr/bin/bash

#source PATH_TO_VIRTUALENV/bin/activate

pycbc_create_injections --verbose \
                        --config-files injection_10.ini \
                        --ninjections 1 \
                        --seed 10 \
                        --output-file injection_11.hdf \
                        --variable-params-section variable_params \
                        --static-params-section static_params \
                        --dist-section prior \
                        --force
