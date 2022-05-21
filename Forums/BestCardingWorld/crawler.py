__author__ = '91Shadows'

from Forums.BestCardingWorld.parser import bestcardingworld_description_parser, bestcardingworld_links_parser

'''git push -u origin main
The Majestic Garden Crawler (Mechanize)
'''

import codecs, os, re
import socks, socket, time
from datetime import date

import urllib.parse as urlparse
import http.client as httplib
import mechanize
import subprocess
from bs4 import BeautifulSoup
from DarkWebMining_Sample.Forums.Initialization.prepare_parser import new_parse
from DarkWebMining_Sample.Forums.TheMajesticGarden.parser import themajesticgarden_links_parser

counter = 1
httplib.HTTPConnection._http_vsn = 10
httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'
baseURL = 'http://bestteermb42clir6ux7xm76d4jjodh3fpahjqgbddbmfrgp4skg2wqd.onion/viewforum.php?f=42&sid=ee2cbfd73c12923d979790b2bb4bdfd5'
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9150)


# Opens Tor Browser, crawls the website
def startCrawling():
    opentor()
    getUrl()
    forumName = getForumName()
    br = getAccess()

    if br != 'down':
        crawlForum(br)
        new_parse(forumName, False)

    # new_parse(forumName, False)

    # closetor()


# Opens Tor Browser
def opentor():
    global pid
    print("Connecting Tor...")
    path = open('../../torPath.txt').readline()
    pro = subprocess.Popen(path)
    pid = pro.pid
    time.sleep(7.5)
    input("Tor Connected. Press ENTER to continue\n")
    return


# Creates a connection through Tor Port
def getUrl(timeout=None):
    socket.socket = socks.socksocket
    socket.create_connection = create_connection
    return


# Makes the onion address request
def create_connection(address, timeout=None, source_address=None):
    sock = socks.socksocket()
    sock.connect(address)
    return sock


# Returns the name of website
def getForumName():
    name = 'BestCardingWorld'
    return name


# Return the link of website
def getFixedURL():
    url = 'http://bestteermb42clir6ux7xm76d4jjodh3fpahjqgbddbmfrgp4skg2wqd.onion/viewforum.php?f=42&sid=ee2cbfd73c12923d979790b2bb4bdfd5'
    # url = 'file:///C:/PhD/Projects/DarkWebMining_Sample/MarketPlaces/Crypto/HTML_Pages/02162016/Listing/Listing1.html'

    return url


# Closes Tor Browser
def closetor():
    global pid
    os.system("taskkill /pid " + str(pid))
    print('Closing Tor...')
    time.sleep(3)
    return


# Creates a Mechanize browser and initializes its options
def createBrowser():
    br = mechanize.Browser()
    cj = mechanize.CookieJar()
    br.set_cookiejar(cj)

    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'),
                     ('Accept', '*/*')]

    return br


def getAccess():
    url = getFixedURL()
    br = createBrowser()

    try:

        br.open(url)
        return br

    except:

        return 'down'


# Saves the crawled html page
def savePage(page, url):
    filePath = getFullPathName(url)
    os.makedirs(os.path.dirname(filePath), exist_ok=True)
    a = page.read()
    open(filePath, "wb").write(a)
    return


# Gets the full path of the page to be saved along with its appropriate file name
def getFullPathName(url):
    fileName = getNameFromURL(url)
    if isDescriptionLink(url):
        fullPath = '../BestCardingWorld/HTML_Pages/' + str("%02d" % date.today().month) + str(
            "%02d" % date.today().day) + str("%04d" % date.today().year) + '/' + 'Description/' + fileName + '.html'
    else:
        fullPath = '../BestCardingWorld/HTML_Pages/' + str("%02d" % date.today().month) + str(
            "%02d" % date.today().day) + str("%04d" % date.today().year) + '/' + 'Listing/' + fileName + '.html'
    return fullPath


# Creates the name of the file based on URL
def getNameFromURL(url):
    global counter
    name = ''.join(e for e in url if e.isalnum())
    if (name == ''):
        name = str(counter)
        counter = counter + 1
    return name


# Hacking and Markets related topics
def getInterestedLinks():
    links = []

    links.append(
        'http://bestteermb42clir6ux7xm76d4jjodh3fpahjqgbddbmfrgp4skg2wqd.onion/viewforum.php?f=43&sid=e12864ffccc5df877b03b573534955be')


    """links.append('http://bm26rwk32m7u7rec.onion/index.php?board=15.0')
    links.append('http://bm26rwk32m7u7rec.onion/index.php?board=35.0')
    links.append('http://bm26rwk32m7u7rec.onion/index.php?board=34.0')
    links.append('http://bm26rwk32m7u7rec.onion/index.php?board=36.0')
    links.append('http://bm26rwk32m7u7rec.onion/index.php?board=33.0')
    links.append('http://bm26rwk32m7u7rec.onion/index.php?board=22.0')
    links.append('http://bm26rwk32m7u7rec.onion/index.php?board=37.0')
    links.append('http://bm26rwk32m7u7rec.onion/index.php?board=21.0')
    links.append('http://bm26rwk32m7u7rec.onion/index.php?board=23.0')"""

    # links.append('file:///C:/PhD/Projects/DarkWebMining_Sample/Forums/TheMajesticGarden/HTML_Pages/02232016/Listing/Listing1.html')
    # links.append('file:///C:/PhD/Projects/DarkWebMining_Sample/Forums/TheMajesticGarden/HTML_Pages/02232016/Listing/Listing2.html')

    return links


# Start crawling Forum pages
def crawlForum(br):
    print("Crawling The Best Carding Worlk forum")

    linksToCrawl = getInterestedLinks()
    visited = set(linksToCrawl)
    initialTime = time.time()


    i = 0
    while i < len(linksToCrawl):
        link = linksToCrawl[i]
        print('Crawling :', link)
        try:
            page = br.open(link)

            """
            Paging
            """
            res = br.response().read()
            savePage(page, link)
            while True:
                soup = BeautifulSoup(res, 'html.parser')
                try:
                    next_link = soup.find("a", {"rel": "next"})['href']
                    full_url = urlparse.urljoin(linksToCrawl[i], next_link)
                    savePage(page, full_url)
                    linksToCrawl.insert(i+1, full_url)
                    page = br.open(next_link)
                    res = br.response().read()

                except:
                    break


            for l in br.links():
                absURL = urlparse.urljoin(l.base_url, l.url)
                if absURL not in visited and isListingLink(absURL):
                    visited.add(absURL)

                    # disabling the process of finding other links
                    # linksToCrawl.append(absURL)

            listOfTopics = findDescriptionPages(link)
            # j = 0
            for topic in listOfTopics:

                itemPage = br.open(str(topic))
                res = br.response().read()



                """
                Paging
                """
                pageNumber = 1
                while True:
                    savePage(itemPage, topic + str(pageNumber))
                    soup = BeautifulSoup(res, 'html.parser')
                    try:
                        next_link = soup.find("a", {"rel": "next"})['href']
                        itemPage = br.open(next_link)
                        res = br.response().read()
                        pageNumber += 1
                    except:
                        break

                # j += 1
        except Exception as e:
            print('Error getting link: ', link, e)
        i += 1

    # finalTime = time.time()
    # print finalTime - initialTime

    input("Crawling Best Carding world forum done sucessfully. Press ENTER to continue\n")

    return


# Returns True if the link is 'Topic' Links
def isDescriptionLink(url):
    if 'topic' in url:
        return True
    return False


# Returns True if the link is a listingPage link
def isListingLink(url):
    reg = 'board=[0-9]+.[0-9]+\Z'
    if len(re.findall(reg, url)) == 0:
        return False
    return True


# calling the parser to define the links
def findDescriptionPages(url):
    soup = ""

    error = False
    try:
        html = codecs.open("..\\BestCardingWorld\\HTML_Pages\\" + str("%02d" % date.today().month) + str(
            "%02d" % date.today().day) + str("%04d" % date.today().year) + "\\Listing\\" + getNameFromURL(
            url) + ".html", encoding='utf8')
        soup = BeautifulSoup(html, "html.parser")
    except:
        try:
            html = open("..\\BestCardingWorld\\HTML_Pages\\" + str("%02d" % date.today().month) + str(
                "%02d" % date.today().day) + str("%04d" % date.today().year) + "\\Listing\\" + getNameFromURL(
                url) + ".html")
            soup = BeautifulSoup(html, "html.parser")
        except:
            error = True
            print("There was a problem to read the file " + getNameFromURL(url) + " in the listing section.")

    if not error:
        return bestcardingworld_links_parser(soup)

    else:
        return []


def crawler():
    startCrawling()
    print("Crawling and Parsing The Best Carding World .... DONE!")
