import requests
import random
import os
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse


class ImageDownloader:
    """A class to download images from a given URL."""
    CHUNK_SIZE = 8192  # optimal chunk size for data transfer 8192
    
    def __init__(self, url: str, name: Optional[str] = None, folder_name: Optional[str] = None, extension = ".jpg"):
        self.url = url
        self.name = name or self.generate_image_name(url)
        self.folder_name = folder_name
        self.extension = extension
        self.save_path = self.construct_save_path()
        self.download_image()

    @staticmethod
    def generate_image_name(url: str):
        """Generate image name from URL if not specified."""
        return urlparse(url).path.split("/")[-1] or f"image_{random.randint(10,1000)}"

    def construct_save_path(self):
        """Construct the save path based on the folder and name info."""
        base_dir = Path(os.getcwd())
        if self.folder_name:
            base_dir /= self.folder_name
            base_dir.mkdir(parents=True, exist_ok=True)
        return base_dir / f"{self.name}{self.extension}"

    def download_image(self):
        """Download the image from the URL and save to the target path."""
        try:
            response = requests.get(self.url, stream=True)
            response.raise_for_status()
            with open(self.save_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=self.CHUNK_SIZE):
                    file.write(chunk)
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")


    

# Example -> 
if __name__ == '__main__':
    url = "https://images.unsplash.com/photo-1565945985125-a59c660a9932?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxjb2xsZWN0aW9uLXBhZ2V8MXwxODEzNDg1OHx8ZW58MHx8fHx8&w=1000&q=80"
    print(ImageDownloader(url,"hey!"))





