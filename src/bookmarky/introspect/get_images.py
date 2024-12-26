"""
    Bookmarky Introspect
    Introspect
    Get Images

"""
import logging.config

from bs4 import BeautifulSoup
import requests

from polite_lib.utils import date_utils

from bookmarky.api.utils import db
from bookmarky.api.utils import glow
from bookmarky.api.collects.bookmarks import Bookmarks
from bookmarky.shared.utils.log_config import log_config


logging.config.dictConfig(log_config)
logger = logging.getLogger(__name__)
logger.propagate = True

image_store_loc = glow.general["IMAGE_DIR"]
user_agents = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.7; rv:131.0) Gecko/20100101 Firefox/131.0"
]


class GetImages:

    def __init__(self):
        self.b_col = Bookmarks()

    def run(self) -> bool:
        """Primary entrypoint"""
        print("run")
        self.get_bookmarks_without_images()
        return True

    def get_bookmarks_without_images(self):
        bookmarks = self.b_col.get_entities_without_meta_key("featured_image")
        # bookmarks = self.b_col.get_by_ids([260, 277])
        logging.info("Found %s bookmarks without images" % len(bookmarks))
        for bookmark in bookmarks:
            if not self.get_bookmark_image(bookmark):
                bookmark.metas["featured_image_fail"] = date_utils.now()
                bookmark.save()

    def get_bookmark_image(self, bookmark):
        """Get an advertised image for a Bookmark if one exists."""
        if bookmark.url[:12] == "about:reader?":
            logging.warning("Cannot get images for reader urls")
            return False
        try:
            headers = {
                "User-Agent": user_agents[0]
            }
            response = requests.get(
                bookmark.url,
                headers=headers,
            )
        except requests.exceptions.ConnectionError as e:
            logging.error(f"Could not resolve Bookmark {bookmark} URL: {bookmark.url}. Error: {e}")
            return False
        except requests.exceptions.InvalidSchema as e:
            logging.error(f"Could not resolve Bookmark {bookmark} URL: {bookmark.url}. Error: {e}")
            return False
        soup = BeautifulSoup(response.text, 'html.parser')
        metas = soup.find_all("meta")
        image_meta_url = None
        for meta in metas:
            if meta.get("property", None) == "og:image":
                image_meta_url = meta.get("content")
                break
        if not image_meta_url:
            logging.warning(f"Could not find a meta image for {bookmark}")
            return False
        else:
            print("\n\n")
            print("Meta Image")
            print(meta)
            print(image_meta_url)
            featured_image = self.store_image(bookmark, image_meta_url)
            if featured_image:
                bookmark.metas["featured_image"] = featured_image
                if bookmark.save():
                    logging.info(f"Saved featued image for: {bookmark}")
                else:
                    logging.error(f"Failed to save featued image for: {bookmark}")
            print("\n\n\n")
            return True

    def store_image(self, bookmark, image_url):
        try:
            # Send a GET request to the URL
            response = requests.get(image_url)
            response.raise_for_status()  # Raise an error for bad responses
            # Get the content type from the response headers
            content_type = response.headers['Content-Type']

            # Determine the file extension based on the content type
            if 'image/jpg' in content_type or 'image/jpeg' in content_type:
                file_extension = 'jpg'
            elif 'image/png' in content_type:
                file_extension = 'png'
            elif 'image/gif' in content_type:
                file_extension = 'gif'
            elif 'image/webp' in content_type:
                file_extension = 'webp'
            elif 'image/bmp' in content_type:
                file_extension = 'bmp'
            else:
                # If none of the types match, raise an error
                raise ValueError(f"Unsupported image type: {content_type}")

            hash_name = str(hash(bookmark.url))
            image_name = f"{hash_name}.{file_extension}"
            # Parse the URL to get the filename
            filename = f"{image_store_loc}/bookmarks/{image_name}"

            # Write the content to a file
            with open(filename, 'wb') as f:
                f.write(response.content)

            print(f"Image downloaded as: {filename}")
            return image_name

        except Exception as e:
            print(f"Error downloading image: {e}")
            return False


if __name__ == "__main__":
    if not db.connect():
        print("Failed database connection, exiting")
        exit(1)
    GetImages().run()


# End File: politeauthority/bookmarky/src/bookmarky/introspect/get_images.py
