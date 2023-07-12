from flask import Flask, request, render_template
import pandas as pd
from fuzzywuzzy import fuzz

app = Flask(__name__)


@app.route("/")
def Home():
    return render_template("index.html")

@app.route("/recommend", methods=['POST'])
def recommend():
    song_name=request.form['song']
    print(song_name)
    rec_df=calculate(song_name)
    # if rec_songs==-1:
    #     pass
    return render_template("index.html", input_song=song_name,rec_songs=rec_df.to_html(classes='table table-striped', index=False), titles=rec_df.columns.values)

def calculate(song_name):
    cluster_df=pd.read_csv('clustered_df.csv')
    flag=False
    for i, row in cluster_df.iterrows():
        if(fuzz.token_set_ratio(song_name, row['name'])>90):
            song_name=row['track_name']
            song_cluster=row['cluster']
            song_genre=row['track_genre']
            song_artist=row['artists']
            flag=True
            break
    if flag==False:
        return -1
    cluster_df = cluster_df[cluster_df['cluster']==song_cluster]
    cluster_df['genre_var']=0
    cluster_df.loc[cluster_df['track_genre']==song_genre, 'genre_var']=1
    print(cluster_df['genre_var'].value_counts())
    cluster_df=cluster_df.sort_values(by=['genre_var','popularity'], ascending=[False,False])
    rec_df=cluster_df[['track_name','artists','album_name','track_genre']]
    rec_df.rename(columns={'track_name':'Song','artists':'Artist','album_name':'Album','track_genre':'Genre'}, inplace=True)
    print(rec_df[:10])
    return rec_df[:10]
    
    

if __name__ == "__main__":
    app.run(debug=True)
