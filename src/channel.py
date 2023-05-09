import json
import os
from googleapiclient.discovery import build


class Channel:
    __api_key: str = os.getenv('API_KEY')
    """
    Класс для ютуб-канала
    """

    def __init__(self, channel_id: str) -> None:
        """
        Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API
        """
        self.__channel_id = channel_id
        youtube = Channel.get_service()
        self.channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = self.channel.get('items')[0].get('snippet').get('title')
        self.description = self.channel.get('items')[0].get('snippet').get('description')
        self.url = f'https://www.youtube.com/channel/{self.__channel_id}'
        self.subscriberCount = int(self.channel.get('items')[0].get('statistics').get('subscriberCount'))
        self.video_count = self.channel.get('items')[0].get('statistics').get('videoCount')
        self.viewCount = self.channel.get('items')[0].get('statistics').get('viewCount')

    def __str__(self):
        """
        Выводит для пользователя название канал и URL
        return: Название канала (URL)
        """
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        """
        Метод суммирующий количество подписчиков 2х каналов
        return: True or False
        """
        return self.subscriberCount + other.subscriberCount

    def __sub__(self, other):
        """
         Метод вычитающий количество подписчиков 2х каналов
         return: True or False
        """
        return self.subscriberCount - other.subscriberCount

    def __gt__(self, other):
        """
        Метод сравнивающий "больше" количество подписчиков 2х каналов
        return: True or False
        """
        return self.subscriberCount > other.subscriberCount

    def __ge__(self, other):
        """
        Метод сравнивающий "больше или равно" количество подписчиков 2-х каналов
        return: True or False
        """
        return self.subscriberCount >= other.subscriberCount

    def __lt__(self, other):
        """
        Метод сравнивающий "меньше" количество подписчиков 2х каналов
        return: True or False
        """
        return self.subscriberCount < other.subscriberCount

    def __le__(self, other):
        """
        Метод сравнивающий "меньше или равно" количество подписчиков 2-х каналов
        return: True or False
        """
        return self.subscriberCount <= other.subscriberCount

    def __eq__(self, other):
        """
        Метод сравнивающий количество подписчиков 2х каналов
        return: True or False
        """
        return self.subscriberCount == other.subscriberCount

    @property
    def channel_id(self):
        return self.__channel_id

    @channel_id.setter
    def channel_id(self, channel_id):
        """
        Сеттер возвращающий ошибку при попытке изменить название канала
        """
        raise AttributeError("property 'channel_id' of 'Channel' object has no setter")

    @classmethod
    def get_service(cls):
        """
        Класс-метод возвращающий объект для работы YouTube API
        """
        youtube = build('youtube', 'v3', developerKey=Channel.__api_key)
        return youtube

    def print_info(self) -> None:
        """
        Выводит в консоль информацию о канале
        """
        channel = self.channel.channels().list(id=self.__channel_id, part="snippet,statistics").execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    def to_json(self, files):
        """
        Функция для записи полученных данных в Json файл
        """
        data = {
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscribers': self.subscriberCount,
            'count videos': self.video_count,
            'total views': self.viewCount
        }
        with open(files, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent='\t')
