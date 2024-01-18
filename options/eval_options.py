import argparse

class EvalOptions():

    def __init__():
        parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        parser.add_argument('--results_dir', type=str , required=True, help='path to results)')
        parser.add_argument('--name', type=str , required=True, help='exp name')
        parser.add_argument('--metrics', type=str, nargs='+', required=True, help='mse, mae, ccr')

        return parser

    
