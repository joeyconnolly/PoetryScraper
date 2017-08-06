# THIS IS STILL PICKING UP NOTES FROM WITHIN THE POEMS

from bs4 import BeautifulSoup
import re
import urllib.request


def get_poems(page):
    fileout = poet + ".txt"
    output = open(fileout, 'w', encoding="utf-8")
    soup = BeautifulSoup(page.read(), "html.parser")

    poems = soup.find_all('a', href=re.compile('.*/poems/\d.*'))
    used_titles = []

    for poem in poems:
        poem_url = poem.get('href')
        poem_page = urllib.request.urlopen(poem_url)
        poem_soup = BeautifulSoup(poem_page.read(), "html.parser")
        # Checks that this is a poem page (i.e., has a h1 title)
        poem_title_tag = poem_soup.find('h1')

        if poem_title_tag is not None:
            poem_title = poem_title_tag.text.strip()

            # remove all annotations
            annotations = poem_soup.find_all('span', id=re.compile('annotation\-\d\-text'))
            for div in annotations:
                div.decompose()

            # Todo - This is picking up non-poem elements, is there a better indicator?
            poem_content = poem_soup.find_all('div', {'style': "text-indent: -1em; padding-left: 1em;"})
            title_out = poem_title

            if poem_title not in used_titles:
                used_titles.append(poem_title)
                print(title_out + "\n", file=output)
                # Remove any html tags
                for line in poem_content:
                    line_out = line.text.strip()
                    print(line_out, file=output)

                print("\n******\n", file=output)

poet = input('Enter a poet: ').lower()
poet = re.sub('[^a-z]+', '-', poet)
url = "http://www.poetryfoundation.org/bio/" + poet + "#about"

try:
    page_in = urllib.request.urlopen(url)
    get_poems(page_in)
except urllib.error.HTTPError:
    print("Nothing found for that poet")
