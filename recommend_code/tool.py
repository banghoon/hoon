import pandas as pd


def load_data(file_paths):  # rank 와 data 의 크기 차이 문제
    rank, data = file_paths
    return pd.DataFrame(rank), pd.DataFrame(data)


def pre_filtering(dataset, options=None):  # 단순 필터링 요소 1 True -1 False 0 None ??????
    data = dataset.iloc[:, 2:]
    return data

