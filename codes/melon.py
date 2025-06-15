import requests
from bs4 import BeautifulSoup,Comment, NavigableString

def extract_lyrics(soup):
    lyrics_div = soup.select_one("#d_video_summary")
    if not lyrics_div:
        return ""

    lines = []
    for elem in lyrics_div.children:
        if isinstance(elem, Comment):
            continue
        elif isinstance(elem, NavigableString):
            text = elem.strip()
            if text:
                lines.append(text)
        elif elem.name == "br":
            lines.append("\n")

    # 줄바꿈 기준으로 나누고 정리
    lyrics = "".join(lines)
    cleaned = "\n".join([
        line.strip() for line in lyrics.split("\n") if line.strip()
    ])
    return cleaned



def get_song(song_url: str):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.melon.com"
    }
    response = requests.get(song_url, headers=headers)
    response.encoding = "utf-8"  # 혹시 한글 깨지면

    soup = BeautifulSoup(response.text, "html.parser")

    try:
        title_div = soup.select_one("#downloadfrm > div > div > div.entry > div.info > div.song_name")
        title = title_div.get_text(strip=True).replace("곡명", "").strip()
        artist = soup.select_one("#downloadfrm > div > div > div.entry > div.info > div.artist > a > span:nth-child(1)").text.strip()
        album = soup.select_one("#downloadfrm > div > div > div.entry > div.meta > dl > dd:nth-child(2) > a").text.strip()
        release_date = soup.select_one("#downloadfrm > div > div > div.entry > div.meta > dl > dd:nth-child(4)").text.strip()
        lyrics = extract_lyrics(soup)

        return {
            "title": title,
            "artist": artist,
            "album": album,
            "release_date": release_date,
            "lyrics": lyrics
        }
    except Exception as e:
        print("오류 발생:", e)
        return None
    
song_info = get_song("https://www.melon.com/song/detail.htm?songId=33367293")
if song_info:
    print("제목:", song_info["title"])
    print("아티스트:", song_info["artist"])
    print("앨범:", song_info["album"])
    print("발매일:", song_info["release_date"])
    print("가사:\n", song_info["lyrics"])