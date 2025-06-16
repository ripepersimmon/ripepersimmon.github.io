from autoblog import get_user_input, get_song, generate_filename, make_markdown, save_markdown
import logging
import os

def main():
    melon_url, youtube_url, filename, instrument = get_user_input()
    song_info = get_song(melon_url)
    if not song_info:
        logging.error("곡 정보를 가져오지 못했습니다. URL을 확인하세요.")
        exit(1)
    output_filename = generate_filename(song_info, instrument)
    # _posts 디렉터리로 경로 지정
    posts_dir = os.path.join(os.path.dirname(__file__), '..', '_posts')
    os.makedirs(posts_dir, exist_ok=True)
    output_path = os.path.join(posts_dir, output_filename)
    markdown_content = make_markdown(song_info, youtube_url, filename, instrument)
    save_markdown(output_path, markdown_content)

if __name__ == "__main__":
    main()
