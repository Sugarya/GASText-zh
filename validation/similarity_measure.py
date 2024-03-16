
from sentence_transformers import SentenceTransformer, util
from config import Pattern
from common import tools
from typing import List

'''
    用于测量句子的相似性
'''
class SimMeasurer:

    def __init__(self):
        self.__sim_model = SentenceTransformer(Pattern.SentenceSimilarityModel)
        

    '''
        获得余弦相似计算下的相似值
    '''
    def compute_cos_similarity(self, sentence1:str, sentence2:str) -> float:
        if not sentence1 and not sentence2:
            return None
        
        embedding1 = self.__sim_model.encode(sentence1, convert_to_tensor=True)
        embedding2 = self.__sim_model.encode(sentence2, convert_to_tensor=True)
        cosine_score = util.cos_sim(embedding1, embedding2).cpu().numpy()
        tools.show_log(f'cosine score = {cosine_score[0][0]}')
        return cosine_score[0][0]
    
    
    def compute_all_cos_similarity(self, sentence_list1:List[str], sentence_list2:List[str]):
        embedding_list1 = self.__sim_model.encode(sentence_list1, convert_to_tensor=True)
        embedding_list2 = self.__sim_model.encode(sentence_list2, convert_to_tensor=True)
        cosine_scores = util.cos_sim(embedding_list1, embedding_list2)
        return cosine_scores
        # pairs = []
        # for i in range(cosine_scores.shape[0]):
        #     for j in range(cosine_scores.shape[1]):
        #         pairs.append({"index": [i, j], "score": cosine_scores[i][j]})
        
        # pairs = sorted(pairs, key=lambda x: x["score"], reverse=True)

        # return pairs[0]["index"]