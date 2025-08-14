'''
PART 2: SIMILAR ACTROS BY GENRE

Using the imbd_movies dataset:
- Create a data frame, where each row corresponds to an actor, each column represents a genre, and each cell captures how many times that row's actor has appeared in that column’s genre 
- Using this data frame as your “feature matrix”, select an actor (called your “query”) for whom you want to find the top 10 most similar actors based on the genres in which they’ve starred 
- - As an example, select the row from your data frame associated with Chris Hemsworth, actor ID “nm1165110”, as your “query” actor
- Use sklearn.metrics.DistanceMetric to calculate the euclidean distances between your query actor and all other actors based on their genre appearances
- - https://scikit-learn.org/stable/modules/generated/sklearn.metrics.DistanceMetric.html
- Output a CSV continaing the top ten actors most similar to your query actor using cosine distance 
- - Name it 'similar_actors_genre_{current_datetime}.csv' to `/data`
- - For example, the top 10 for Chris Hemsworth are:  
        nm1165110 Chris Hemsworth
        nm0000129 Tom Cruise
        nm0147147 Henry Cavill
        nm0829032 Ray Stevenson
        nm5899377 Tiger Shroff
        nm1679372 Sudeep
        nm0003244 Jordi Mollà
        nm0636280 Richard Norton
        nm0607884 Mark Mortimer
        nm2018237 Taylor Kitsch
- Describe in a print() statement how this list changes based on Euclidean distance
- Make sure your code is in line with the standards we're using in this class
'''

#Write your code below
import os
import json
import pandas as pd
from sklearn.metrics import DistanceMetric
from sklearn.metrics.pairwise import cosine_distances
from datetime import datetime




path = os.path.join(os.path.dirname(__file__), 'data')


#load data
with open('data/imdb.json', "r") as f:
    movies = [json.loads(line) for line in f]

#create a matrix so that actors are rows and the columns are genres

actor_genre_count={}
for movie in movies:
    genres = movie.get("genres")
    actors = movie.get("actors")
    for actor_id, actor_name in actors:
        if actor_id not in actor_genre_count:
            actor_genre_count[actor_id] = {"actor_name": actor_name}
        for genre in genres:
            actor_genre_count[actor_id][genre] = actor_genre_count[actor_id].get(genre, 0) + 1

actor_df = pd.DataFrame.from_dict(actor_genre_count, orient='index').fillna(0)
        
actor_names = actor_df["actor_name"]
actor_features = actor_df.drop(columns=["actor_name"])

# example
query_actor_id = "nm1165110"
query_vector = actor_features.loc[query_actor_id].values.reshape(1, -1)

#cosine distance
cosine_scores = cosine_distances(query_vector, actor_features.values)[0]

# Put into DataFrame for ranking
cosine_df = pd.DataFrame({
    "actor_id": actor_features.index,
    "actor_name": actor_names,
    "cosine_distance": cosine_scores
}).sort_values(by="cosine_distance")

# Top 10 most similar actors (excluding Chris himself)
top10_cosine = cosine_df[cosine_df["actor_id"] != query_actor_id].head(10)

#to CSV
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
top10_cosine.to_csv(f'data/similar_actors_genre_{timestamp}.csv', index=False)

#euclidean Distance
euclidean_dist = DistanceMetric.get_metric("euclidean")
euclidean_scores = euclidean_dist.pairwise(query_vector, actor_features.values)[0]
euclidean_df = pd.DataFrame({
    "actor_id": actor_features.index,
    "actor_name": actor_names,
    "euclidean_distance": euclidean_scores
}).sort_values(by="euclidean_distance")

top10_euclidean = euclidean_df[euclidean_df["actor_id"] != query_actor_id].head(10)

print("Top 10 similar actors to Chris Hemsworth (Cosine distance):")
print(top10_cosine)

print("Top 10 similar actors to Chris Hemsworth (Euclidean distance):")
print(top10_euclidean)

print("Cosine distance finds actors most alike in style like Tom Cruise, Henry Cavill, while Euclidean distance favors actors closer in features.")


