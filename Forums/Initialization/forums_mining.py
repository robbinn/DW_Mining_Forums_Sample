
'''
Starting point of the Darkweb Mining Platform
'''

import os
from datetime import *
from DarkWebMining_Sample.Forums.TheMajesticGarden.crawler import crawler as crawlerTheMajesticGarden
from DarkWebMining_Sample.Forums.BestCardingWorld.crawler import crawler as crawlerBestCardingWorld
import time

# reads list of marketplaces
def getForums():
    with open('forumsList.txt') as f:
        forums = f.readlines()
    return forums

# Start mining each marketplace, start with crawling
#def crawl(mkt):
#    command = '../' + mkt + '/crawler.py'
#    os.system(command)

# Creates needed directories for marketplace if doesn't exist
def createDirectory(forum):

    # Package should already be there, holding crawler and parser
    if forum == 'Reddits':
       pagesMainDir = '../' + forum
    else:
       pagesMainDir = '../' + forum + "/HTML_Pages"

    if not os.path.isdir(pagesMainDir):
        os.mkdir(pagesMainDir)

    if forum == 'Reddits':
        createRedditsSubdirectories(pagesMainDir)
    else:
        createSubdirectories(pagesMainDir)

def createRedditsSubdirectories(pagesMainDir):

    with open('../Reddits/redditsList.txt', 'r') as f:
        reddits = f.readlines()

    for reddit in reddits:
        reddit = reddit.strip('\n')
        redditMainDir = pagesMainDir + '/' + reddit + '/HTML_Pages'
        if not os.path.isdir(redditMainDir):
            os.mkdir(redditMainDir)
        # Create inner time folders
        createSubdirectories(redditMainDir)

def createSubdirectories(pagesDir):

    currentDateDir = pagesDir + '/' +  str("%02d" %date.today().month) + str("%02d" %date.today().day) + str("%04d" %date.today().year)
    if not os.path.isdir(currentDateDir):
        os.mkdir(currentDateDir)

    listingDir = currentDateDir + '/Listing'
    if not os.path.isdir(listingDir):
        os.mkdir(listingDir)

    descriptionDir = currentDateDir + '/Description'
    if not os.path.isdir(descriptionDir):
        os.mkdir(descriptionDir)

if __name__ == '__main__':
    forumsList = getForums()

    for forum in forumsList:
        forum = forum.replace('\n','')

        print ("Creating listing and description directories ...")
        createDirectory(forum)
        time.sleep(5)
        input("Directories created sucessfully. Press ENTER to continue\n")

        if forum == "BestCardingWorld":
            crawlerBestCardingWorld()
            #crawlerTheMajesticGarden()


    print ("Scraping process completed sucessfully!")
