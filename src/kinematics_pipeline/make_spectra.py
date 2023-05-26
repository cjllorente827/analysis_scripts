import trident
from analysis_scripts import *

from ndustria import AddTask

@AddTask()
def make_spectra(ds, index, line, line_list = ['H', 'C', 'N', 'O', 'Mg']):

    ray_file = f"{getOutputDir()}/{str(ds)}_ray_{index}.h5"
    output_file = f'{getOutputDir()}/spec_raw_{index}.txt'
    plot_file = f"{getTempDir()}/{str(ds)}_spectra_{index}.png"

    ray = trident.make_simple_ray(ds,
        line[0],
        line[1],
        fields=["radial_velocity"],
        data_filename=ray_file,
        lines=line_list)

    sg = trident.SpectrumGenerator('COS-G130M')
    sg.make_spectrum(ray, lines=line_list)

    sg.add_qso_spectrum()
    #sg.add_gaussian_noise(30)

    sg.save_spectrum(output_file)
    sg.plot_spectrum(plot_file)

    return [ray_file, output_file]