from __future__ import print_function

import os
import subprocess
from pathlib import Path
from multiprocessing import Pool, cpu_count


def create_dir(path):
    path_obj = Path(path)
    if not path_obj.is_dir():
        path_obj.mkdir(parents=True, exist_ok=True)
    return


def bet(src_path, dst_path, frac="0.5"):
    command = ["bet", src_path, dst_path, "-R", "-f", frac, "-g", "0"]
    subprocess.call(command)
    return


def unwarp_strip_skull(arg, **kwarg):
    return strip_skull(*arg, **kwarg)


def strip_skull(src_path, dst_path, frac="0.4"):
    print("Working on :", src_path)
    try:
        bet(src_path, dst_path, frac)
    except RuntimeError:
        print("\tFailed on: ", src_path)

    return

parent_dir = Path.cwd().parent
data_dir = Path('/scratch/kmouheb/p1_data')
data_src_dir = data_dir / "ADNIReg"
data_dst_dir = data_dir / "ADNIBrain"

create_dir(data_dst_dir)


data_src_paths, data_dst_paths = [], []
for subject in data_src_dir.iterdir():
    data_src_paths.append(subject)
    dst_label_dir = Path(str(subject).replace('ADNIReg', 'ADNIBrain'))
    data_dst_paths.append(dst_label_dir)

# Test
strip_skull(data_src_paths[0], data_dst_paths[0])

# Multi-processing
# paras = zip(data_src_paths, data_dst_paths)
# pool = Pool(processes=cpu_count())
# pool.map(unwarp_strip_skull, paras)
