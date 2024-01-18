from abc import ABC, abstractmethod

class BaseSample(ABC):

    def __init__(self, opt):
        """Initialize the class; save the options in the class

        Parameters:
            opt (Option class)-- stores all the experiment flags; needs to be a subclass of BaseOptions
        """

        self.opt = opt
        self.root = opt.root
        self.isTrain = opt.isTrain