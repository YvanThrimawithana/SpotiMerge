# SpotiMerge

A python tool to help split spotify playlists with more than 500 songs

## Features

- Split large Spotify playlists (>500 tracks) into smaller ones
- Takes the original playlist and create playlist copies with a max limit of 500 each so that original playlist stays intact. 

## Installation

1. Clone this repository
2. Install required packages:
```bash
pip install spotipy ytmusicapi
```

## Setup

### Spotify Setup
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new application
3. Set the redirect URI to: `http://127.0.0.1:8888/callback`
4. Copy your Client ID and Client Secret
5. Update `playlist_splitter.py` with your credentials if needed


## Usage

### Splitting Spotify Playlists

```bash
pip install -r requirements.txt
```

```bash
python playlist_splitter.py
```
- Enter your Spotify playlist URL when prompted
- The script will create two new playlists if the original has more than 500 tracks


## Notes

- Spotify playlists are split at the 500-track limit
- Original playlists remain unchanged
- New playlists are created as private by default
