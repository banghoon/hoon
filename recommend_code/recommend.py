from sklearn.metrics.pairwise import cosine_similarity, pairwise_distances
from sklearn.metrics import jaccard_score
import pandas as pd
import numpy as np
import tool


def similarity_matrix(a, b=None, method='cosine'):
    sim = None
    if method.lower() == 'cosine':
        if b is None:
            sim = cosine_similarity(a.values, a.values)
        else:
            sim = cosine_similarity(a.values, b.values)
    elif method.lower() == 'jaccard':
        if b is None:
            sim = 1 - pairwise_distances(a.T, metric="hamming")
    return pd.DataFrame(data=sim, columns=a.index.values, index=a.index)


def rating(rating_df, sim_df, user, rating_col='rating', user_col='userId', item_col='movieId'):
    user_sim = sim_df.loc[rating_df[rating_df[user_col] == user][item_col]]
    user_rating = rating_df[rating_df[user_col] == user][rating_col]
    sim_sum = user_sim.sum(axis=0)
    predict_ratings = np.matmul(user_sim.T.to_numpy(), user_rating) / (sim_sum)
    return predict_ratings


class CBF:
    def __init__(self, data, rating_df):
        self.data = tool.pre_filtering(data)
        self.index = data['FilmID']
        self.rating_df = rating_df
        self.sim_df = None

    def predict(self, user, rating_col='rating', user_col='userId', item_col='movieId'):
        self.sim_df = similarity_matrix(self.data, self.data)
        return self.index, rating(self.rating_df, self.sim_df, user, rating_col, user_col, item_col)


class CF:
    def __init__(self, rating_df):
        self.data = None
        self.sim_df = None
        self.rating_df = rating_df

    def predict(self, user, rating_col='rating', user_col='userId', item_col='movieId'):
        self.data = self.rating_df.pivot(item_col, user_col, rating_col).fillna(0)
        self.sim_df = similarity_matrix(self.data, self.data)
        return rating(self.rating_df, self.sim_df, user, rating_col, user_col, item_col)


# 처음 온 사람을 위한 컨텐츠 기반 추천시스템
class CBFv2:
    def __init__(self, data, values):
        self.data = tool.pre_filtering(data)
        self.values = values
        self.index = data['FilmID']
        self.sim_df = None

    def predict(self, top):
        target_value = np.array(self.values).reshape(1, -1)
        self.sim_df = similarity_matrix(target_value, self.data)
        sim_idx = self.sim_df.argsort()[::-1][0, :top + 1]
        result = self.index.loc[sim_idx]['FilmID']
        return result[:top]
