# coding=utf-8

__author__ = 'DarkWeb'

import string
import time
from datetime import datetime, timedelta
import datetime as fulldatetime

def predict(title, description, language):
    return 0.8

def cleanText(originalText):

    safe_chars = string.ascii_letters + string.digits + " " + "_" + "/" + "&" + "$" + "#" "@" + "+" + "-" + "*" + "=" \
                     ":" + ";" + "." "," + "?" + "!" + "{" + "}" + "[" + "]" + "(" + ")" + "%" + "`" + "~" + "^" + "|" + "<" + ">"

    for index, text in enumerate(originalText):

        originalText[index] = ''.join([char if char in safe_chars else '' for char in text])

    return originalText

def convertDate(sdate, language, crawlerDate):

    if language == "english":

       todaysday = crawlerDate.strftime("%m/%d/%Y")

       sdate = sdate.replace(u"January","01")
       sdate = sdate.replace(u"February","02")
       sdate = sdate.replace(u"March","03")
       sdate = sdate.replace(u"April","04")
       sdate = sdate.replace(u"May","05")
       sdate = sdate.replace(u"June","06")
       sdate = sdate.replace(u"July","07")
       sdate = sdate.replace(u"August","08")
       sdate = sdate.replace(u"September","09")
       sdate = sdate.replace(u"October","10")
       sdate = sdate.replace(u"November","11")
       sdate = sdate.replace(u"December","12")
       sdate = sdate.replace(u"Jan","01")
       sdate = sdate.replace(u"Feb","02")
       sdate = sdate.replace(u"Mar","03")
       sdate = sdate.replace(u"Apr","04")
       sdate = sdate.replace(u"May","05")
       sdate = sdate.replace(u"Jun","06")
       sdate = sdate.replace(u"Jul","07")
       sdate = sdate.replace(u"Aug","08")
       sdate = sdate.replace(u"Sep","09")
       sdate = sdate.replace(u"Oct","10")
       sdate = sdate.replace(u"Nov","11")
       sdate = sdate.replace(u"Dec","12")
       sdate = sdate.replace(u".","")

       if sdate == "Today at":
          sdate = datetime.strptime(str(todaysday), '%m/%d/%Y').strftime('%m %d %Y')

       sdate = datetime.strptime(str(sdate), '%m %d %Y').strftime('%m/%d/%Y')

    elif language == "french":

       todaysday = crawlerDate.strftime("%m/%d/%Y")

       sdate = sdate.replace(u"janvier","01")
       sdate = sdate.replace(u"jan","01")
       sdate = sdate.replace(u"février","02")
       sdate = sdate.replace(u"juin","06")
       sdate = sdate.replace(u"juillet","07")
       sdate = sdate.replace(u"juil","07")
       sdate = sdate.replace(u"août","08")
       sdate = sdate.replace(u"septembre","09")
       sdate = sdate.replace(u"sept","09")
       sdate = sdate.replace(u"octobre","10")
       sdate = sdate.replace(u"oct","10")
       sdate = sdate.replace(u"novembre","11")
       sdate = sdate.replace(u"nov","11")
       sdate = sdate.replace(u"décembre","12")
       sdate = sdate.replace(u"déc","12")
       sdate = sdate.replace(u".","")

       if sdate == u"Aujourd'hui":
          sdate = datetime.strptime(str(todaysday), '%m/%d/%Y').strftime('%d %m %Y')

       if "mar" in sdate:
           print ("Add March to the IBM Black Market")
           raise SystemExit
       elif "avr" in sdate:
           print ("Add April to the IBM Black Market")
           raise SystemExit
       elif "mai" in sdate:
           print ("Add May to the IBM Black Market")
           raise SystemExit

       sdate = datetime.strptime(str(sdate), '%d %m %Y').strftime('%m/%d/%Y')

    elif language == "swedish":

       sdate = sdate.replace(u"jan","01")
       sdate = sdate.replace(u"feb","02")
       sdate = sdate.replace(u"mar","03")
       sdate = sdate.replace(u"apr","04")
       sdate = sdate.replace(u"maj","05")
       sdate = sdate.replace(u"jun","06")
       sdate = sdate.replace(u"jul","07")
       sdate = sdate.replace(u"aug","08")
       sdate = sdate.replace(u"sep","09")
       sdate = sdate.replace(u"okt","10")
       sdate = sdate.replace(u"nov","11")
       sdate = sdate.replace(u"dec","12")
       sdate = sdate.replace(u".","")

       sdate = datetime.strptime(str(sdate), '%d %m %Y').strftime('%m/%d/%Y')

    elif language == "russian":

       if sdate == u'\u0412\u0447\u0435\u0440\u0430':
          sdate = crawlerDate.today() - timedelta(1)
          sdate = datetime.strptime(str(sdate), '%Y-%m-%d').strftime('%d %m %Y')
       elif u'\xd1\xee\xe7\xe4\xe0\xed\xee' in sdate:
          return ""

       sdate = sdate.replace(u"января","01")
       sdate = sdate.replace(u"янв","01")
       sdate = sdate.replace(u"февраля","02")
       sdate = sdate.replace(u"Февраль", "02")
       sdate = sdate.replace(u"фев","02")
       sdate = sdate.replace(u"марта","03")
       sdate = sdate.replace(u"апреля","04")
       sdate = sdate.replace(u"апр","04")
       sdate = sdate.replace(u"мар","05")
       sdate = sdate.replace(u"май","05")
       sdate = sdate.replace(u"мая","05")
       sdate = sdate.replace(u"июня","06")
       sdate = sdate.replace(u"июн","06")
       sdate = sdate.replace(u"июля","07")
       sdate = sdate.replace(u"июл","07")
       sdate = sdate.replace(u"августа","08")
       sdate = sdate.replace(u"авг","08")
       sdate = sdate.replace(u"сентября","09")
       sdate = sdate.replace(u"сен","09")
       sdate = sdate.replace(u"октября","10")
       sdate = sdate.replace(u"Октябрь","10")
       sdate = sdate.replace(u"окт","10")
       sdate = sdate.replace(u"ноября","11")
       sdate = sdate.replace(u"ноя","11")
       sdate = sdate.replace(u"декабря","12")
       sdate = sdate.replace(u"дек","12")
       sdate = sdate.replace(u".","")

       sdate = datetime.strptime(str(sdate), '%d %m %Y').strftime('%m/%d/%Y')

    return sdate

def cleanLink(originalLink):

    safe_chars = string.ascii_letters + string.digits

    originalLink = ''.join([char if char in safe_chars else '' for char in originalLink])

    return originalLink

def organizeTopics(forum, nm, topic, board, view, post, user, addDate, href):

    rw = []

    for n in range(nm):

        lne = forum + "," + topic[n] + "," + board + ","
        lne += "-1" if len(view) == 0 else view[n]
        lne += ","
        lne += "-1" if len(post) == 0 else post[n]
        lne += "," + user[n] + "," + addDate[n] + "," + time.asctime()
        lne += ",-1,-1,-1,-1,-1,-1,-1,-1,"
        lne += href[n]

        rw.append(lne)

    return rw

def cleanString(originalString):
    updated_string = originalString.replace(",", "")    #replace all commas
    updated_string = updated_string.replace("\n", "")   #replace all newlines
    updated_string = updated_string.replace("\t", "")   #replace all tabs
    updated_string = updated_string.replace("\r", "")   #replace all carriage returns
    updated_string = updated_string.replace("'", "^")   #replace all semicolons
    updated_string = updated_string.replace(u"»", '')   #replace all arrows
    updated_string = updated_string.replace("!", "")
    updated_string = updated_string.replace(";", "") #replace all exclamations

    return updated_string

#function to convert long informal date string to formal date
def convertFromLongDate(longDate, crawlerdate):
    list_of_words = []
    list_of_words = longDate.split()

    day = 0
    week = 0
    hour = 0
    second = 0
    minute = 0
    year = 0
    total_days = 0


    if 'days' in list_of_words:
        index = list_of_words.index('days')
        day = float(list_of_words[index - 1])

    if 'weeks' in list_of_words:
        index = list_of_words.index('weeks')
        week = float(list_of_words[index - 1])

    if 'hours' in list_of_words:
        index = list_of_words.index('hours')
        hour = float(list_of_words[index - 1])

    if 'seconds' in list_of_words:
        index = list_of_words.index('seconds')
        second = float(list_of_words[index - 1])

    if 'minutes' in list_of_words:
        index = list_of_words.index('minutes')
        minute = float(list_of_words[index - 1])

    if 'years' in list_of_words:
        index = list_of_words.index('years')
        year = float(list_of_words[index - 1])

    if year != 0:
        total_days = day + 365 * year

    #today = datetime.date.today()
    timeDelta = fulldatetime.timedelta(days=total_days, weeks=week, hours=hour, seconds=second, minutes=minute)

    date = crawlerdate - timeDelta
    correct_date = str(date.strftime('%m/%d/%Y'))

    return correct_date













