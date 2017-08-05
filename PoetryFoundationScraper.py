# THIS IS STILL PICKING UP NOTES FROM WITHIN THE POEMS

from bs4 import BeautifulSoup
import re
import urllib.request
from html.parser import HTMLParser
import html

poet = input('Enter a poet: ')
poet = poet.lower()
poet = re.sub('[^a-z]+','-',poet)
url = "http://www.poetryfoundation.org/bio/"+poet+"#about"

def getPoems(page):
    fileout = poet + ".txt"
    output = open(fileout,'w')
    soup = BeautifulSoup(page.read(),"html.parser")
    parser = HTMLParser()

    poems = soup.find_all('a',href=re.compile('.*/poems/\d.*'))
    usedTitles = []

    for poem in poems:
        poemURL = poem.get('href')
        poemPage = urllib.request.urlopen(poemURL)
        poemSoup = BeautifulSoup(poemPage.read(),"html.parser")
        poemTitleTag = poemSoup.find('h1')
        if poemTitleTag != None:
            poemTitle = poemTitleTag.text.strip()
            poemContent = poemSoup.find_all('div',{'style':"text-indent: -1em; padding-left: 1em;"})
            titleOut = poemTitle
            if poemTitle not in usedTitles:
                usedTitles.append(poemTitle)
                print(titleOut,file=output)
                print("",file=output)
                for line in poemContent:
                    lineOut = line.text.strip()
                    print(lineOut,file=output)
                print("\n******\n",file=output)

try:
    page = urllib.request.urlopen(url)
    getPoems(page)
except:
    print("Nothing found for that poet (or some other error)")
