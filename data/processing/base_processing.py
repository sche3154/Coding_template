from abc import ABC, abstractmethod
import numpy as np

class BaseProcessing(ABC):

    def __init__(self, opt):
        """Initialize the class; save the options in the class

        Parameters:
            opt (Option class)-- stores all the experiment flags; needs to be a subclass of BaseOptions
        """
        self.opt = opt
        self.isTrain = opt.isTrain

    #---------------------------------------------#
    #               preproessing                  #
    #---------------------------------------------#
    @abstractmethod
    def preprocessing(self, sample):

        pass

    #---------------------------------------------#
    #               postproessing                  #
    #---------------------------------------------#
    @abstractmethod
    def postprocessing(self, sample):

        pass

    def get_norm(self)

        norm = getattr(self, self.opt + '_norm')

        return norm

    def instance_norm(self, image, mask):
        # image: (W,H,D,C)
        # computes mean, std along the spatial dimensions for each channel and each sample
        means  = np.mean(image[mask==1], axis = (0)) # (c, )
        stds = np.std(image[mask==1], axis = (0))  # (c,)

        image[mask==1] = (image[mask == 1] - means)/stds  
        image[mask != 1] = 0

        return image, means, stds

    def find_bounding_box(self, mask):
        x, y, z = mask.shape[0], mask.shape[1], mask.shape[2]
        for i in range(z):
            slice = mask[:,:,i]
            if np.sum(slice) > 0:
                save_z_from_I = i
                break

        for i in reversed(range(z)):
            slice = mask[:,:,i]
            if np.sum(slice) > 0:
                save_z_from_S = i
                break

        for i in range(y):
            slice = mask[:, i, :]
            if np.sum(slice) > 0:
                save_y_from_P = i
                break

        for i in reversed(range(y)):
            slice = mask[:, i, :]
            if np.sum(slice) > 0:
                save_y_from_A = i
                break

        for i in range(x):
            slice = mask[i,:,:]
            if np.sum(slice) > 0:
                save_x_from_L = i
                break

        for i in reversed(range(x)):
            slice = mask[i,:,:]
            if np.sum(slice) > 0:
                save_x_from_R = i
                break

        return save_x_from_L, save_x_from_R, save_y_from_P, save_y_from_A, save_z_from_I, save_z_from_S

    def patch_generations(self, image):
        



