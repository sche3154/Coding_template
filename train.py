from options.train_options import TrainOptions
from data import create_dataset
from models import create_model
from utils.recorder import Recorder

import torch
import numpy as np
import random
import time

torch.manual_seed(1)
np.random.seed(1)
random.seed(1)
torch.cuda.manual_seed_all(1)
torch.cuda.manual_seed(1)
torch.backends.cudnn.benchmark = True
torch.backends.cudnn.deterministic = True

if __name__ == '__main__':         # SIngle sample cropped, no pre-loaded batches

    torch.cuda.empty_cache()
    opt = TrainOptions().parse()   # get training options
    dataset = create_dataset(opt)  # create a dataset given opt.dataset_mode and other options

    dataset_size = len(dataset)    # get the number of images in the dataset.
    print('The number of training images = %d' % dataset_size)

    model = create_model(opt)      # create a model given opt.model and other options
    model.setup(opt)               # regular setup: load and print networks; create schedulers

    for epoch in range(opt.epoch_count, opt.n_epochs + opt.n_epochs_decay + 1):

        epoch_loss = {}
        epoch_start_time = time.time()  # timer for entire epoch

        # training
        counter = 0
        for i, data in enumerate(dataset):

            if opt.input_patch_size > 0: # now can handle patches
                data_patched = {}
                patch_nums = len(data[next(iter(data))])
                for j in range(0, patch_nums, self.opt.input_batch_sizes):
                    data_patched = {}
                    for key, value in data.items()
                        value = value.squeeze(0)
                        data_patched[key] = value[j:min(j+self.opt.input_batch_sizes, patch_nums),...]

                    model.set_input(data_patched)
                    model.optimize_parameters()
                    losses = model.get_current_losses()

                    for k, v in losses.items():
                        epoch_loss[k] += v if epoch_loss[k] is not None else epoch_loss[k] = v

                    counter +=1
            else:
                model.set_input(data)
                model.optimize_parameters()
                losses = model.get_current_losses()

                for k, v in losses.items():
                    epoch_loss[k] += v if epoch_loss[k] is not None else epoch_loss[k] = v

                counter +=1
     
        recorder.print_epoch_losses(epoch, epoch_loss/counter, time.time() - epoch_start_time)
        print('End of epoch %d / %d \t Time Taken: %d sec' % (epoch, opt.n_epochs + opt.n_epochs_decay, time.time() - epoch_start_time))

        if epoch % opt.save_epoch_freq == 0:  # cache our model every <save_epoch_freq> epochs
            print('saving the model at the end of epoch %d, iters %d' % (epoch, total_iters))
            model.save_networks('latest')
            model.save_networks(epoch)
    
    print('End of training')
    recorder.close()