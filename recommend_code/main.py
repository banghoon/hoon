import recommend
import pandas as pd

movie_data = pd.read_csv('./dataset/film.csv')
rating_data = pd.read_csv('./dataset/rangering.csv')

model = recommend.CBF(movie_data, rating_data)
index, result = model.predict(1, 'Rangering', 'BrukerID', 'FilmID')
print(pd.Series(result, index=index))

model2 = recommend.CF(rating_data)
print(model2.predict(1, 'Rangering', 'BrukerID', 'FilmID'))

# CBF와 CF의 크기가 다른 경우 어떻게 처리를 할 것인가
# 완전 처음 온 사람의 경우 컨텐츠 기반을 통해 유사도로만 추천해줄것인가

