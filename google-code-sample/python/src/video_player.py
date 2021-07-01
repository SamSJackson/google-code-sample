"""A video player class."""

from .video_library import VideoLibrary
from .video import Video
from .video_playlist import Playlist
import random


class VideoPlayer:
    """A class used to represent a Video Player."""


    def __init__(self):
        self._video_library = VideoLibrary()
        self.video_playing = {"playing": False, "title": "" , "paused": False, "video_object": ""}
        # Args = [video playing, video title, video paused, video_object] 
        # video_playing initalises at start, ensuring that it is always False on startup
        self.playlist_names = {}
        self.all_videos = sorted((list(self._video_library._videos.keys())))
        self.flagged_videos = {}
        # All video IDs available


    def search_output_print(self, found_videos, isFound, search_term):
        if not isFound:
            print("No search results for " + search_term)
        else:
            print("Here are the results for " + search_term + ":")
            counter = 1
            for video in found_videos:
                    video_object = self._video_library.get_video(video)
                    video_title = video_object.title
                    video_tags = str(' '.join(video_object.tags))
                    print(" " + str(counter) + ") " + video_title + " (" + video + ") [" + video_tags + "]")
                    counter += 1
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            userInput = input()
            if userInput.isnumeric():
                if int(userInput) <= counter:
                    self.play_video(found_videos[int(userInput)-1])

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        # All videos in library, from function
        videos = self._video_library.get_all_videos() # All video objects
        videoDict = {}
        for video_object in videos:
            # Made new dictionary with video title as key (easy to sort)
            videoDict[video_object.title] = [video_object.video_id, video_object.tags]
        videoDict = dict(sorted(videoDict.items()))
        # Sorting of dictionary
        print("Here's a list of all available videos:")
        for element in videoDict:
            video_id = videoDict[element][0]
            video_tags = ' '.join(videoDict[element][1])
            if video_id in self.flagged_videos:
                print(" " + element + " (" + videoDict[element][0] + ") [" + str(video_tags) + "] - FLAGGED " + self.flagged_videos[video_id] + "")
            else:
                print(" " + element + " (" + videoDict[element][0] + ") [" + str(video_tags) + "]")
            # This is just so string appears appropriately.

    
    def play_video(self, video_id):
        
        video_object = self._video_library.get_video(video_id)
        if video_object == None: # get_video returns None if no such video_id exists
            print("Cannot play video: Video does not exist")
        elif video_id in self.flagged_videos:
            print("Cannot play video: " + "Video is currently flagged " + self.flagged_videos[video_id])
        else:
            if not self.video_playing["playing"]:
                # Checks if file is already playing
                print("Playing video: " + video_object.title)
                self.video_playing["playing"] = True # File is now playing
                self.video_playing["video_object"] = video_object # object of video
            else:
                print("Stopping video: " + self.video_playing["title"]) 
                print("Playing video: " + video_object.title)
                # video_playing[0] does not change boolean value, always playing here

            self.video_playing["video_object"] = video_object
            self.video_playing["paused"] = False
            self.video_playing["title"] = video_object.title


    def stop_video(self):
        if self.video_playing["playing"]:
            print("Stopping video: " + self.video_playing["title"])
            self.video_playing["playing"] = False
            self.video_playing["title"] = ''
            self.video_playing["video_object"] = '' 
        else:
            print("Cannot stop video: No video is currently playing")
        # Stops the current video.

    def play_random_video(self):
        if len(self.flagged_videos) == len(self._video_library.get_all_videos()):
            print("No videos available")
        else:
            video_objects = self._video_library.get_all_videos()
            random_video = random.choice(video_objects) # Picking random video
            self.play_video(random_video.video_id) # Calling earlier function with video_id

    def pause_video(self):
        if self.video_playing["playing"]: # If video playing
            if not self.video_playing["paused"]: # If video not paused
                print("Pausing video: " + self.video_playing["title"])
                self.video_playing["paused"] = True
                # video_playing = [True, video_title, True] same as
                # video_playing = [video playing, title, paused]
            else: 
                print("Video already paused: " + self.video_playing["title"])

        else:
            print("Cannot pause video: No video is currently playing")

    def continue_video(self):    
        if self.video_playing["paused"]:
            # If video_playing = [video playing, title, paused]
            print("Continuing video: " + self.video_playing["title"])
            self.video_playing["paused"] = False
        else:
            if self.video_playing["playing"]:
                # if video playing but not paused
                print("Cannot continue video: Video is not paused")
            else:
                # if no video playing
                print("Cannot continue video: No video is currently playing")
        

    def show_playing(self):
        # Need to be able to get information on video
        # Got information on self.video_playing["paused"]
        if self.video_playing["playing"]:
            video_object = self.video_playing["video_object"]
            video_id = video_object.video_id
            video_tags = ' '.join(video_object.tags)
            
            if not self.video_playing["paused"]:
                print("Currently playing: " + self.video_playing["title"] + " (" + video_id + ") [" + str(video_tags) + "]")
                # print(" " + element + " (" + str(videoDict[element][0]) + ") [" + str(video_tags) + "]")
            elif self.video_playing["paused"]:
                print("Currently playing: " + self.video_playing["title"] + " (" + video_id + ") [" + str(video_tags) + "] - PAUSED" )
        else:
            print("No video is currently playing")

    def create_playlist(self, playlist_name):
        if playlist_name.lower() in self.playlist_names:
            print("Cannot create playlist: A playlist with the same name already exists")
        else:
            self.playlist_names[playlist_name.lower()] = Playlist(playlist_name)
            print("Successfully created new playlist: " + self.playlist_names[playlist_name.lower()].title)


    def add_to_playlist(self, playlist_name, video_id):
        
        if playlist_name.lower() not in self.playlist_names:
            print("Cannot add video to " + playlist_name + ": Playlist does not exist")
        else:
            if video_id not in self.all_videos:
                # Video name not valid/found
                print("Cannot add video to " + playlist_name + ": Video does not exist")
            elif video_id in self.flagged_videos:
                print("Cannot add video to " + playlist_name + ": " + "Video is currently flagged " + self.flagged_videos[video_id])
            else:
                keyName = playlist_name.lower()
                # Easier to read, adding this variable.
                video_object = self._video_library.get_video(video_id)
                self.playlist_names[keyName].add_video(video_object, playlist_name)


    def show_all_playlists(self):
        if len(self.playlist_names) == 0:
            print("No playlists exist yet")
        else:
            self.playlist_names = dict(sorted(self.playlist_names.items()))
            # Sorting dictionary keys in lexicographical order (alpahebetical + numbers)
            print("Showing all playlists:")
            for playlist in self.playlist_names:
                print(" " + self.playlist_names[playlist].title)

    def show_playlist(self, playlist_name):
        # Display all contents of playlist (provided it exists)
        if playlist_name.lower() not in self.playlist_names:
            print("Cannot show playlist " + playlist_name + ": Playlist does not exist")
        else:
            keyName = playlist_name.lower()
            print("Showing playlist: " + playlist_name)
            playlist_videos = self.playlist_names[keyName].videos
            # 
            if len(playlist_videos) == 0:
                print(" No videos here yet")
            else:
                for video_object in (playlist_videos):
                    video_id = video_object.video_id
                    video_tags = str(' '.join(video_object.tags))
                    if video_id in self.flagged_videos:
                        print(" " + video_object.title + " (" + video_id + ") [" + video_tags + "] - FLAGGED " + self.flagged_videos[video_id] + "")
                    else:
                        print(" " + video_object.title + " (" + video_id + ") [" + video_tags + "]")
        

    def remove_from_playlist(self, playlist_name, video_id):
        keyName = playlist_name.lower()
        if keyName not in self.playlist_names or video_id not in self.all_videos:
            if keyName not in self.playlist_names:
                # notExist is variable for which problem. If problem is playlist
                # playlist, hence, does not exist.
                notExist = "Playlist"
            else:
                notExist = "Video"
            print("Cannot remove video from " + playlist_name + ": " + notExist +" does not exist")       
        else:
            video_object = self._video_library.get_video(video_id)
            if video_object not in self.playlist_names[keyName].videos:
                print("Cannot remove video from " + playlist_name + ": Video is not in playlist")
            else:
                self.playlist_names[keyName].remove_video(video_object)
                print("Removed video from " + playlist_name + ": " + video_object.title)


    def clear_playlist(self, playlist_name):
        keyName = playlist_name.lower()
        if keyName not in self.playlist_names:
            print("Cannot clear playlist " + playlist_name + ": Playlist does not exist")
        else:
            for video in self.playlist_names[keyName].videos:
                # Loops through all videos in playlist (0 loops if no videos)
                self.playlist_names[keyName].remove_video(video)
                # Then removes video from dictionary value
            print("Successfully removed all videos from " + playlist_name)

    def delete_playlist(self, playlist_name):
        keyName = playlist_name.lower()
        if keyName not in self.playlist_names:
            print("Cannot delete playlist " + playlist_name + ": Playlist does not exist")
        else:
            del self.playlist_names[keyName]
            # No error can be caused due to error-checking in line before
            # self.playlist_names[keyName] must exist
            print("Deleted playlist: " + playlist_name)

    def search_videos(self, search_term):
        isFound = False
        found_videos = []
        for video in self.all_videos:
            if video in self.flagged_videos:
                continue
                # If video is a flagged video then it is not checked
                # Loop is skipped
            if search_term.lower() in video:
                found_videos.append(video)
                isFound = True
        # Put into function as simpler, factoring out.
        self.search_output_print(found_videos, isFound, search_term)

    def search_videos_tag(self, video_tag):
        isFound = False
        found_videos = []
        for video in self.all_videos:
            if video in self.flagged_videos:
                continue
                # See lines 254-255
            video_object = self._video_library.get_video(video)
            video_tags = video_object.tags
            if video_tag.lower() in video_tags:
                found_videos.append(video)
                isFound = True
        self.search_output_print(found_videos, isFound, video_tag)


    def flag_video(self, video_id, flag_reason="Not supplied"):
        if video_id not in self.all_videos:
            print("Cannot flag video: Video does not exist")
        elif video_id in self.flagged_videos:
            print("Cannot flag video: Video is already flagged")
        else:
            video_object = self._video_library.get_video(video_id)
            if video_object.title == self.video_playing["title"]:
                # Stops video if the to-be-flagged video is playing
                self.stop_video()
            self.flagged_videos[video_id] = "(reason: " + flag_reason + ")"
            # Add reason to dictionary so that can be accessed in other functions easily
            print("Successfully flagged video: " + video_object.title + " (reason: " + flag_reason + ")")

    def allow_video(self, video_id):
        if video_id not in self.all_videos or video_id not in self.flagged_videos:
            reason_not_allowed = "Video is not flagged" 
            if video_id not in self.all_videos:
                # If video does not exist, reason changes to not existing (takes priority)
                reason_not_allowed = "Video does not exist"
            print("Cannot remove flag from video: " + reason_not_allowed)
        else:
            video_object = self._video_library.get_video(video_id)
            del self.flagged_videos[video_id]
            # self.flagged_videos[video_id] must exist
            # Know this through checking 'if not in self.flagged_videos' earlier
            # See line 292
            print("Successfully removed flag from video: " + video_object.title) 
