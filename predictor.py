import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmwrite, mmread
import pickle
from gensim.models import Word2Vec
from api.models.book import Book


class Predictor:
    def __init__(self):
        self.Tfidf_matrix = mmread("./data/tfidf_book_summary.mtx").tocsr()
        with open("./data/tfidf.pickle", "rb") as f:
            self.Tfidf = pickle.load(f)
        self.embedding_model = Word2Vec.load("./data/word2VecModel.model")
        self.df = pd.DataFrame.from_records(list(Book.objects.all().values()))

    def getRecommendation(self, keyword):
        summary = [keyword] * 10
        if keyword in self.embedding_model.wv.key_to_index:
            sim_word = self.embedding_model.wv.most_similar(keyword, topn=10)
            labels = []
            for label, _ in sim_word:
                labels.append(label)
            # 가장 유사한 단어를 많이 저장
            for i, word in enumerate(labels):
                summary += [word] * (9 - i)
        # 유사한 단어를 조합한 문장
        summary = " ".join(summary)
        print(summary)
        summary_vec = self.Tfidf.transform([summary])
        cosine_sim = linear_kernel(summary_vec, self.Tfidf_matrix)

        simScore = list(
            enumerate(cosine_sim[-1])
        )  # book_idx와 전체 martix의 cosine 유사도에 해당하는 값과 index list로 반환
        simScore = sorted(simScore, key=lambda x: x[1], reverse=True)  # 유사도의 내림차순으로 정렬
        simScore = simScore[1:11]  # 가장 유사한 상위 10개 책
        bookidx = [i[0] for i in simScore]  # 10개 책의 index
        print(bookidx)
        recBookList = self.df.loc[bookidx, "title"]
        print(recBookList)
        return recBookList
