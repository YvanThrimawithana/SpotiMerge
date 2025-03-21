import spotipy
from spotipy.oauth2 import SpotifyOAuth
import re

# Set up Spotify API credentials
SPOTIPY_CLIENT_ID = 'YOUR_SPOTIFY_CLIENT_ID'
SPOTIPY_CLIENT_SECRET = 'YOUR_SPOTIFY_CLIENT_SECRET'
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:8888/callback'
SCOPE = 'playlist-modify-public playlist-modify-private playlist-read-private'

def extract_playlist_id(playlist_link):
    # Extract playlist ID from Spotify URL
    pattern = r'playlist/([a-zA-Z0-9]+)'
    match = re.search(pattern, playlist_link)
    return match.group(1) if match else None

def main():
    # Initialize Spotify client
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=SCOPE
    ))

    # Get playlist link from user
    playlist_link = input("Enter Spotify playlist link: ")
    playlist_id = extract_playlist_id(playlist_link)

    if not playlist_id:
        print("Invalid playlist link!")
        return

    try:
        # Get playlist details
        playlist = sp.playlist(playlist_id)
        total_tracks = playlist['tracks']['total']
        playlist_name = playlist['name']
        
        if total_tracks <= 500:
            print(f"Playlist '{playlist_name}' has {total_tracks} tracks. No split needed.")
            return

        # Create Part 1 and Part 2 playlists
        user_id = sp.current_user()['id']
        part1_name = f"{playlist_name} (Part 1)"
        part2_name = f"{playlist_name} (Part 2)"
        part1_playlist = sp.user_playlist_create(user_id, part1_name)
        part2_playlist = sp.user_playlist_create(user_id, part2_name)

        # Get all tracks
        tracks = []
        offset = 0
        while offset < total_tracks:
            results = sp.playlist_tracks(playlist_id, offset=offset)
            tracks.extend(results['items'])
            offset += len(results['items'])

        # Get track URIs for both playlists
        part1_tracks = [track['track']['uri'] for track in tracks[:500]]
        part2_tracks = [track['track']['uri'] for track in tracks[500:]]

        # Add tracks to Part 1 playlist
        print("\nCreating Part 1 playlist...")
        for i in range(0, len(part1_tracks), 100):
            batch = part1_tracks[i:i + 100]
            sp.playlist_add_items(part1_playlist['id'], batch)
            print(f"Added tracks {i+1}-{min(i+100, 500)} to Part 1 playlist")

        # Add tracks to Part 2 playlist
        print("\nCreating Part 2 playlist...")
        for i in range(0, len(part2_tracks), 100):
            batch = part2_tracks[i:i + 100]
            sp.playlist_add_items(part2_playlist['id'], batch)
            print(f"Added tracks {i+1}-{min(i+100, len(part2_tracks))} to Part 2 playlist")

        print(f"\nSuccessfully created split playlists:")
        print(f"1. {part1_name} (500 tracks)")
        print(f"2. {part2_name} ({total_tracks - 500} tracks)")
        print(f"Original playlist '{playlist_name}' remains unchanged.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
