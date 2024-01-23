import pandas as pd


class MetadataSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._generate_dataframe()
        return cls._instance

    def _generate_dataframe(self):
        df = pd.read_csv("data/youtube_playlist/videos.csv")
        df["guest_names"] = df["title"].apply(self._extract_guest_names)
        df["episode_title"] = df["title"].apply(self._extract_episode_title)
        df["views"] = df["views"].astype(str)
        df["length"] = df["length"].astype(str)
        df["episode_number"] = df["title"].apply(self._extract_episode_number)
        df = df.set_index("episode_number")
        self.metadata_yt = df

    def _extract_guest_names(self, title):
        if ":" in title:
            return title.split(":")[0]
        else:
            return ""

    def _extract_episode_number(self, title):
        # "Ask Me Anything (AMA)" episodes have "#" but not conventional episode numbers
        if "AMA" not in title and "#" in title:
            return str(int(title.split("#")[1]))    # remove leading zeros
        else:
            return None

    def _extract_episode_title(self, title):
        if "|" in title:
            episode_title = title.split("|")[0].strip()
            if ":" in episode_title:
                return episode_title.split(":")[1].strip()
            else:
                return episode_title
        else:
            # Handle case where "|" is not present
            return ""


metadata_singleton = MetadataSingleton()
metadata_yt = metadata_singleton.metadata_yt
