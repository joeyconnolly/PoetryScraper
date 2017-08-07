from bs4 import BeautifulSoup, SoupStrainer
import httplib2
import re
import urllib.request

i = 1
index = set([])


#  Scan over each page of poet index and store the urls in a dictionary for later
def get_poets():
    global i
    index_page = "https://www.poetryfoundation.org/poets/browse#page=" + str(i) + "&sort_by=last_name&preview=0"
    # Try to open each page in turn, if not possible, we've run out of pages
    try:
        build_index(index_page)
        i += 1
        get_poets()
    except urllib.error.HTTPError as e:
        print(e)
        print("reached end of index")


def build_index(index_url):
    soup = BeautifulSoup(index_url, "html.parser")
    for link in soup.find_all('a', href=re.compile('.*/poets/.*')):
        print("Adding " + str(link) + "...")
        index.add(link)


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
            annotations = poem_soup.find_all('span', id=re.compile('annotation-\d-text'))
            for div in annotations:
                div.decompose()

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

# poet = input('Enter a poet: ').lower()
# poet = re.sub('[^a-z]+', '-', poet)
poet = "Seamus Heaney"
url = "http://www.poetryfoundation.org/bio/" + poet + "#about"

get_poets()

# try:
#     page_in = urllib.request.urlopen(url)
#     get_poems(page_in)
# except urllib.error.HTTPError:
#     print("Nothing found for that poet")
