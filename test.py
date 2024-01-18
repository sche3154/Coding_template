import torch
import numpy as np
import random

from options.test_options import TestOptions
from data import create_dataset
from models import create_model

torch.manual_seed(1)
np.random.seed(1)
random.seed(1)
torch.cuda.manual_seed_all(1)
torch.cuda.manual_seed(1)
torch.backends.cudnn.benchmark = True
torch.backends.cudnn.deterministic = True

if __name__ == '__main__':
    torch.cuda.empty_cache()
    opt = TestOptions().parse()  # get test options
    dataset = create_dataset(opt)  # create a dataset given opt.dataset_mode and other options
    dataset_size = len(dataset)    # get the number of images in the dataset.
    print('The number of testing images = %d' % dataset_size)

    model = create_model(opt)      # create a model given opt.model and other options
    model.setup(opt)               # regular setup: load and print networks; create schedulers
    model.eval()

    processing = dataset.dataset.processing
    io = dataset.dataset.io

    for i, data in enumerate(dataset):

        start_time = time.time()

        if i >= opt.num_test:  # only apply our model to opt.num_test images.
            break

        if opt.input_patch_size > 0: # now can handle patches
            pred_list = []
            patch_nums = len(data[next(iter(data))])

            for j in range(0, patch_nums, self.opt.input_batch_sizes):
                data_patched = {}
                for key, value in data.items()
                    value = value.squeeze(0)
                    data_patched[key] = value[j:min(j+self.opt.input_batch_sizes, patch_nums),...]

                model.set_input(data_patched)
                output = model.test()  # run inference
                output = output.detach().cpu().numpy()
                # b c w h d -> b w h d c
                output = np.transpose(output, (0, 2, 3, 4, 1))
                pred_list.append(output)
                preds = np.concatenate(pred_list, axis=0)
                resulted_img = dataset.dataset.postprocessing(preds)
        else:
            model.set_input(data)
            output = model.test()  # run inference
            output = output.detach().cpu().numpy()
            # b c w h d -> b w h d c
            resulted_img = np.transpose(output, (0, 2, 3, 4, 1))

        if (i+1) % opt.save_prediction == 0:
            dataset.dataset.save_sample(resulted_img, suffix = opt.save_suffix)

    print('End inference')