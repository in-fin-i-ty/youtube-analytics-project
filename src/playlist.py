from src.channel import Channel
import datetime
import isodate


class PlayList:
    """
    Класс инициализирующий ID видео, выдающий атрибуты:
    Название видео и ссылку на видео
    """

    def __init__(self, playlist_id):
        youtube = Channel.get_service()
        playlist_request = youtube.playlists().list(
            part='snippet',
            id=playlist_id,
            maxResults=50
        )
        playlist_response = playlist_request.execute()
        self.playlist_id = playlist_id
        self.title = playlist_response['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

    @property
    def total_duration(self):
        """
        Функция возвращающая суммарную длительность плейлиста
        """
        total_duration = datetime.timedelta()
        youtube = Channel.get_service()
        play_list_items_request = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=self.playlist_id,
            maxResults=50
        )
        play_list_times_response = play_list_items_request.execute()
        for item in play_list_times_response['items']:
            video_id = item['contentDetails']['videoId']
            youtube = Channel.get_service()
            video_request = youtube.videos().list(
                part='contentDetails',
                id=video_id
            )
            video_response = video_request.execute()
            video_duration_timedelta = isodate.parse_duration(video_response['items'][0]
                                                              ['contentDetails']['duration'])
            total_duration += video_duration_timedelta
        return total_duration

    def show_best_video(self):
        """
        Функция выводящая ссылку на самое популярное виде из плейлиста (по количеству лайков)
        """
        youtube = Channel.get_service()
        play_list_items = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=self.playlist_id,
            maxResults=50
        )
        play_list_items_response = play_list_items.execute()

        top_likes = 0

        for item in play_list_items_response['items']:
            video_id = item['contentDetails']['videoId']
            youtube = Channel.get_service()
            video_request = youtube.videos().list(
                part='statistics',
                id=video_id
            )
            video_response = video_request.execute()
            if int(video_response['items'][0]['statistics']['likeCount']) > top_likes:
                top_likes = int(video_response['items'][0]['statistics']['likeCount'])
                best_video: str = f'https://youtu.be/{video_id}'
        return best_video
