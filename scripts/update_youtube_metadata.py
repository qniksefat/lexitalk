from pytube import Playlist, YouTube
import csv

def dump_urls_to_file(playlist_url, file_path):
    playlist = Playlist(playlist_url)
    with open(file_path, "w") as f:
        for url in playlist:
            f.write(url + "\n")

def read_csv_file(file_path):
    set_urls = set()
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            set_urls.add(row["url"])
    return set_urls

yt_url_prefix = "https://www.youtube.com/watch?v="

def get_video_info(video_url):
    try:
        yt = YouTube(video_url)
        return {
            "title": yt.title,
            "views": yt.views,
            "length": yt.length,
            "video_id": yt.video_id,
            "publish_date": yt.publish_date,
            "url": yt_url_prefix + yt.video_id,
        }
    except Exception as e:
        print(f"An error occurred with url: {video_url}, error: {str(e)}")
        return None

def append_video_info_to_csv(video_info, file_path):
    with open(file_path, "a") as f:
        writer = csv.DictWriter(
            f, fieldnames=["title", "views", "length", "video_id", "publish_date", "url"])
        writer.writerow(video_info)


if __name__ == "__main__":
    
    playlist_url = "https://www.youtube.com/playlist?list=UULFSHZKyawb77ixDdsGog4iWA"
    urls_file_path = "data/youtube_playlist/urls.txt"
    csv_file_path = "data/youtube_playlist/videos.csv"

    # Step 1: Dump URLs from playlist to a file
    dump_urls_to_file(playlist_url, urls_file_path)

    # Step 2: Read CSV file and create a set of URLs
    set_urls = read_csv_file(csv_file_path)

    # Step 3: Get video info for URLs not in the set and append to CSV file
    with open(urls_file_path, "r") as f:
        urls = f.readlines()

    for url in urls:
        url = url.strip()
        if url not in set_urls:
            print(f"Processing url: {url}")
            video_info = get_video_info(url)
            if video_info:
                append_video_info_to_csv(video_info, csv_file_path)
