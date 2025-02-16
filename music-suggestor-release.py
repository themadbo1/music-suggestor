import spotipy
import requests
import elementpath
import xml.etree.ElementTree as ET
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
client_id = 'YOUR CLIENT ID'
client_secret = 'YOUR CLIENT SECRET'

# Authenticate using the Client Credentials flow
#client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
#sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri="https://google.com",
                                               scope=["playlist-modify-public", "playlist-modify-private", "user-library-read", "user-read-private"]))
#xml_data = """<toptags artist="Cher" track="Believe">
#  <tag>
#    <name>pop</name>
#    <count>97</count>
#    <url>www.last.fm/tag/pop</url>
#  </tag>
#  <tag>
#    <name>dance</name>
#    <count>88</count>
#    <url>www.last.fm/tag/dance</url>
#  </tag>
#</toptags>"""
#
## Parse the XML string
#root = ET.fromstring(xml_data)
#
## Use XPath to select all <name> elements
#names = [name.text for name in elementpath.select(root, "/toptags/tag/name")]
#
#print(type(names))  # Output: ['pop', 'dance']






API = "YOUR LASTFM API CODE"
artist = input("Name the Artist for the song you are providing: ")
artist = artist.lower()
track = input("Provide the name of the track you are looking for: ")
for i in track:
    if i == " ":
        track.replace(" ", "+")
        break
    else:
        continue
track = track.lower()


link = f"http://ws.audioscrobbler.com/2.0/?method=track.gettoptags&artist={artist}&track={track}&api_key={API}"
x = requests.post(link)
x = x.text

root = ET.fromstring(x)
genre = [name.text for name in elementpath.select(root, "/lfm/toptags/tag/name")]

genre = genre[0]
print(genre)
link = f"http://ws.audioscrobbler.com/2.0/?method=track.getsimilar&artist={artist}&track={track}&api_key={API}"
x = requests.post(link)
x = x.text

root = ET.fromstring(x)

track_info = {}
for track in root.findall(".//track"):
    track_name = track.find("name").text
    artist_name = track.find("artist/name").text

    track_name = track_name.lower()
    
    for i in track_name:
        if i == "`":
            track_name = track_name.replace("`","")
        elif i == ",":
            track_name = track_name.replace(",","")
        elif i == ".":
            track_name = track_name.replace(".","")
        elif i == "'":
            track_name = track_name.replace("'","")
    
    for i in artist_name:
        if i == "&":
            artist_name = artist_name.replace("&", "")
    


    link = f"http://ws.audioscrobbler.com/2.0/?method=track.gettoptags&artist={artist_name}&track={track_name}&api_key={API}"
    x = requests.post(link)
    x = x.text




  
    root = ET.fromstring(x)
    genre_test = [name.text for name in elementpath.select(root, "/lfm/toptags/tag/name")]
    #print(genre_test)
    if len(genre_test) == 0:
        continue
    genre_test = genre_test[0]
    if genre == genre_test:
        track_info[track_name]=artist_name
    else:
        continue
    # Store track name and artist in a dictionary and add it to the list

    
#print(track_info)
#with open("logtext.log", "w") as file:
#    file.write(x.text)
uri = sp.current_user()['uri']
id = sp.current_user()['id']

pl_name = input("what do you want your playlist to be called: ")
x = sp.user_playlist_create(id,pl_name)

playlist_id = x["id"]
print(playlist_id)
timer = 0
#remaster%20track:Doxy%20artist:Miles%20Davis
"""
track = sp.search("Black Pearl Jam",type='track', limit=1)
track =track["tracks"]
track = track["items"]
track = track[0]
track_id = track["uri"]
sp.playlist_add_items(playlist_id,track_id)
print(track_id)
"""
for i in track_info:
    query= i + track_info[i]
    track = sp.search(query,type='track', limit=1)
    track =track["tracks"]
    track = track["items"]
    track = track[0]
    track_id = track["uri"]
    sp.playlist_add_items(playlist_id,[track_id])
    timer = timer + 1
    if timer >= 51:
        break
print("done")
