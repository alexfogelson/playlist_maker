import requests
import re
import json
import sys

playlist = []

if (len(sys.argv) < 2):
    print("Please run again, placing the desired phrase in quotes after the program name.")
    sys.exit()

phrase = sys.argv[1]
words = phrase.split(' ')
verbose = len(sys.argv) > 2 and sys.argv[2].lower() == "verbose"

default_limit = 10

def query_song(song, attempt_number, limit):
    song = song.lower()
    if (attempt_number > 10):
        return None
    song_results = requests.get("https://itunes.apple.com/search?", params = {"term": song, "media": "music", "limit": limit, "attribute": "songTerm"})

    if (not(song_results.ok)):
        query_song(song, attempt_number + 1, default_limit)


    json_results = json.loads(song_results.text)
    #if (verbose):
        #print(json.dumps(json_results, indent=1))

    if (json_results["resultCount"] != None and json_results["resultCount"] > 0):
        results = json_results["results"]
        for track in results:
            song_title = track["trackName"]
            artist_name = track["artistName"]

            if (song_title.upper() == song.upper()):
                return (song_title, artist_name)

        for track in results:
            song_title = track["trackName"]
            artist_name = track["artistName"]

            if (song_title.upper().find(song.upper() + ' ') == 0):
                return (song_title, artist_name)

        #found nothing, so give us information
        if (verbose):
            for track in results:
                song_title = track["trackName"]
                artist_name = track["artistName"]

                print(song_title + "by" + artist_name)
    if (limit == 100):
        return None 
    else:
        return query_song(song, attempt_number + 1, 100)

sys.stdout.write("0%")
counter = 1
for word in words:
    sys.stdout.flush()
    sys.stdout.write('\r' + str(round(counter/len(words)*100)) + "%")
    playlist.append(query_song(word, 0, default_limit))
    counter += 1
    
sys.stdout.write('\r')


for songs in playlist:
    if (songs != None):
        (title, artist) = songs
        print(title + " by " + artist)
