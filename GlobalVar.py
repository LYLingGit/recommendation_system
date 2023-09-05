import tkinter as tk

userid = 1
BigWindow = tk.Tk()

#data的位置
pathmovie = "D:/workspace_py/RecommendationSystem/data/movies.csv"
pathlink = "D:/workspace_py/RecommendationSystem/data/links.csv"
pathrating = "D:/workspace_py/RecommendationSystem/data/ratings.csv"
pathcosSim_svd = "D:/workspace_py/RecommendationSystem/data/cosSim.csv"#pickle
pathmovie_similar_svd = "D:/workspace_py/RecommendationSystem/data/movie_similar_svd.csv"
pathoffline_recommend_svd = "D:/workspace_py/RecommendationSystem/data/offline_recommend_svd.csv"
pathoffline_recommend_als = "D:/workspace_py/RecommendationSystem/data/offline_recommend_als.csv"
pathmovie_similar_svd ="D:/workspace_py/RecommendationSystem/data/movie_similar_svd.csv"
pathmovie_similar_als = "D:/workspace_py/RecommendationSystem/data/movie_similar_als.csv"
pathusers = "D:/workspace_py/RecommendationSystem/data/users.csv"

pathonline_recommend = "D:/workspace_py/RecommendationSystem/data/online_recommend.csv"
pathmovieidlist = "D:/workspace_py/RecommendationSystem/data/movieidlist.pickle"