import os
import re
import frontmatter
import logging
from melon import get_song
from autoblog import download_album_art
import requests
from dotenv import load_dotenv

# codes/.env 파일 명시적 로드
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

def update_post_metadata(md_path):
    post = frontmatter.load(md_path)
    # 기존 정보 추출
    title = post.get('title', '')
    date = post.get('date', '')
    instrument = ''
    melon_url = ''
    # 제목에서 악기 추출 (예: ..._드럼 악보 PDF 다운로드)
    m = re.search(r'_(.+?) 악보', title)
    if m:
        instrument = m.group(1).strip()
    # melon_url 추출: front matter > 본문(html a태그) > 수동 입력
    if 'melon_url' in post and post['melon_url']:
        melon_url = post['melon_url']
    else:
        # 본문에서 melon_url 추출 (a태그 href)
        melon_url_match = re.search(r'<a href=["\'](https://www.melon.com/song/detail[^"\']+)["\']', post.content)
        if melon_url_match:
            melon_url = melon_url_match.group(1)
        else:
            melon_url = input(f"{md_path}의 멜론 곡 URL을 입력하세요: ").strip()
    song_info = get_song(melon_url)
    if not song_info:
        logging.warning(f"곡 정보를 가져올 수 없음: {melon_url}")
        return
    artist = song_info['artist']
    album = song_info['album']
    album_art_url = song_info.get('album_art')
    image_filename = download_album_art(album_art_url, album, artist) if album_art_url else ''
    # front matter 갱신
    post['image'] = image_filename
    post['tags'] = [artist, instrument]
    post['melon_url'] = melon_url
    # 본문에 원곡 들으러가기 버튼 추가 (이미 있으면 중복 방지)
    listen_btn = f'<p><a href="{melon_url}" target="_blank"><strong>🎧 원곡 들으러가기</strong></a></p>'
    if listen_btn not in post.content:
        post.content = listen_btn + '\n' + post.content
    # 본문 내 각 헤더(##, ### 등) 뒤에 adsense.html 광고 삽입
    post.content = re.sub(r'(\n##+ .+?\n)', r'\1\n{% include adsense.html %}\n', post.content)
    # 다운로드 섹션 내 기존 광고 코드 제거 후, 다운로드 버튼 아래에만 광고 삽입
    post.content = re.sub(r'(## 다운로드\n)(\s*\{\% include adsense.html \%\}\s*\n)?(.*?)(\n\n|\Z)', r'\1\3\n\n{% include adsense.html %}\n', post.content, flags=re.DOTALL)
    # 저장 (date는 그대로)
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(frontmatter.dumps(post))
    print(f"{md_path} 업데이트 완료.")

if __name__ == "__main__":
    posts_dir = os.path.join(os.path.dirname(__file__), '..', '_posts')
    for fname in os.listdir(posts_dir):
        if fname.endswith('.md'):
            update_post_metadata(os.path.join(posts_dir, fname))
