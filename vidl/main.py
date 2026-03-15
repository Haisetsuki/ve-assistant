import yt_dlp
from datetime import datetime


def main():
    print("YT-DLP (Prototype Ver.0.0.1)")

    # Get URL
    url = input("Enter the URL: ").strip()
    if not url:
        print("URL cannot be empty. Exiting.")
        return

    # Select File Type
    print("\nSelect File Type:")
    print("1) mp4 (Video)")
    print("2) mkv (Video)")
    print("3) mp3 (Audio Only)")
    print("4) m4a (Audio Only)")
    type_choice = input("Select a number (Default: 1): ").strip()

    type_map = {"1": "mp4", "2": "mkv", "3": "mp3", "4": "m4a"}
    file_type = type_map.get(type_choice, "mp4")

    # Initialize variables for video settings
    resolution = "1080"

    # Only ask for resolution if it's a video format
    if file_type in ["mp4", "mkv"]:
        # Select Resolution
        print("\nSelect Resolution:")
        print("1) 1080p")
        print("2) 720p")
        print("3) 480p")
        print("4) 360p")
        res_choice = input("Select a number (Default: 1): ").strip()

        res_map = {"1": "1080", "2": "720", "3": "480", "4": "360"}
        resolution = res_map.get(res_choice, "1080")

    # Filename Formatting (source-datetime)
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # %(extractor)s pulls the source name (e.g., 'youtube', 'tiktok', 'twitter')
    output_template = f"%(extractor)s-{current_time}.%(ext)s"

    # Configure yt-dlp options based on inputs
    ydl_opts = {
        "outtmpl": output_template,
        "quiet": False,
        "no_warnings": False,
    }

    if file_type in ["mp3", "m4a"]:
        # Audio-only settings
        ydl_opts["format"] = "bestaudio/best"
        ydl_opts["postprocessors"] = [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": file_type,
                "preferredquality": "192",
            }
        ]
    else:
        # Video settings (always includes sound)
        # We added [vcodec^=avc] to force the widely compatible H.264 codec
        ydl_opts["format"] = (
            f"bestvideo[vcodec^=avc][height<={resolution}]+bestaudio[ext=m4a]/best[height<={resolution}]"
        )

    # Execute the Download
    print(f"\nStarting download for {url}...")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("\nDownload completed successfully!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")


if __name__ == "__main__":
    main()
