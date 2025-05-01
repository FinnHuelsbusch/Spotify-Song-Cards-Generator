import os 
import argparse
import spotipy
import requests
from spotipy.oauth2 import SpotifyClientCredentials
import qrcode
from weasyprint import HTML
from urllib.parse import urlparse
from dotenv import load_dotenv

def get_input(inputfile: str):
    with open(inputfile, 'r') as f:
        urls = f.readlines()
        urls = [url.strip() for url in urls]
        # verify if urls are valid
        to_remove = []
        for url in urls:
            parsed_url = urlparse(url)
            if parsed_url.netloc not in ['open.spotify.com', 'spotify.com'] or not any(segment in parsed_url.path for segment in ['track', 'playlist']):
                print(f"Warning: {url} is not a valid Spotify track or playlist URL. Skipping.")
                to_remove.append(url)
        for url in to_remove:
            urls.remove(url)
    return urls

class Song:
    def __init__(self, track_id: str):
        self.track_id = track_id
        self.track = sp.track(track_id)
        # replace '/' in name with '-' to avoid issues with file names
        self.name = self.track['name'].replace('/', '-')
        self.artists = [artist['name'] for artist in self.track['artists']]
        self.release_date = self.track['album']['release_date'].split('-')[0]
        self.album_cover = requests.get(self.track['album']['images'][0]['url'])
        
    def __str__(self):
        return f"{self.name} by {', '.join(self.artists)} ({self.release_date})"
    
    def export_qrcode(self):
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=2,
        )
        qr.add_data(f"spotify:track:{self.track_id}")
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        self.qrcode_path = f"./temp/{self.name.replace(' ', '-').replace('?','')}.png"
        # make path absolute
        self.qrcode_path = os.path.abspath(self.qrcode_path)
        img.save(self.qrcode_path)

    def export_songs_to_pdf(song_list: list):
        # create temp directory
        if not os.path.exists('./temp'):
            os.makedirs('./temp')
        for index, song in enumerate(song_list):
            if index % 12 == 0:
                with open('front_template_table.html', 'r') as f:
                    current_html_front = f.read()
                with open('back_template_table.html', 'r') as f:
                    current_html_back = f.read()
            song.export_qrcode()
            current_html_front = current_html_front.replace("{SONG_NAME_" + f"{index % 12}" + "}", song.name)
            current_html_front = current_html_front.replace("{ARTISTS_" + f"{index % 12}" + "}", ', '.join(song.artists))
            current_html_front = current_html_front.replace("{RELEASE_DATE_" + f"{index % 12}" + "}", song.release_date)
            current_html_front = current_html_front.replace("{ALBUM_COVER_" + f"{index % 12}" + "}", song.album_cover.url)
            current_html_back = current_html_back.replace("{QR-CODE-PATH_" + f"{index % 12}" + "}", song.qrcode_path)
            current_html_back = current_html_back.replace("{BAKCGROUND-PATH}", os.path.abspath("background.jpg"))
            # write current_html to file
            if index % 12 == 11 or index == len(song_list) - 1:
                HTML(string=current_html_front).write_pdf(f"./output/{index // 12}-front.pdf")
                with open(f'./temp/{index // 12}-front.html', 'w') as f:
                    f.write(current_html_front)
                HTML(string=current_html_back, base_url='file://').write_pdf(f"./output/{index // 12}-back.pdf")
                with open(f'./temp/{index // 12}-back.html', 'w') as f:
                    f.write(current_html_back)
                print(f"Exported {index // 12}.pdf")
        # remove temp files
        for file in os.listdir('./temp'):
            os.remove(os.path.join('./temp', file))

            

def main(inputfile: str):
    urls = get_input(inputfile)
    songs = []
    track_ids = []
    for url in urls:
        if 'track'  in url:
            track_id = url.split('/')[-1]
            track_id = track_id.split('?')[0]
            if track_id in track_ids:
                continue
            track = Song(track_id)
            songs.append(track)
            track_ids.append(track_id)
        elif 'playlist' in url:
            playlist_id = url.split('/')[-1]
            playlist_id = playlist_id.split('?')[0]
            playlist = sp.playlist(playlist_id)
            for track in playlist['tracks']['items']:
                track_id = track['track']['id']
                if track_id in track_ids:
                    continue
                song = Song(track_id)
                songs.append(song)
                track_ids.append(track_id)
    Song.export_songs_to_pdf(songs)
        
    



if __name__ == "__main__":

    # define parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Inputfile containig Spotify urls of songs to include', default="input.txt", dest='input', type=str)
    # parse arguments
    args = parser.parse_args()

    # Load environment variables from .env file
    load_dotenv()

    # Get credentials from environment variables or command line
    client_id = os.getenv("SPOTIFY_CLIENT_ID") or input("Enter Spotify Client ID: ")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET") or input("Enter Spotify Client Secret: ")

    spotifyCredentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=spotifyCredentials)

    main(args.input)