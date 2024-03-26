import argparse
from config import ArgStyle, ArgAlgorithm, ArgLabel, ArgAblation


ArgumentDict = {}

def parse_args():
    global Argument_Dict
    parser = argparse.ArgumentParser()
    
    parser.add_argument(ArgStyle.NAME,
                           default = ArgStyle.Default,
                           type = str,
                           help = "the style to be attacked")
    
    parser.add_argument(ArgAlgorithm.NAME,
                           default = ArgAlgorithm.Default,
                           type = str,
                           help = "attack algorithm")
    
    parser.add_argument(ArgLabel.NAME,
                           default = ArgLabel.Default,
                           type = int,
                           help = "target label")
    
    parser.add_argument(ArgAblation.NAME,
                           default = ArgAblation.Default,
                           type = int,
                           help = "ablation type")

    args = parser.parse_args()
    for key in list(args.__dict__.keys()):
        ArgumentDict[key] = args.__dict__[key]
    return args



    
    

