from utils.mrtrix import *
from utils.downsampling import *
import os
import nibabel as nib
import numpy as np

def load_data(path, index = None, needs_affine = False):

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
        data_copied = vol.get_fdata(dtype = np.float32).copy()
        ## debug
        # print(data_copied.dtype)
        affine_copied = vol.affine.copy()
    else:
        raise IOError('file extension not supported: ' + str(path))
        exit(0)

    # Return volume
    if needs_affine:
        return data_copied, affine_copied
    else:
        return data_copied

def load_downsampled_mif_dwi(path, index = None, grad_dirs = 6, needs_affine = False, random = True):

    if not os.path.exists(path):
        raise ValueError(
            "Data could not be found \"{}\"".format(path)
        )
        exit(0)

    if path.endswith('.mif.gz') or path.endswith('.mif'):
        mif = load_mrtrix(path)
        affine_copied = mif.transform.copy()
        old_grad = mif.grad
        bvals = old_grad[:, -1]
        bvecs = old_grad[:, :-1]

        if random:
            print('Random downsampling {:}'.format(index))
        else:
            print('Downsampling {:}'.format(index))

        lr_bvecs, lr_bvals, lr_index, b0_index = extract_single_shell(
                bvals, bvecs, directions = grad_dirs, extract_bval = np.max(bvals), sample=random
        )
        
        lr_index = np.array(lr_index.tolist())

        mif_b0 = np.mean(mif.data[..., b0_index], axis=-1, keepdims=True)
        downsampled_data_copied = np.concatenate([mif_b0, mif.data[..., lr_index]], axis=-1).copy()

        if needs_affine:
            return downsampled_data_copied, lr_bvecs.copy(), lr_bvals.copy(), affine_copied
        else:
            return downsampled_data_copied, lr_bvecs.copy(), lr_bvals.copy()

    else:
        raise IOError('file extension is not supported for downsampling must mif: ' + str(path))
        exit(0)

def save_data(self, data, affine, output_name):
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

def get_PPMIsamples(ppmi_split_path, train=True):
    if not os.path.exists(ppmi_split_path):
        raise IOError(
            "PPMI splited list path, {}, could not be resolved".format(ppmi_split_path)
        )
        exit(0)
    
    with open(ppmi_split_path, 'rb') as handle:
        sub_list = pickle.load(handle)

        sample_list = []
        if train:
            sample_list.extend(sub_list['CONTROL_train'])
            sample_list.extend(sub_list['PD_train'])
            sample_list.remove('40541')
        else:
            sample_list.extend(sub_list['CONTROL_test'])
            sample_list.extend(sub_list['PD_test'])

    return sample_list