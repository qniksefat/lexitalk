import pandas as pd

class MetadataSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._generate_dataframe()
        return cls._instance

    def _generate_dataframe(self):
        df = pd.read_csv("data/youtube_playlist/video_info.csv")
        df["guest_names"] = df["title"].apply(lambda x: x.split(":")[0])
        df["episode_number"] = df["title"].apply(lambda x: x.split("#")[1]).astype(int)
        df["episode_title"] = df["title"].apply(lambda x: x.split("|")[0].strip())
        df["episode_title"] = df["episode_title"].apply(lambda x: x.split(":")[1].strip())
        df["url"] = "https://www.youtube.com/watch?v=" + df["video_id"]
        df = df.set_index("episode_number")
        self.metadata_yt = df

metadata_singleton = MetadataSingleton()
metadata_yt = metadata_singleton.metadata_yt
