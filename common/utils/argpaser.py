import argparse


Argument_Dict = {}

def parse_arguments():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--dataset",
                           default="shopping",
                           type=str,
                           help="the dataset to be attacked")
    
    parser.add_argument("--victim",
                           default="bert-base-uncased-ag",
                           type=str,
                           help="the victim to be attacked")
    
    parser.add_argument("--encoder_decoder",
                           default="bert-base",
                           type=str,
                           help="the fill mask model")
    

    
    args = parser.parse_args()

    global Argument_Dict
    for key in list(args.__dict__.keys()):
        Argument_Dict[key] = args.__dict__[key]
        
    return args



    
    

