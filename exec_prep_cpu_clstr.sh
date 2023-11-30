
module load python/3.9.5
module load cmake/3.3.1
module load ANTs
module load fsl/6.0.4

export FSLDIR=/cm/shared/apps/fsl/6.0.4
export FSLOUTPUTTYPE=NIFTI_GZ

echo $PATH
echo $FSLDIR
echo $FSLOUTPUTTYPE


source /home/kmouheb/envs/venv_prep/bin/activate 
pip install tqdm numpy scipy niptype nibabel matplotlib sciKit-fuzzy scikit-learn


python /home/kmouheb/repos/brain-mri-preprocessing/src/registration.py



