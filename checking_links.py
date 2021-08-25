"""
   Purpose of script: Get all links from website, and then check that they all
   work. Only surface those that need to be checked manually.

    --- Step 0:
        Create virtual env: "env-links", activate it, and install packages:
        pip3 install -r requirements.txt

    --- Step 1: After virtual env is created:
        cd Documents/Consulting/Website/
        source Envs/env-links/bin/activate
        python3 checking_links.py
"""

import urllib.parse

from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
import requests


WEBSITE_URL = ["https://www.ikukuyeva.com"] 


def remove_google_redirect_from_url(webpage):
    if  (webpage.startswith("http://www.google.com/url?q=") | 
         webpage.startswith("https://www.google.com/url?q=")):
        # Extract original URL, without Google's redirect links. This is because
        # if it's webpage that's getting Google's redirect for tracking, we need
        # to check actual webpage getting redirect to; otherwise if the page is 
        # not loading, it will look like it is because of the redirct.

        # Start of redirect:
        webpage = webpage.replace("http://www.google.com/url?q=", "")
        webpage = webpage.replace("https://www.google.com/url?q=", "")
        index_end_redirect = webpage.find("&sa=D")
        webpage = webpage[:index_end_redirect]

        # Convert any symbols in URL to working URL:
        webpage = urllib.parse.unquote(webpage)
    return webpage


def get_all_urls_on_page(webpage):
    resp = requests.get(webpage)
    # Note: Content of page is in: resp.content

    # Parse website with Beautiful Soup, per
    # https://stackoverflow.com/questions/1080411/retrieve-links-from-web-page-using-python-and-beautifulsoup
    html_encoding = EncodingDetector.find_declared_encoding(resp.content,
                                                            is_html=True)
    soup = BeautifulSoup(resp.content,
                         from_encoding=html_encoding,
                         features="html.parser")

    url_list = []
    for link in soup.find_all('a', href=True):
        if link['href'] != "#ContactMe":
            url_list.append(link['href'])

        # Remove duplicates:
    url_list = list(set(url_list))
    url_list = [ link for link in url_list if link[0] != "#" ]
    return url_list


def get_webpage_status(webpage):
    """Check that web page exists/load."""
    try:
        # Parsing requests output, per:
        # https://stackoverflow.com/questions/16778435/python-check-if-website-exists
        request = requests.get(webpage)
        if request.status_code != 200:
            return request.status_code
    except requests.exceptions.SSLError:
            return -99
    except requests.exceptions.MissingSchema:
            return -99


if __name__ == '__main__':
    # --- Step 1: Get all links from website
    #
    for site_url in WEBSITE_URL:
        print(f"--- Step 1: Starting process to check website links for {site_url}.")
        links_list = get_all_urls_on_page(site_url)

    print(f"""    There are {len(links_list)} links on website.""")
    print()
    
    # --- Step 2: Check that all the links still work, and print out those
    #             that do not for a manual check.
    #
    print(""""--- Step 2: We're now checking that they all work:""")
    for index, url in enumerate(links_list):
        # Check all links on page:
        if url[0] == '/':
            url = site_url + url
        else:
            # Check if there's a Google redict to URL and remove it, if exists:
            url = remove_google_redirect_from_url(url)
        print(f"    {index}. Checking URL: {url}")    
        url_status = get_webpage_status(url)
        if url_status == -99:
            print(f"Error in loading url: {url}")
        else:
            url_links_list = get_all_urls_on_page(url)
            # Ignore those that pertain to main webiste that we already checked:
            url_links_list = [ sub_url for sub_url in url_links_list if sub_url[0] != "/" ]
            print(f"        There are {len(url_links_list)} links on the page.")    
            if url_links_list:
                for sub_url in url_links_list:
                    url_status = get_webpage_status(sub_url)
                    if url_status == -99:
                        print(f"Error in loading url: {sub_url}")
    print("--- Process complete.")
    print()
