import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

data = pd.read_csv('dataset/movie.csv')

data['Genre'] = data['Genre'].str.replace(',' , ' ')
data['Actors'] = data['Actors'].str.replace(',' , ' ')
data['Title'] = data['Title'].str.lower()

data_recommend = data.drop(['Rank', 'Year' ,'Runtime (Minutes)' ,'Rating' ,'Votes' ,'Revenue (Millions)', 'Metascore'],axis=1)

data_recommend['combine'] = data_recommend[data_recommend.columns[1:]].apply(
        lambda x: ','.join(x.dropna().astype(str)),axis=1)

count =  CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(data_recommend['combine'])

cosine_sim = cosine_similarity(count_matrix)

names = data_recommend['Title']

indices = pd.Series(data_recommend.index, index=data_recommend['Title'])

def recommend(title):
        title = title.lower()

        if title not in data_recommend['Title'].unique():
                return 'Movie not in Database'

        else:
                
                sim_scores = list(enumerate(cosine_sim[indices[title]]))
                sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
                sim_scores = sim_scores[1:11]

                movie_indices = [i[0] for i in sim_scores]
                movie_title = data['Title'].iloc[movie_indices]
                movie_genre = data['Genre'].iloc[movie_indices]

                recommendation_data = pd.DataFrame(columns=['Genre','Name'])
                recommendation_data['Genre'] = movie_genre
                recommendation_data['Name'] = movie_title

                #result = recommendation_data.to_json(orient = 'records')
                
                return   recommendation_data.to_dict('records')

        



        

