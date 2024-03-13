import argparse
from config import KEY


Argument_Dict = {}

def parse_arguments():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--style",
                           default = KEY.Shopping,
                           type = str,
                           help = "the style to be attacked")
    
    parser.add_argument("--split",
                           default = "ltp",
                           type = str,
                           help = "segmentation")
    
    # parser.add_argument("--masked",
    #                        default = KEY.Bert,
    #                        type = str,
    #                        help = "mask language model")
    
    
    args = parser.parse_args()

    global Argument_Dict
    for key in list(args.__dict__.keys()):
        Argument_Dict[key] = args.__dict__[key]
        
    return args



    
    

