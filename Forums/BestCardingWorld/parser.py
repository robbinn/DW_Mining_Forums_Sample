__author__ = 'DarkWeb'

# Here, we are importing the auxiliary functions to clean or convert data
from DarkWebMining_Sample.Forums.Utilities.utilities import *

# Here, we are importing BeautifulSoup to search through the HTML tree
from bs4 import BeautifulSoup

# This is the method to parse the Description Pages (one page to each topic in the Listing Pages)

def bestcardingworld_description_parser(soup, crawlerDate):

    # Fields to be parsed

    topic = "-1"           # topic name
    user = []              # all users of each post
    addDate = []           # all dated of each post
    feedback = []          # all feedbacks of each vendor (this was found in just one Forum and with a number format)
    status = []            # all user's authority in each post such as (adm, member, dangerous)
    reputation = []        # all users's karma in each post (usually found as a number)
    sign = []              # all user's signature in each post (usually a standard message after the content of the post)
    post = []              # all messages of each post
    interest = []          # all user's interest in each post

    # Finding the topic (should be just one coming from the Listing Page)

    li = soup.find("h2", {"class": "topic-title"})
    topic = li.text
    topic = topic.replace(",","")
    topic = topic.replace("\n","")
    topic = cleanString(topic.strip())

    # Finding the repeated tag that corresponds to the listing of posts

    # posts = soup.find("form", {"name": "quickModForm"}).findAll('div', {"class": "windowbg"}) + \
    #         soup.find("form", {"name": "quickModForm"}).findAll('div', {"class": "windowbg2"})

    posts = soup.findAll('div', {"class": "post has-profile bg2"}) + \
            soup.findAll('div', {"class": "post has-profile bg1"})

    # For each message (post), get all the fields we are interested to:

    for ipost in posts:

        # Finding a first level of the HTML page

        #post_wrapper = ipost.find('div', {"class": "post_wrapper"}).find('div', {"class": "poster"})
        post_wrapper = ipost.find('a', {"class": "username-coloured"})
        # Finding the author (user) of the post

        #author = post_wrapper.find('h4')
        author = post_wrapper.text.strip()
        user.append(cleanString(author)) # Remember to clean the problematic characters

        # Finding the status of the author

        smalltext = ipost.find('dl', {"class": "postprofile"})

        # Testing here two possibilities to find this status and combine them

        # BestCarding does not have membergroup and postgroup
        membergroup = smalltext.find('li', {"class": "membergroup"})
        postgroup = smalltext.find('li', {"class": "postgroup"})
        if membergroup != None:
           membergroup = membergroup.text.strip()
           if postgroup != None:
              postgroup = postgroup.text.strip()
              membergroup = membergroup + " - " + postgroup
        else:
           if postgroup != None:
              membergroup = postgroup.text.strip()
           else:
              membergroup = "-1"
        status.append(cleanString(membergroup))

        # Finding the interest of the author
        # BestCarding does not have blurb
        blurb = smalltext.find('li', {"class": "blurb"})
        if blurb != None:
           blurb = blurb.text.strip()
        else:
           blurb = "-1"
        interest.append(cleanString(blurb))

        # Finding the reputation of the user
        # BestCarding does not have karma
        karma = smalltext.find('li', {"class": "karma"})
        if karma != None:
            karma = karma.text
            karma = karma.replace("Community Rating: ","")
            karma = karma.replace("Karma: ","")
            karma = karma.strip()
        else:
            karma = "-1"
        reputation.append(cleanString(karma))

        # Getting here another good tag to find the post date, post content and users' signature

        postarea = ipost.find('div', {"class": "inner"})

        dt = ipost.find('p', {"class": "author"}).text.split('»')[1]
        #dt = dt.strip().split()
        dt = dt.strip()
        date_time_obj = datetime.strptime(dt, '%a %b %d, %Y %I:%M %p')
        stime = date_time_obj.strftime('%a %b %d, %Y')
        sdate = date_time_obj.strftime('%I:%M %p')
        addDate.append(date_time_obj)
        # Finding the date of the post
        # date_time_obj = datetime.strptime(dt, '%a %b %d, %Y %I:%M %p')
        # smalltext = postarea.find('div', {"class": "flow_hidden"}).find('div', {"class": "keyinfo"})\
        #     .find('div', {"class": "smalltext"})
        # sdatetime = smalltext.text
        # sdatetime = sdatetime.replace(u"\xab","") # Removing unnecessary characters
        # sdatetime = sdatetime.replace(u"\xbb","") # Removing unnecessary characters
        # sdatetime = sdatetime.split("on: ")       # Removing unnecessary characters
        # sdatetime = sdatetime[1].strip()
        # stime = sdatetime[:-12:-1]                # Finding the time of the post
        # stime = stime[::-1]
        # sdate = sdatetime.replace(stime,"")       # Finding the date of the post
        # sdate = sdate.replace(",","")
        # sdate = sdate.strip()


        # Covert the date of the post that can be informed as: "12 February 2016", "today", "yesterday". We need
        # a date format here as "mm/dd/yyyy"

        #addDate.append(convertDate(sdate,"english", crawlerDate) + " " + stime)

        # Finding the post

        inner = postarea.find('div', {"class": "content"})
        inner = inner.text.strip()
        post.append(cleanString(inner))

        # Finding the users's signature

        #signature = ipost.find('div', {"class": "post_wrapper"}).find('div', {"class": "moderatorbar"}).find('div', {"class": "signature"})
        signature = ipost.find('div', {"class": "post_wrapper"})
        if signature != None:
           signature = signature.text.strip()
        else:
           signature = "-1"
        sign.append(cleanString(signature))

        # As no information about users's feedback was found, just assign "-1" to the variable

        feedback.append("-1")

    # Populate the final variable (this should be a list with all fields scraped)

    row = (topic, post, user, addDate, feedback, status, reputation, sign, interest)

    # Sending the results

    return row

# This is the method to parse the Listing Pages (one page with many posts)

def bestcardingworld_listing_parser(soup, html, crawlerDate):

    board = "-1"       # board name (the previous level of the topic in the Forum categorization tree.
                       # For instance: Security/Malware/Tools to hack Facebook. The board here should be Malware)

    nm = 0             # this variable should receive the number of topics
    topic = []         # all topics
    user = []          # all users of each topic
    post = []          # number of posts of each topic
    view = []          # number of views of each topic
    addDate = []       # when the topic was created (difficult to find)
    href = []          # this variable should receive all cleaned urls (we will use this to do the marge between
                       # Listing and Description pages)

    # Finding the board (should be just one)

    parents = soup.find('ul', {"class": "linklist navlinks"}).findAll('a')
    board = parents[1].text + u"->" + parents[2].text
    board = board.replace(u"\xbb","")
    board = cleanString(board.strip())

    # Finding the repeated tag that corresponds to the listing of topics

    itopics = soup.find('ul', {"class": "topiclist topics"}).findAll('div',{"class": "list-inner"})
    replies = soup.find('ul', {"class": "topiclist topics"}).findAll('dd',{"class": "posts"})
    views = soup.find('ul', {"class": "topiclist topics"}).findAll('dd',{"class": "views"})
    index = 0
    for itopic in itopics:

        # For each topic found, the structure to get the rest of the information can be of two types. Testing all of them
        # to don't miss any topic


        # tds = itopic.findAll('td', {"class": "subject stickybg2"})
        #
        # if len(tds) > 0:
        #    tag.append("strong")
        #    tag.append("subject stickybg2")
        #    tag.append("stats stickybg")
        # else:
        #    tds = itopic.findAll('td', {"class": "subject windowbg2"})
        #    if len(tds) > 0:
        #       tag.append("span")
        #       tag.append("subject windowbg2")
        #       tag.append("stats windowbg")

        # Adding the topic to the topic list

        topics = itopic.find('a', {"class": "topictitle"}).text
        topic.append(cleanString(topics))

        # Counting how many topics we have found so far

        nm = len(topic)

        # Adding the url to the list of urls
        link = itopic.find('a', {"class": "topictitle"}).get('href')
        link = cleanLink(link)
        href.append(link)

        # Finding the author of the topic
        ps = itopic.find('div', {"class":"responsive-hide"}).find('a', {"class": "username-coloured"}).text
        author = ps.strip()
        user.append(cleanString(author))

        # Finding the number of replies
        posts = replies[index].text.split()[0]
        posts = posts.strip()
        post.append(cleanString(posts))

        # Finding the number of Views
        tview = views[index].text.split()[0]
        tview = tview.strip()
        view.append(cleanString(tview))

        # As no information about when the topic was added, just assign "-1" to the variable
        dt = itopic.find('div', {"class": "responsive-hide"}).text.split('»')[1]
        dt = dt.strip()
        date_time_obj = datetime.strptime(dt,'%a %b %d, %Y %I:%M %p')
        # addDate.append(date_time_obj)
        addDate.append("-1")



        index += 1
    return organizeTopics("BestCardingWorld", nm, topic, board, view, post, user, addDate, href)

        # if len(tag) > 0:
        #
        #     # Finding the topic
        #
        #     tds = tds[0].find(tag[0])
        #     topics = tds.text
        #     topics = topics.replace(u"\xbb","")
        #     topics = topics.strip()
        #     topic.append(cleanString(topics))
        #
        #     # Counting how many topics we have found so far
        #
        #     nm = len(topic)
        #
        #     # Adding the url to the list of urls
        #
        #     link = tds.findAll('a', href=True)
        #     link = link[0].get('href')
        #     link = cleanLink(link)
        #     href.append(link)
        #
        #     # Finding the author of the topic
        #
        #     ps = itopic.find('td', {"class": tag[1]}).find('p').find('a')
        #     if ps == None:
        #        ps = itopic.find('td', {"class": tag[1]}).find('p')
        #        ps = ps.text.replace("Started by ","")
        #     else:
        #        ps = ps.text
        #     author = ps.strip()
        #     user.append(cleanString(author))
        #
        #     # Finding the number of replies
        #
        #     statistics = itopic.find('td', {"class": tag[2]})
        #     statistics = statistics.text
        #     statistics = statistics.split("Replies")
        #     posts = statistics[0].strip()
        #     post.append(cleanString(posts))
        #
        #     # Finding the number of Views
        #
        #     views = statistics[1]
        #     views = views.replace("Views","")
        #     views = views.strip()
        #     view.append(cleanString(views))
        #
        #     # As no information about when the topic was added, just assign "-1" to the variable
        #
        #     addDate.append("-1")

    #return organizeTopics("TheMajesticGarden", nm, topic, board, view, post, user, addDate, href)

def bestcardingworld_links_parser(soup):

    # Returning all links that should be visited by the Crawler

    href = []

    listing = soup.find('div', {"class": "forumbg"}).find('ul', {"class": "topiclist topics"}).findAll('li', {"class": "row bg1"}) + \
              soup.find('div', {"class": "forumbg"}).find('ul', {"class": "topiclist topics"}).findAll('li', {"class": "row bg2"})

    for a in listing:
        bae = a.find('a', {"class": "topictitle"}, href=True)
        link = bae['href']
        href.append(link)

    return href