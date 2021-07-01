"""A video playlist class."""
from .video import Video

class Playlist:
    """A class used to represent a Playlist."""
    def __init__(self, playlist_title: str):
        self._title = playlist_title
        self._list = []

    def add_video(self, video_object, playlist_title):
        # Takes in arg 'playlist_title' to ensure that the title 
        # remains the same as input
        if video_object in self._list:
            print("Cannot add video to " + playlist_title + ": Video already added")
            return 0
        else:
            print("Added video to " + playlist_title + ": " + video_object.title)
            self._list.append(video_object)
            return self._list

    def remove_video(self, video_object):
        self._list.remove(video_object)
        return self._list

    @property
    def title(self) -> str:
        return self._title

    @property
    def videos(self) -> list:
        return self._list

