### Goal: Get all links from website, and then check that they all work

# --- Step 0:
# Create virtual env: "env-links", activate it, and install packages:
# pip3 install -r requirements.txt

from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
import requests

WEBSITE_URL = "http://www.ikukuyeva.com"


if __name__ == '__main__':
	# --- Step 1: Get all links from website
	#
	print(f"--- Starting process to check website links for {WEBSITE_URL}.")
	resp = requests.get(WEBSITE_URL)
	# Note: Content of page is in: resp.content

	# Parse website with Beautiful Soup, per
	# https://stackoverflow.com/questions/1080411/retrieve-links-from-web-page-using-python-and-beautifulsoup
	html_encoding = EncodingDetector.find_declared_encoding(resp.content,
															is_html=True)
	soup = BeautifulSoup(resp.content,
						 from_encoding=html_encoding,
						 features="html.parser")

	links_list = []
	for link in soup.find_all('a', href=True):
		if link['href'] != "#ContactMe":
			links_list.append(link['href'])

	print(f"""    There are {len(links_list)} links on website. 
	- We're now checking that they all work.
	- Note: any URLs that don't, will be printed below.""")

	# --- Step 2: Check that all the links still work, and print out those
	#             that do not for a manual check.
	#
	for index, url in enumerate(links_list):
		if url[0] == '/':
			url = WEBSITE_URL + url 
		try:
			# Parsing requests output, per:
			# https://stackoverflow.com/questions/16778435/python-check-if-website-exists
			request = requests.get(url)
			if request.status_code != 200:
				print(f"{index}: {request.status_code} for {url}")
		except requests.exceptions.SSLError:
			print(f"{index}: {request.status_code} for {url}")

	print("--- Process complete.")
