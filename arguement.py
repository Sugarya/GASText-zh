import argparse
from config import ArgStyle, ArgAlgorithm, ArgLabel, ArgAblation, ArgSubstituteSize, ArgPostfix, ArgSpaceSize, ArgSpaceStyle, ArgFragileType, ArgSubstituteType, ArgMaskedSimThreshold, ArgHownetSimThreshold


ArgumentDict = {}

def parse_args():
    global Argument_Dict
    parser = argparse.ArgumentParser()

    # 必须参数
    parser.add_argument(ArgStyle.NAME,
                           default = ArgStyle.Default,
                           type = str,
                           help = "the style to be attacked")
    parser.add_argument(ArgAlgorithm.NAME,
                           default = ArgAlgorithm.Default,
                           type = str,
                           help = "attack algorithm")
    
    # ----------可选参数-----------
    parser.add_argument(ArgLabel.NAME,
                           default = ArgLabel.Default,
                           type = int,
                           help = "target label")
    
    parser.add_argument(ArgAblation.NAME,
                           default = ArgAblation.Default,
                           type = int,
                           help = "ablation type")
    
    parser.add_argument(ArgPostfix.NAME,
                           default = ArgPostfix.Default,
                           type = str,
                           help = "the postfix of dataset file")
    
    parser.add_argument(ArgSubstituteSize.NAME,
                           default = ArgSubstituteSize.Default,
                           type = int,
                           help = "the size of substitute set")
    
    parser.add_argument(ArgSubstituteType.NAME,
                           default = ArgSubstituteType.Default,
                           type = str,
                           help = "the type of substitute set")
    
    parser.add_argument(ArgSpaceSize.NAME,
                           default = ArgSpaceSize.Default,
                           type = int,
                           help = "the size of space columns")
    
    parser.add_argument(ArgSpaceStyle.NAME,
                           default = ArgSpaceStyle.Default,
                           type = str,
                           help = "the style of space")
    
    parser.add_argument(ArgFragileType.NAME,
                           default = ArgFragileType.Default,
                           type = str,
                           help = "the type of fragile computing")   

    parser.add_argument(ArgHownetSimThreshold.NAME,
                           default = ArgHownetSimThreshold.Default,
                           type = int,
                           help = "the threshold of hownet word similary")
    
    parser.add_argument(ArgMaskedSimThreshold.NAME,
                           default = ArgMaskedSimThreshold.Default,
                           type = int,
                           help = "the threshold of word similary in masked language model")


    args = parser.parse_args()
    for key in list(args.__dict__.keys()):
        ArgumentDict[key] = args.__dict__[key]
    return args



    
    

