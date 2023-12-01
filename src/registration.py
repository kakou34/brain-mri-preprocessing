import os
from pathlib import Path
import subprocess
from multiprocessing import Pool, cpu_count


def registration(src_path, dst_path, ref_path):
    command = ["flirt", "-in", src_path, "-ref", ref_path, "-out", dst_path,
               "-bins", "256", "-cost", "corratio", "-searchrx", "0", "0",
               "-searchry", "0", "0", "-searchrz", "0", "0", "-dof", "12",
               "-interp", "spline"]
    subprocess.call(command, stdout=open(os.devnull, "r"),
                    stderr=subprocess.STDOUT)
    return


def orient2std(src_path, dst_path):
    command = ["fslreorient2std", src_path, dst_path]
    subprocess.call(command)
    return

def create_dir(path):
    path_obj = Path(path)
    if not path_obj.is_dir():
        path_obj.mkdir(parents=True, exist_ok=True)
    return


def unwarp_main(arg, **kwarg):
    return main(*arg, **kwarg)


def main(src_path, dst_path, ref_path):
    print("Registration on: ", src_path)
    try:
        orient2std(src_path, dst_path)
        registration(dst_path, dst_path, ref_path)
    except RuntimeError:
        print("\tFalied on: ", src_path)

    return


parent_dir = Path.cwd().parent
data_dir = Path('/scratch/kmouheb/p1_data')
data_src_dir = data_dir / "ADNI_comp"
data_dst_dir = data_dir / "ADNIReg"

create_dir(data_dst_dir)

ref_path = Path('/cm/shared/apps/fsl/6.0.4/data/standard/MNI152_T1_1mm.nii.gz')
# ref_path = os.path.join(data_dir, "Template", "MNI152_T1_1mm_brain.nii.gz")

data_src_paths, data_dst_paths = [], []

for subject in data_src_dir.iterdir():
    data_src_paths.append(subject)
    dst_label_dir = Path(str(subject).replace('ADNI_comp', 'ADNIReg'))
    data_dst_paths.append(dst_label_dir)

# Test
main(data_src_paths[0], data_dst_paths[0], ref_path)

# Multi-processing
# paras = zip(data_src_paths, data_dst_paths,
#             [ref_path] * len(data_src_paths))
# pool = Pool(processes=cpu_count())
# pool.map(unwarp_main, paras)
