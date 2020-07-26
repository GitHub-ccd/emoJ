#!/usr/bin/env python

# standalone script to make set of quries to scrape images for 7 main 
# emotinos for google.images. Google images is limited within the same IP. Thus, 
# use VPN to make seraches from different regions to get different set of images. 
# 
import time
import json
from selenium import webdriver
import os
import sys
import io
from PIL import Image
import requests
import hashlib
import numpy as np

# This is the path I use
DRIVER_PATH = './chromedriver.exe'
# Put the path for your ChromeDriver here
wd = webdriver.Chrome(executable_path=DRIVER_PATH)

def fetch_image_urls(query: str, max_links_to_fetch: int, wd: webdriver, sleep_between_interactions: int = 1):
    """
	This will push a quary to google web driver, traverse through the page at each image click one image at a time 
	and fetch urls for each of the images
	"""
	def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)

    # build the google query
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img&tbs=isz%3Al"
    print(search_url)
    # load the page
    wd.get(search_url.format(q=query))

    image_urls = set()
    image_count = 0
    results_start = 0
    while image_count < max_links_to_fetch:
        scroll_to_end(wd)

        # get all image thumbnail results
        try:
            thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
        except Exception:
            continue
        number_results = len(thumbnail_results)

        print(f"Found: {number_results} search results on {query}. "
              f"Extracting links from {results_start}:{number_results}")

        for img in thumbnail_results[results_start:number_results]:
            # try to click every thumbnail such that we can get the real image behind it
            try:
                img.click()
                time.sleep(sleep_between_interactions)
            except Exception:
                continue

            # extract image urls
            try:
                actual_images = wd.find_elements_by_css_selector('img.n3VNCb')
            except Exception:
                continue

            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))

            image_count = len(image_urls)

            if len(image_urls) >= max_links_to_fetch:
                print(f"Found: {len(image_urls)} image links on {query}, done!")
                break
        else:
            print("Found:", len(image_urls),
                  "image links, looking for more ...")
            time.sleep(np.random.randint(27, 35, dtype=int))
            try:
                load_more_button = wd.find_element_by_css_selector(".mye4qd")
            except Exception:
                continue

            if load_more_button:
                wd.execute_script("document.querySelector('.mye4qd').click();")

        # move the result startpoint further down
        results_start = len(thumbnail_results)

    return image_urls



def persist_image(folder_path: str, url: str):
	"""
	read and save image. both exceptions are handeled.
	"""
    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        file_path = os.path.join(folder_path, hashlib.sha1(
            image_content).hexdigest()[:10] + '.png')
        with open(file_path, 'wb') as f:
            image.save(f, 'PNG', compress_level=0, optimize=False)
        print(f"SUCCESS - saved {url} - as {file_path}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")


def search_and_download(search_term: str, driver_path: str,  number_images=int, target_path='./images', image_directory='unknown'):
    """
	Target path is set and directories are created if needed. The webdriver is called at regular intervals 
	as randomly set by the x. Regular calls for continuous requests will be blocked by the server. Recommend changing random number 
	regularly or each time running the script. 
	"""
	target_folder = os.path.join(
        target_path, image_directory)

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    with webdriver.Chrome(executable_path=driver_path) as wd:
        X = np.array([0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
        index = np.random.choice(X.shape[0], 1, replace=False)
        res = fetch_image_urls(search_term, number_images,
                               wd=wd, sleep_between_interactions=X[index].item(0))
    search_term = search_term.replace(' ', '_')
    for elem in res:
        persist_image(target_folder, elem)


def construct_query(emotion):
    """Maps the emotion to the optimal query

    The Google Images query for most emotion keywords will be "<emotion> human face".
    For a few exceptions, the optimal query is different.

    Parameters
    ----------
    emotion: str

    Returns
    -------
    query: str
    """
    exceptions = ['disgusted', 'grossed_out', 'resentful', 'elated']
    if emotion in exceptions:
        query = f'{emotion} face'
    else:
        query = f'{emotion} human face'
    return query


def get_emotions():
	"""
	Main funtion. The emotions dictionary defines the specific quaries and similar 
	keywords for a given emotion. Target path should be set accordingly
	"""
    num_images = 1
    target_path = './images'

    emotions = {'angry': ['angry', 'furious', 'resentful', 'irate'],
                'disgust': ['disgusted', 'repugnant', 'sour', 'grossed out'],
                'fear': ['fear', 'terror', 'fright', 'horror', 'dread'],
                'happy': ['happy', 'smiling', 'cheerful', 'elated', 'joyful'],
                'sad': ['sad', 'sorrowful', 'mournful', 'grieving', 'crying'],
                'surprise': ['surprised', 'astonished', 'shocked', 'amazed'],
                'neutral': ['neutral','unreadable', 'poker-faced', 'emotionless', 'inexpressive']}

    for emotion_label, keywords in emotions.items():
        image_directory = emotion_label
        for k in keywords:
            query = construct_query(k)
            search_and_download(query, DRIVER_PATH, num_images, target_path, image_directory)


if __name__ == '__main__':
	get_emotions()
