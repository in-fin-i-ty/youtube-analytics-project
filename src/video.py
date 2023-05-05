import os
from googleapiclient.discovery import build


class Video:
    """
    Класс инициализирующий реальными данными атрибуты:
    - id видео
    - название видео
    - ссылка на видео
    - количество просмотров
    - количество лайков
    """
    def __init__(self, video_id: str) -> None:
        self.video_id = video_id
        api_key: str = os.getenv('API_KEY')
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                    id=video_id).execute()
        self.video_title = video_response['items'][0]['snippet']['title']
        self.view_count = video_response['items'][0]['statistics']['viewCount']
        self.like_count = video_response['items'][0]['statistics']['likeCount']
        self.comment_count = video_response['items'][0]['statistics']['commentCount']
        self.url = f'https://www.youtube.com/video/{self.video_id}'

    def __str__(self):
        """
        Функция вывода для пользователя названия канала
        """
        return f"{self.video_title}"


class PLVideo(Video):
    """
    Дочерний класс класса Video инициализирующий реальными данными атрибуты:
    - id видео
    - название видео
    - ссылка на видео
    - количество просмотров
    - количество лайков
    - id плейлиста
    """
    def __init__(self, video_id, playlist_id: str):
        super().__init__(video_id)
        self.playlist_id = playlist_id
        self.playlist_videos = self.youtube.playlistItems().list(playlistId=playlist_id, part='contentDetails',
                                                                 maxResults=50).execute()
