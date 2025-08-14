'''
PART 2: NETWORK CENTRALITY METRICS

Using the imbd_movies dataset
- Build a graph and perform some rudimentary graph analysis, extracting centrality metrics from it. 
- Below is some basic code scaffolding that you will need to add to
- Tailor this code scaffolding and its stucture to however works to answer the problem
- Make sure the code is inline with the standards we're using in this class 
'''

import pandas as pd
import networkx as nx
import json
from datetime import datetime

# Build the graph
g = nx.Graph()

# Set up your dataframe(s) -> the df that's output to a CSV should include at least the columns 'left_actor_name', '<->', 'right_actor_name'


with open("data/imdb.json", "r") as in_file:
    # Don't forget to comment your code
    for line in in_file:

        # Don't forget to include docstrings for all functions

        # Load the movie from this line
        this_movie = json.loads(line)
        # Create a node for every actor
        for actor_id,actor_name in this_movie['actors']:
        # add the actor to the graph
            g.add_node(actor_name)    
        # Iterate through the list of actors, generating all pairs
        ## Starting with the first actor in the list, generate pairs with all subsequent actors
        ## then continue to second actor in the list and repeat
        
            i = 0 #counter
        for left_actor_id,left_actor_name in this_movie['actors']:
            for right_actor_id,right_actor_name in this_movie['actors'][i+1:]:

                # Get the current weight, if it exists
                if g.has_edge(left_actor_name, right_actor_name):
                    g[left_actor_name][right_actor_name]['weight'] += 1
                
                
                # Add an edge for these actors
                else:
                    g.add_edge(left_actor_name,right_actor_name, weight=1)
                


# Print the info below
print("Nodes:", len(g.nodes))
print("Edges:", len(g.edges))

#Print the 10 the most central nodes
centrality = nx.degree_centrality(g)
top_10 = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:10]
print("centrality top 10")
for name, centrality in top_10:
    print(f'{name}, {centrality:.2f} ')


# Output the final dataframe to a CSV named 'network_centrality_{current_datetime}.csv' to `/data'
final_dict = []
for left_actor, right_actor, data in g.edges(data=True):
    final_dict.append({
        'left_actor_name': left_actor,
        '<->': '<->',
        'right_actor_name': right_actor,
        'weight': data['weight']
    })
final_df = pd.DataFrame(final_dict)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

final_df.to_csv(f"data/network_centrality_{timestamp}.csv", index=False)
