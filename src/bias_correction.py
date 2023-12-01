from __future__ import print_function

from pathlib import Path
from multiprocessing import Pool, cpu_count
from nipype.interfaces.ants.segmentation import N4BiasFieldCorrection


def create_dir(path):
    path_obj = Path(path)
    if not path_obj.is_dir():
        path_obj.mkdir(parents=True, exist_ok=True)
    return


def unwarp_bias_field_correction(arg, **kwarg):
    return bias_field_correction(*arg, **kwarg)


def bias_field_correction(src_path, dst_path):
    print("N4ITK on: ", src_path)
    try:
        n4 = N4BiasFieldCorrection()
        n4.inputs.input_image = str(src_path)
        n4.inputs.output_image = str(dst_path)

        n4.inputs.dimension = 3
        n4.inputs.n_iterations = [100, 100, 60, 40]
        n4.inputs.shrink_factor = 3
        n4.inputs.convergence_threshold = 1e-4
        n4.inputs.bspline_fitting_distance = 300
        n4.run()
    except RuntimeError:
        print("\tFailed on: ", src_path)

    return


parent_dir = Path.cwd().parent
data_dir = Path('/scratch/kmouheb/p1_data')
data_src_dir = data_dir / "ADNIBrain"
data_dst_dir = data_dir / "ADNIDenoise"
create_dir(data_dst_dir)

data_src_paths, data_dst_paths = [], []
for subject in data_src_dir.iterdir():
    data_src_paths.append(subject)
    dst_label_dir = Path(str(subject).replace('ADNIBrain', 'ADNIDenoise'))
    data_dst_paths.append(dst_label_dir)

# Test
bias_field_correction(data_src_paths[0], data_dst_paths[0])

# Multi-processing
# paras = zip(data_src_paths, data_dst_paths)
# pool = Pool(processes=cpu_count())
# pool.map(unwarp_bias_field_correction, paras)
