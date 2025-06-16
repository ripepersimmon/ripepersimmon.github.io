import requests
from bs4 import BeautifulSoup, Comment, NavigableString
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def extract_lyrics(soup):
    lyrics_div = soup.select_one("#d_video_summary")
    if not lyrics_div:
        logging.warning("가사 정보를 찾을 수 없습니다.")
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

def get_album_art(soup):
    # 앨범 아트 URL 추출
    img_tag = soup.select_one('#d_song_org > a > img')
    if img_tag and img_tag.has_attr('src'):
        return img_tag['src']
    return None

def get_song(song_url: str):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.melon.com"
    }
    try:
        response = requests.get(song_url, headers=headers, timeout=10)
        response.encoding = "utf-8"  # 혹시 한글 깨지면
        if response.status_code != 200:
            logging.error(f"HTTP 오류: {response.status_code} - {song_url}")
            return None
        soup = BeautifulSoup(response.text, "html.parser")
        title_div = soup.select_one("#downloadfrm > div > div > div.entry > div.info > div.song_name")
        if not title_div:
            logging.error("곡 제목 정보를 찾을 수 없습니다.")
            return None
        title = title_div.get_text(strip=True).replace("곡명", "").strip()
        artist_elem = soup.select_one("#downloadfrm > div > div > div.entry > div.info > div.artist > a > span:nth-child(1)")
        album_elem = soup.select_one("#downloadfrm > div > div > div.entry > div.meta > dl > dd:nth-child(2) > a")
        release_elem = soup.select_one("#downloadfrm > div > div > div.entry > div.meta > dl > dd:nth-child(4)")
        if not (artist_elem and album_elem and release_elem):
            logging.error("아티스트/앨범/발매일 정보를 찾을 수 없습니다.")
            return None
        artist = artist_elem.text.strip()
        album = album_elem.text.strip()
        release_date = release_elem.text.strip()
        lyrics = extract_lyrics(soup)
        album_art = get_album_art(soup)
        return {
            "title": title,
            "artist": artist,
            "album": album,
            "release_date": release_date,
            "lyrics": lyrics,
            "album_art": album_art
        }
    except Exception as e:
        logging.error(f"오류 발생: {e}")
        return None
