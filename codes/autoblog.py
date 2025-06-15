from datetime import datetime
from melon import get_song

def make_markdown(melon_url, youtube_url: str, filename: str, instrument: str):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S +0900")
    song_info = get_song(melon_url)
    title = song_info["title"]
    artist = song_info["artist"]
    album = song_info["album"]
    release_date = song_info["release_date"]
    
    # 줄바꿈을 마크다운 형식으로 반영
    lyrics_lines = song_info["lyrics"].split("\n")
    formatted_lyrics = "\n".join([line.strip() + "  " for line in lyrics_lines if line.strip()])

    # 포스트 제목 포맷 변경
    post_title = f"{title}-{artist}_{instrument} 악보 PDF 다운로드"

    youtube_embed = f'<iframe width="560" height="315" src="{youtube_url.replace("watch?v=", "embed/")}" frameborder="0" allowfullscreen></iframe>'
    download_button = f'<p><a href="{filename}" download><strong>📥 Download Sheet Music</strong></a></p>'

    return f"""---
layout: post
title: {post_title}
date: {now}
categories: sheet music
---

{youtube_embed}

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

# 사용자 입력 받기
melon_url = input("멜론 곡 URL을 입력하세요: ").strip()
youtube_url = input("YouTube URL을 입력하세요: ").strip()
filename = input("악보 파일 경로 또는 링크를 입력하세요 (예: /downloads/song.pdf 또는 Gumroad 링크): ").strip()
instrument = input("악기 파트를 입력하세요 (예: Piano, Violin): ").strip()

# 곡 정보 가져오기
song_info = get_song(melon_url)

# 날짜 포함된 파일명 생성
today = datetime.now().strftime("%Y-%m-%d")
safe_title = song_info['title'].replace(" ", "_")
safe_instrument = instrument.replace(" ", "_")
output_filename = f"{today}-{safe_title}_{safe_instrument}_악보_pdf_다운로드.md"

# 마크다운 생성
markdown_content = make_markdown(melon_url, youtube_url, filename, instrument)

# 저장
with open(output_filename, "w", encoding="utf-8") as f:
    f.write(markdown_content)

print(f"{output_filename} 로 저장되었습니다.")
