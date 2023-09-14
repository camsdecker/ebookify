from bs4 import BeautifulSoup
import urllib.request
import os

def main():
    book = "Title"
    author = "Author"
    #cover = images/sun.jpg
    firstchapter = "https://yourlinkhere.com"

    curr = firstchapter
    with open("out.txt", 'a', encoding="utf-8") as out:
        #out.write("![username](" + cover + ")\n")
        out.write("% "+book+'\n')
        out.write("% "+author+'\n')
        while curr is not None:
            if (curr[:6] != 'https:'): 
                curr = 'https:' + curr   # fixes link in case it gets cut off (8.3 of Twig's link is like this for some reason)
            print("got link: " + curr)
            
            html = urllib.request.urlopen(curr)
            soup = BeautifulSoup(html, 'html.parser')

            title, chapter = parsePage(soup)
            out.write("\n# " + title)
            out.write(chapter)
            print(" finished " + title)

            curr = getNext(soup)

    print("creating epub...")
    os.system("pandoc out.txt -o" + book + ".epub")
    os.remove("out.txt")
    print("done!")

# returns title and body of a chapter
def parsePage(soup):
    title_html = soup.find(id="content").article.header.h1
    body_html = soup.find(id="content").article.header.next_sibling.next_sibling.next_sibling
    
    body = body_html.get_text().splitlines()
    title = title_html.get_text().strip()
    
    for i, line in enumerate(body):
        if i == 1 or i == len(body)-1 or line == "Previous                                                                                                                      Next":
            continue
        try:
            chapter = chapter + '\n' + line + '\n'
        except NameError:
            chapter = line + '\n'
    return title, chapter

# returns link to next page or None if at end
def getNext(soup):
    next_button = soup.find(id="content").article.header.next_sibling.next_sibling.next_sibling.find_all('a')[1]
    if next_button.get_text() == 'Next' or next_button.get_text() == 'Next Chapter':
        link = next_button.get('href')
        return link
    else:
        return None

if __name__ == "__main__":
    main()