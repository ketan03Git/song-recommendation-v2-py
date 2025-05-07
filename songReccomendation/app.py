# Music Recommendation System
import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = "66b41aa6cd6841f0a748fe70cb332fa5"
CLIENT_SECRET = "0df1f6441caa4cb3b050d49b10e00359"

client_credentials_manager = SpotifyClientCredentials(client_id = CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q = search_query, type="track")
    
    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        print(album_cover_url)
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"
    
# finding 5 similar songs name and posters url gor that songs
def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_posters = []
    for i in distances[1:6]:
        # fetch the poster
        artist = music.iloc[i[0]].artist
        print(artist)
        print(music.iloc[i[0]].song)
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        recommended_music_names.append(music.iloc[i[0]].song)
        
    return recommended_music_names, recommended_music_posters

st.header('Music Recommender System')
# music = pickle.load(open('songReccomendation/df.pkl', 'rb'))
# similarity = pickle.load(open('songReccomendation/similarity.pkl','rb'))

# files from drive
import gdown

# df.pkl
gdown.download("https://drive.google.com/uc?id=1h3hjNQuHmgQ3kXz3XeZhd7swlbd0xmfN", "songReccomendation/df.pkl", quiet=False)

# similarity.pkl
gdown.download("https://drive.google.com/uc?id=17i298MWl4qAI5D_3L_ybqIu_4OEt49ph", "songReccomendation/similarity.pkl", quiet=False)

music = pickle.load(open('songReccomendation/df.pkl', 'rb'))
similarity = pickle.load(open('songReccomendation/similarity.pkl','rb'))


music_list = music['song'].values
selected_music = st.selectbox(
    "Type or select a song from the dropdown",
    music_list
)

if st.button('show Recommendation'):
    recommended_music_names,recommended_music_posters = recommend(selected_music)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_music_names[0])
        st.image(recommended_music_posters[0])
    with col2:
        st.text(recommended_music_names[1])
        st.image(recommended_music_posters[1])
    with col3:
        st.text(recommended_music_names[2])
        st.image(recommended_music_posters[2])
    with col4:
        st.text(recommended_music_names[3])
        st.image(recommended_music_posters[3])
    with col5:
        st.text(recommended_music_names[4])
        st.image(recommended_music_posters[4])


    