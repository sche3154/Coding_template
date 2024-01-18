import importlib

def find_eval_using_name(eval_name):
    """
    Import the module "eval/[eval_name]_eval.py".
    """
    eval_filename = "eval." + eval_name + "_eval"
    evallib = importlib.import_module(eval_filename)
    eval = None
    target_eval_name = eval_name.replace('_', '') + 'eval'
    for name, cls in evallib.__dict__.items():
        if name.lower() == target_eval_name.lower():
            eval = cls

    if eval is None:
        print("In %s.py, there should be a eval with class name that matches %s in lowercase." % (eval_filename, target_eval_name))
        exit(0)

    return loader

def create_eval(eval_name, opt):
    """
    Create a eval class based on the flags given in the optevalns
    """

    eval_class = find_eval_using_name(eval_name)
    eval = eval_class(opt)

    return eval