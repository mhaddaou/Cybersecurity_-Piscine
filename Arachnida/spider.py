# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    learn.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mhaddaou <mhaddaou@student.1337.ma>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/13 02:43:12 by mhaddaou          #+#    #+#              #
#    Updated: 2024/04/13 02:43:13 by mhaddaou         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

#!/usr/bin/env python3

import requests
import sys
from bs4 import BeautifulSoup
import signal
import os




def get_url():
    return sys.argv[1]

def handler_signal(signal , frame):
    raise TimeoutError()

def check_server_is_work():
    try:
        signal.signal(signal.SIGALRM, handler_signal)
        signal.alarm(3)
        res = requests.get(get_url())
        signal.alarm(0)
        if res.status_code == 200:
            return res
    except requests.exceptions.RequestException as e:
        print(e)

def __recursivly__scraping(parser_html):
    links = parser_html.find_all('a')
    for link in links:
        print(link.get('href'))

def __save__images(img_url, img_res):
    
    # Extract the filename from the URL
    img_filename = os.path.join('images', os.path.basename(img_url))
    with open(img_filename, 'wb') as f:
        f.write(img_res.content)

def extract_images(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    img_tags = soup.find_all('img')
    for img_tag in img_tags:
        img_url = img_tag.get('src')
        if img_url:
            img_res = requests.get(img_url, timeout=5)
            if(img_res.status_code == 200):
                #create folder if it doesn't exist
                if not os.path.exists('images'):
                    os.makedirs('images')
                __save__images(img_url, img_res)
                __recursivly__scraping(soup)


response = check_server_is_work()
if (response):
    extract_images(response.text)