import importlib

def find_io_using_name(io_name):
    """
    Import the module "io/[io_name]_io.py".
    """
    io_filename = "io." + io_name + "_io"
    iolib = importlib.import_module(io_filename)
    io = None
    target_io_name = io_name.replace('_', '') + 'io'
    for name, cls in iolib.__dict__.items():
        if name.lower() == target_io_name.lower():
            io = cls

    if io is None:
        print("In %s.py, there should be a dataio with class name that matches %s in lowercase." % (io_filename, target_io_name))
        exit(0)

    return loader

def create_io(io_name, opt):
    """
    Create a io class based on the flags given in the options
    """

    io_class = find_io_using_name(io_name)
    io = io_class(opt)

    return io

# def find_sample_using_name(sample_name):
#     """
#     Import the module "io/[sample_name]_sample.py".
#     """
#     sample_filename = "sample." + sample_name + "_sample"
#     samplelib = importlib.import_module(sample_filename)
#     sample = None
#     target_sample_name = sample_name.replace('_', '') + 'sample'
#     for name, cls in samplelib.__dict__.items():
#         if name.lower() == target_sample_name.lower():
#             sample = cls

#     if sample is None:
#         print("In %s.py, there should be a dataio with class name that matches %s in lowercase." % (sample_filename, target_sample_name))
#         exit(0)

# def create_sample(sample_name, opt):
#     """
#     Create a sample class based on the flags given in the options
#     """

#     sample_class = find_sample_using_name(sample_name)
#     sample = sample_class(opt)

#     return io




