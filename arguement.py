import argparse
from config import ArgStyle, ArgSpliter


ArgumentDict = {}

def parse_args():
    global Argument_Dict
    parser = argparse.ArgumentParser()
    
    parser.add_argument(ArgStyle.NAME,
                           default = ArgStyle.Default,
                           type = str,
                           help = "the style to be attacked")
    
    parser.add_argument(ArgSpliter.NAME,
                           default = ArgSpliter.Default,
                           type = str,
                           help = "segmentation")
    

    args = parser.parse_args()
    for key in list(args.__dict__.keys()):
        ArgumentDict[key] = args.__dict__[key]
    return args



    
    

