from konlpy.tag import Kkom # 형태소 분석기
from konlpy.tag import twiter

import numpy as np #키워드 분석을 위한 그래프 생성 패키지

# Scikit-learn 머신러링 이용을 위한 import
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize

class SentenceTokenizer(object):
    def __init__(self):
        self.kkma = Kkma()
        self.twitter = Twitter()
        self.stopwords = ['중인' ,'만큼', '마찬가지', '꼬집었', "연합뉴스", "데일리", "동아일보", "중앙일보", "조선일보", "기자","아", "휴", "아이구", "아이쿠", "아이고", "어", "나", "우리", "저희", "따라", "의해", "을", "를", "에", "의", "가",]

    def text2sentences(self, text):
        sentences = self.kkma.sentences(text)      
            for idx in range(0, len(sentences)):
                if len(sentences[idx]) <= 10:
                    sentences[idx-1] += (' ' + sentences[idx])
                    sentences[idx] = ''
        
        return sentences

def get_nouns(self, sentences):
    nouns = []
    for sentence in sentences:
        if sentence is not '':
            nouns.append(' '.join([noun for noun in self.twitter.nouns(str(sentence)) 
                                   if noun not in self.stopwords and len(noun) > 1]))
        
    return nouns


# 전치 행렬을 만들어서 adj(A)의 값을 구해 taxt rank 구현
class GraphMatrix(object):
    def __init__(self):
        self.tfidf = TfidfVectorizer()
        self.cnt_vec = CountVectorizer()
        self.graph_sentence = []
        
    def build_sent_graph(self, sentence):
        tfidf_mat = self.tfidf.fit_transform(sentence).toarray()
        self.graph_sentence = np.dot(tfidf_mat, tfidf_mat.T)
        return  self.graph_sentence
        
    def build_words_graph(self, sentence):
        cnt_vec_mat = normalize(self.cnt_vec.fit_transform(sentence).toarray().astype(float), axis=0)
        vocab = self.cnt_vec.vocabulary_
        return np.dot(cnt_vec_mat.T, cnt_vec_mat), {vocab[word] : word for word in vocab}

class Rank(object):
  def get_ranks(self, graph, d=0.85): # d = damping factor
    A = graph
    matrix_size = A.shape[0]
    for id in range(matrix_size):
      A[id, id] = 0 # diagonal 부분을 0으로 
      link_sum = np.sum(A[:,id]) # A[:, id] = A[:][id]
      if link_sum != 0:
        A[:, id] /= link_sum
      A[:, id] *= -d
      A[id, id] = 1
            
      B = (1-d) * np.ones((matrix_size, 1))
      ranks = np.linalg.solve(A, B) # 연립방정식 Ax = b
    return {idx: r[0] for idx, r in enumerate(ranks)}
