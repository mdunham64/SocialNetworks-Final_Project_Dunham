import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math as math
import time

from networkx import Graph
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

df = pd.read_csv('tiktoks_trending.csv', encoding='UTF8')

df.head()

text_content = df['description']
#
# TfidfVectorizer uses a in-memory vocabulary (a python dict) to map the most frequent words to features indices
# and hence compute a word occurrence frequency (sparse) matrix. The word frequencies are then reweighted using
# the Inverse Document Frequency (IDF) vector collected feature-wise over the corpus.
#
vector = TfidfVectorizer(max_df=.4,  # this drops words that are used more than 60% of the time, like #
                         min_df=1,  # this does the same thing but only uses words that appear 1 time
                         stop_words='english',  # this removes stop words like a and articles
                         lowercase=True,
                         use_idf=True,
                         smooth_idf=True)  # prevents divide by zero errors

tfidf = vector.fit_transform(
    text_content)  # this will convert our raw description data into a matrix of TF-IDF features


# Find similar : get the top_n movies with description similar to the target description
def find_similar(tfidf_matrix, index, top_n=5):
    cosine_similarities = linear_kernel(tfidf_matrix[index:index + 1], tfidf_matrix).flatten()
    related_docs_indices = [i for i in cosine_similarities.argsort()[::-1] if i != index]
    return [index for index in related_docs_indices][0:top_n]


G: Graph = nx.Graph(label="Tik-Toks")

start_time = time.time()

for i, row_i in df.iterrows():
    G.add_node(row_i['NickName'], key=row_i['Unique Name'], label="Tik-Toks", description=row_i['description'],
               duration=row_i['duration'], song_name=row_i['song name'])
    indices = find_similar(tfidf, i, top_n=5)
    snode = "S: " + row_i['NickName']
    G.add_node(snode, label="SIMILAR")
    G.add_edge(row_i['NickName'], snode, label="SIMILARITY")
    for element in indices:
        G.add_edge(snode, df['NickName'].loc[element], label="SIMILARITY")


def get_all_adj_nodes(list_in):
    sub_graph = set()
    for m in list_in:
        sub_graph.add(m)
        for e in G.neighbors(m):
            sub_graph.add(e)
    return list(sub_graph)


def draw_sub_graph(sub_graph):
    subgraph = G.subgraph(sub_graph)
    colors = []
    for e in subgraph.nodes():
        if G.nodes[e]['label'] == "Tik-Toks":
            colors.append('blue')
        elif G.nodes[e]['label'] == "SIMILAR":
            colors.append('red')
        elif G.nodes[e]['label'] == "DURATION":  # not used in report, but interesting findings in relation to duration
            colors.append('green')

    nx.draw(subgraph, with_labels=True, font_weight='normal', node_color=colors)
    plt.show()


def get_recommendation(root):
    commons_dict = {}
    for e in G.neighbors(root):
        for e2 in G.neighbors(e):
            if e2 == root:
                continue
            if G.nodes[e2]['label'] == "Tik-Toks":
                commons = commons_dict.get(e2)
                if commons == None:
                    commons_dict.update({e2: [e]})
                else:
                    commons.append(e)
                    commons_dict.update({e2: commons})
    tik_toks = []
    weight = []
    for key, values in commons_dict.items():
        w = 0.0
        for e in values:
            w = w + 1 / math.log(G.degree(e))
        tik_toks.append(key)
        weight.append(w)

    result = pd.Series(data=np.array(weight), index=tik_toks)
    result.sort_values(inplace=True, ascending=False)
    return result


#  BELOW GETS ME THE RECOMMENDATIONS
#  research using MicrosoftWord for tight knit community
account_name = "SuzanFreek"
result = get_recommendation(account_name)
print(f"*" * 40 + f"\n Recommendation for {account_name} \n" + "*" * 40)
print(result.head())

#  BELOW GETS ME THE PRETTY GRAPH
reco = list(result.index[:4].values)
reco.extend([account_name])
sub_graph = get_all_adj_nodes(reco)
draw_sub_graph(sub_graph)
