from abc import ABC, abstractmethod

class BaseEvaluation(ABC):

    def __init__(self, opt):
        self.opt = opt

    @abstractmethod
    def evaluation(self):
        pass

    @abstractmethod
    def save_evaluation(self):
        pass

