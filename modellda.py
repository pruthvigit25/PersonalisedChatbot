import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

data = pd.read_csv("space-news.csv")
data_2 = pd.read_csv("space-news-2.csv")
data_3 = pd.read_csv("space-news-3.csv")
data_4 = pd.read_csv("space-news-4.csv")
data_5 = pd.read_csv("space-news-5.csv")

data["text"] = data["title"] + " " + data["content"] + " " + data["postexcerpt"] + " " + data_2["title"]+ " " + data_2["body"]+ " " + data_3["title"]+ " " + data_3["body"]+ " " + data_3["description"]+ " " + data_4["Column_1"]+ " " + data_4["Column_2"]+" " + data_4["Column_3"]+" " + data_4["Column_4"]+" " + data_4["Column_5"]+" " + data_4["Column_6"]+" " + data_5["Column_1"]+" " + data_5["Column_2"]+" " + data_5["Column_3"]+" " + data_5["Column_4"]+" " + data_5["Column_5"]+" " + data_5["Column_6"]+" " + data_5["Column_7"]+" " + data_5["Column_8"]+" " + data_5["Column_9"]+" " + data_5["Column_10"]+" " + data_5["Column_11"]+" " + data_5["Column_12"]+" " + data_5["Column_13"]+" " + data_5["Column_14"]+" " + data_5["Column_15"]+" " + data_5["Column_16"]+" " + data_5["Column_17"]+" " + data_5["Column_18"]+" " + data_5["Column_19"]+" " + data_5["Column_20"]+" " + data_5["Column_21"]+" " + data_5["Column_22"]+" " + data_5["Column_23"]

vectorizer = CountVectorizer(stop_words="english", max_features=1000)
data["text"] = data["text"].fillna("")

dtm = vectorizer.fit_transform(data["text"])
lda = LatentDirichletAllocation(n_components=20, random_state=42)
lda.fit(dtm)

with open('updatedlda_model.pkl', 'wb') as f:
    pickle.dump(lda, f)