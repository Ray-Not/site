import os
from urllib.parse import urlparse

import requests
from django.conf import settings
from django.core.management.base import BaseCommand

from web.models import Door


class Command(BaseCommand):
    help = 'Загружает все медиа с ссылок'

    def handle(self, *args, **kwargs):
        media_dir = settings.MEDIA_ROOT
        if not os.path.exists(media_dir):
            os.makedirs(media_dir)

        doors = Door.objects.all()

        for door in doors:
            print(f"Processing door: {door.title}")

            door_dir = os.path.join(media_dir, f"doors/{door.slug or door.id}")
            if not os.path.exists(door_dir):
                os.makedirs(door_dir)

            print(door.images)
            image_urls = [
                url.strip() for url in door.images.split(',') if url.strip()
            ]
            saved_images = []

            for url in image_urls:
                image_path = download_image(url, door_dir)
                if image_path:
                    relative_media_path = os.path.relpath(
                        image_path,
                        settings.MEDIA_ROOT
                    )
                    saved_images.append(relative_media_path)

            if saved_images:
                door.images = ','.join(saved_images)
                door.save()
                print(door.images)
                print(f"Updated images for door: {door.title}")


def download_image(url, save_dir):
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    file_path = os.path.join(save_dir, filename)

    if os.path.exists(file_path):
        print(f"Image already exists: {file_path}")
        return file_path

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f"Image downloaded: {file_path}")
            return file_path
        else:
            print(
                f"Failed to download {url}: Status code {response.status_code}"
            )
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return None
