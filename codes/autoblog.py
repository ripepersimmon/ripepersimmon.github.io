import re
from datetime import datetime
from melon import get_song
import logging
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

# .env 파일에서 환경변수 불러오기
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def get_user_input():
    try:
        melon_url = input("멜론 곡 URL을 입력하세요: ").strip()
        youtube_url = input("YouTube URL을 입력하세요: ").strip()
        filename = input("악보 파일 경로 또는 링크를 입력하세요 (예: /downloads/song.pdf 또는 Gumroad 링크): ").strip()
        instrument = input("악기 파트를 입력하세요 (예: Piano, Violin): ").strip()
        return melon_url, youtube_url, filename, instrument
    except Exception as e:
        logging.error(f"입력 오류: {e}")
        exit(1)

def generate_filename(song_info, instrument):
    today = datetime.now().strftime("%Y-%m-%d")
    raw_title = f"{today}-{song_info['title']}_{instrument}_악보_pdf_다운로드.md"
    # Windows에서 사용할 수 없는 문자 제거
    return re.sub(r'[<>:"/\\|?*]', '', raw_title)

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GOOGLE_CX = os.getenv('GOOGLE_CX')

# RAG(곡 정보 요약) 기능 임시 비활성화
# def get_google_summary(query, lang='ko'):
#     """
#     Google Custom Search API를 사용해 곡에 대한 요약 정보를 추출합니다.
#     """
#     try:
#         api_url = 'https://www.googleapis.com/customsearch/v1'
#         params = {
#             'key': GOOGLE_API_KEY,
#             'cx': GOOGLE_CX,
#             'q': query,
#             'hl': lang,
#             'num': 3
#         }
#         response = requests.get(api_url, params=params, timeout=10)
#         data = response.json()
#         if 'items' in data and len(data['items']) > 0:
#             # 첫 번째 검색 결과의 스니펫 사용
#             snippet = data['items'][0].get('snippet', '').replace('\n', ' ')
#             return snippet or '검색 결과를 찾을 수 없습니다.'
#         else:
#             return '검색 결과를 찾을 수 없습니다.'
#     except Exception as e:
#         logging.warning(f"Google API 정보 검색 실패: {e}")
#         return '검색 결과를 찾을 수 없습니다.'

def make_markdown(song_info, youtube_url: str, filename: str, instrument: str):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S +0900")
    title = song_info["title"]
    artist = song_info["artist"]
    album = song_info["album"]
    release_date = song_info["release_date"]
    album_art = song_info.get("album_art")
    lyrics_lines = song_info["lyrics"].split("\n")
    formatted_lyrics = "\n".join([line.strip() + "  " for line in lyrics_lines if line.strip()])
    post_title = f"{title}-{artist}_{instrument} 악보 PDF 다운로드"
    youtube_embed = f'<iframe width="560" height="315" src="{youtube_url.replace("watch?v=", "embed/")}" frameborder="0" allowfullscreen></iframe>'
    download_button = f'<p><a href="{filename}" download><strong>📥 Download Sheet Music</strong></a></p>'
    # 앨범 아트 썸네일 추가
    thumbnail_md = f'![앨범아트]({album_art})\n' if album_art else ''
    return f"""---
layout: post
title: {post_title}
date: {now}
categories: sheet
thumbnail: {album_art if album_art else ''}
---

{thumbnail_md}{youtube_embed}

## 🎵 {title} - {artist}

- **앨범**: {album}  
- **발매일**: {release_date}  

### 가사
{formatted_lyrics}

## 다운로드

{{% include adsense.html %}}

{download_button}

## 작성자 
- **작성자**: autoblog.bot made by sahong
- **작성일**: {now}
"""

def save_markdown(output_filename, markdown_content):
    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        logging.info(f"{output_filename} 로 저장되었습니다.")
    except Exception as e:
        logging.error(f"파일 저장 오류: {e}")
        exit(1)

# main() 함수 및 직접 실행 부분 제거 (실행 파일에서 import해서 사용)
