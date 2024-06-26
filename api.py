import requests
from bs4 import BeautifulSoup
from apikey import api_token

def get_song_lyrics(song_title, artist_name, api_token):
    base_url = "https://api.genius.com"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    search_url = base_url + "/search?"
    query = f"{song_title} {artist_name}"
    params = {
        'q': query
    }
    response = requests.get(search_url, headers=headers, params=params)
    json_data = response.json()

    song_info = None
    for hit in json_data['response']['hits']:
        if song_title.lower() in hit['result']['title'].lower():
            song_info = hit
            break
    
    if song_info:
        song_url = song_info['result']['url']
        lyrics_response = requests.get(song_url, headers=headers)
        return lyrics_response.text
    else:
        return "Lyrics not found"
    
def SaveLyrics(lyrics, filename):
    # create file
    with open(filename, "w", encoding="utf-8") as file:
        file.write(lyrics)
    print(f"Lyrics saved to {filename}")
    
def extract_lyrics(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    lyrics_div = soup.find_all('div', {'data-lyrics-container': 'true'})
    if lyrics_div:
        return str(lyrics_div)
    else:
        return "[Lyrics not found in the expected format]"

def main():
    song_title = input("Enter the song title: ")    

    lyrics = get_song_lyrics(song_title, api_token)    
    extractedLyrics = extract_lyrics(lyrics)
    SaveLyrics(extractedLyrics, f"{song_title}.txt")
    

if __name__ == "__main__":
    main()
