import os
import nibabel as nib
import pickle
from utils.mrtrix import *

def load_data(path, needs_affine = False):

    if not os.path.exists(path):
        raise ValueError(
            "Data could not be found \"{}\"".format(path)
        )
        exit(0)

    if path.endswith('.mif.gz') or path.endswith('.mif'):
        vol = load_mrtrix(path)
        data_copied = vol.data.copy()
        affine_copied = vol.transform.copy()
    elif path.endswith('.nii.gz') or path.endswith('.nii'):
        vol = nib.load(path)
        data_copied = vol.get_fdata().copy()
        affine_copied = vol.affine.copy()
    else:
        raise IOError('file extension not supported: ' + str(path))
        exit(0)

    # Return volume
    if needs_affine:
        return data_copied, affine_copied
    else:
        return data_copied
    
def save_data(data, affine, output_name):
    nifti = nib.Nifti1Image(data, affine=affine)
    nib.save(nifti, output_name)
    print('Save image to the path {:}'.format(output_name))

def get_HCPsamples(hcp_split_path, train =True):
    if not os.path.exists(hcp_split_path):
        raise IOError(
            "hcp splited list path, {}, could not be resolved".format(hcp_split_path)
        )
        exit(0)

    with open(hcp_split_path, 'rb') as handle:
        sub_list = pickle.load(handle)
        
        if train:
            sample_list = sub_list['train']
        else:
            sample_list = sub_list['test']
            
    return sample_list