import subprocess
import configparser
import read_ini_file as r

# Leggi il file .ini e ottieni il dizionario risultante
file_path = 'injection_11.ini'
params = r.read_ini_file(file_path)

print(params)

# Costruisci il comando completo
command = f"""
    pycbc_inference_plot_posterior --verbose \
    --input-file samples_11.hdf \
    --output-file corner_11_s.png \
    --plot-density --plot-contours --plot-marginal \
    --density-cmap inferno \
    --parameters \
        'final_spin:$\chi_f$' \
        'final_mass:$M_f (M_\odot)$' \
        'phi220:$\phi_{{220}}$' \
        'amp220:$A_{{220}}$' \
        'phi221:$\phi_{{221}}$' \
        'amp221:$A_{{221}}$' \
    --expected-parameters \
        final_spin:{params["static_params"]["final_spin"]} \
        final_mass:{params["static_params"]["final_mass"]} \
        phi220:{params["static_params"]["phi220"]} \
        amp220:{params["static_params"]["amp220"]} \
        phi221:{params["static_params"]["phi221"]} \
        amp221:{params["static_params"]["amp221"]} \
    --expected-parameters-color ORANGE
"""

# Esegui il comando
subprocess.run(command, shell=True)

