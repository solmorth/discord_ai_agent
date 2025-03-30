import yt_dlp
import requests


class YouTube:
    def __init__(self, url):
        self.url = url
        self.options = {
            "quiet": True,  # Suppress unnecessary output
            "skip_download": True,  # Do not download the video
        }
        self.ytdlp = yt_dlp.YoutubeDL()

    def get_subtitles(self):
        """
        Fetch subtitles for the given YouTube URL.
        """
        try:
            info = self.ytdlp.extract_info(self.url, download=False)
            if "subtitles" in info and info["subtitles"]:
                for lang, subs in info["subtitles"].items():
                    if lang == "en":
                        sub = subs[0]
                        sub_url = sub["url"].replace(sub["ext"], "srt")
                        sub_text = requests.get(sub_url).text
                        return sub_text
            else:
                return None
        except Exception as e:
            return f"An error occurred: {e}"
