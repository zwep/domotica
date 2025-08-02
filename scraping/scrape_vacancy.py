import requests
from bs4 import BeautifulSoup
import re

# Define the URL of the initial page
initial_url = "https://kombijde.politie.nl/vacatures?categories=ict"


# Function to get all .html URLs from a page
def get_html_urls(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    # Find all anchor tags with href attribute ending with .html
    html_links = soup.find_all('a', href=re.compile(r'\.html$'))

    # Extract the href attribute from the anchor tags
    html_urls = [link['href'] for link in html_links]

    return html_urls


# Function to extract text from a URL
def extract_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    # Extract text from the page (modify as needed)
    text = soup.get_text()

    return text


if __name__ == "__main__":
    # Get all .html URLs from the initial page
    html_urls = get_html_urls(initial_url)

    vacancy_container = []
    # Loop through the retrieved URLs and extract text
    for url in html_urls:
        full_url = f"https://kombijde.politie.nl{url}"
        text = extract_text_from_url(full_url)
        vacancy_container.append(text)
        # Print or save the extracted text
        # print(f"Text from {full_url}:\n{text}\n{'-' * 50}\n")
        # extract_text_from_url()
        # print(text.strip('\n'))


# Store each vacancy text
import os
dd = '/media/bugger/MyBook/data/politie_vacancy/'
for i, i_file in enumerate(vacancy_container):
    vacancy_name = i_file.strip('\n').split('-')[0]
    dest_file = os.path.join(dd, f'{vacancy_name}_{i}.txt')
    with open(dest_file, 'w') as f:
        f.write(i_file)

# Extract Waar ga je werken? tot Wie ben jij?
file_list = os.listdir(dd)
waargajewerken = []
for i_file in file_list:
    dest_file = os.path.join(dd, i_file)
    with open(dest_file, 'r') as f:
        A = f.readlines()

    A = [x.strip() for x in A]
    try:
        ind_start = A.index('Waar ga je werken?')
    except ValueError:
        ind_start = A.index('In welk werkveld kom je terecht?')
    try:
        ind_end = A.index('Wie ben jij?')
    except ValueError:
        ind_end = A.index('Wie ben je?')

    extracted_text = A[ind_start+1:ind_end-1]
    waargajewerken.append(extracted_text)

import itertools
unique_werken = set(list(itertools.chain(*waargajewerken)))

dest_file = os.path.join(dd, f'waargajewerken.txt')
with open(dest_file, 'w') as f:
    f.write('\n'.join(unique_werken))
# Process one vacancy text...


# Test
import numpy as np
import string
sample_list = list(string.ascii_lowercase) + [' '] + [' '] + [' '] + [' '] + [' '] + [' ']
''.join(list(np.random.choice(sample_list, 100, replace=True)))


