from datetime import datetime
from melon import get_song
from datetime import datetime

def make_markdown(melon_url, youtube_url: str, filename: str):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S +0900")
    song_info = get_song(melon_url)
    title = song_info["title"]
    artist = song_info["artist"]
    album = song_info["album"]
    release_date = song_info["release_date"]
    lyrics = song_info["lyrics"]

    youtube_embed = f'<iframe width="560" height="315" src="{youtube_url.replace("watch?v=", "embed/")}" frameborder="0" allowfullscreen></iframe>'
    download_button = f'<p><a href="{filename}" download><strong>📥 Download Sheet Music</strong></a></p>'

    return f"""---
layout: post
title: {title}
date: {now}
categories: sheet music
---

{youtube_embed}

## 🎵 {title} - {artist}

- **앨범**: {album}  
- **발매일**: {release_date}  

### 가사
{lyrics}
## 다운로드
{download_button}
## 작성자 
- **작성자**: autoblog made by sahong
- **작성일**: {now}
"""


# 사용자 입력 받기
melon_url = input("멜론 곡 URL을 입력하세요: ").strip()
youtube_url = input("YouTube URL을 입력하세요: ").strip()
filename = input("업로드할 파일 이름 (예: sheet_music.pdf): ").strip()
instrument = input("악기 파트를 입력하세요 (예: Piano, Violin): ").strip()

# 곡 정보 가져오기
song_info = get_song(melon_url)

# 마크다운 생성
markdown_content = make_markdown(melon_url, youtube_url, filename)

# 파일명 생성 (공백 제거 + 악기 파트 포함)
safe_title = song_info['title'].replace(" ", "_")
safe_instrument = instrument.replace(" ", "_")
output_filename = f"./{safe_title}_{safe_instrument}_악보_pdf_다운로드.md"

# 파일 저장
with open(output_filename, "w", encoding="utf-8") as f:
    f.write(markdown_content)

print(f"{output_filename}로 저장되었습니다.")
