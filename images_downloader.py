import os
import requests
import json
from tqdm import tqdm


def url_ok(url):
    try:
        response = requests.head(url)

        if response.status_code == 200:
            return True
        else:
            return False

    except requests.ConnectionError as e:
        return e


def download_image(url, save_directory):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

        # Extract the image file name from the URL
        filename = os.path.join(save_directory, os.path.basename(url))

        # Save the image data to a local file
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Image downloaded successfully: {filename}")

    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request exception occurred: {e}")
    except IOError as e:
        print(f"IO error occurred: {e}")


final_folder = "/home/Wolverine/Documents/images"


if __name__ == "__main__":
    json_path = "/home/Wolverine/Documents/json_files/analytics_numberplateevent_urls_3rdAug.json"

    with open(json_path, "r") as f:
        data = json.load(f)
        # print(data[0])

    data = [d for d in tqdm(data) if not url_ok(d["plate_img_url"])]

    for dir in tqdm(data):
        plate_url = dir["plate_img_url"]
        frame_url = dir["frame_img_url"]
        img_name = os.path.basename(frame_url)

        if os.path.exists(os.path.join(final_folder, img_name)):
            print(os.path.join(final_folder, img_name))
            continue

        download_image(frame_url, final_folder)
