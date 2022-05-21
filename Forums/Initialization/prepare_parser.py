# coding=utf-8

__author__ = 'DarkWeb'

import codecs
import glob
import os

from DarkWebMining_Sample.Forums.DB_Connection.db_connection import *

from DarkWebMining_Sample.Forums.BestCardingWorld.parser import *

#from DarkWebMining_Sample.Forums.Classifier.classify_product import predict
#from DarkWebMining_Sample.Forums.Classifier.classify_product import predict_semi



def isRussianForum(forum):

    with open('russian_forums.txt') as f:
        forums = f.readlines()

    result = False
    for iforum in forums:

        iforum = iforum.replace('\n','')
        if iforum == forum:
           result = True
           break

    return result

def mergePages(detPage, rec):

    key = u"Top:" + rec[1].upper() + u" User:" + rec[5].upper()
    #key = rec[16]

    if key in detPage:

        rmm = detPage[key]

        print ("----------------- Matched: " + rec[1] + "--------------------")
        rec[8] = rmm[1]
        rec[9] = rmm[2]
        rec[10] = rmm[3]
        rec[11] = rmm[4]
        rec[12] = rmm[5]
        rec[13] = rmm[6]
        rec[14] = rmm[7]
        rec[15] = rmm[8]

    return rec

def getPosts(posts):

    strPosts = ' '.join(posts)
    return strPosts.strip()

def persist_data(row, cur):

    user = create_user(cur, row[5])

    forum = create_forum(cur, row)

    board = create_board(cur, row, forum)

    topic = create_topic(cur, row, forum, board, user)

    create_posts(cur, row, forum, board, topic)

def new_parse(forum, createLog):

    print("Parsing The " + forum + " Forum and conduct data classification to store the information in the database.")

    crawlerDate = date.today()
    #crawlerDate = datetime.strptime('02/24/2020', '%m/%d/%Y').date()

    ini = time.time()

    global site

    con = connectDataBase()
    cur = con.cursor()

    create_database(cur, con)

    nError = 0

    lines = [] #lines.clear()
    lns = []   #lns.clear()
    listTopics = []
    detTopics = []
    detPage = {}
    rw = []
    errorMessage = False
    soup = ""

    if createLog:
        if not os.path.exists("./" + forum + "/Logs/" + forum + "_" + str("%02d" %crawlerDate.month) + str("%02d" %crawlerDate.day) + str("%04d" %crawlerDate.year) + ".log"):
            logFile = open("./" + forum + "/Logs/" + forum + "_" + str("%02d" %crawlerDate.today().month) + str("%02d" %crawlerDate.day) + str("%04d" %crawlerDate.year) + ".log", "w")
        else:
            print ("Files of the date " + str("%02d" %crawlerDate.today().month) + str("%02d" %crawlerDate.today().day) + str("%04d" %crawlerDate.today().year) +
                   " from the Forum " + forum + " were already read. Delete the referent information in the Data Base and also delete the log file "
                   "in the _Logs folder to read files from this Forum of this date again.")
            raise SystemExit

    for fileListing in glob.glob(os.path.join (os.getcwd().replace("Initialization","") + forum + "\\HTML_Pages\\" + str("%02d" %crawlerDate.month) + str("%02d" %crawlerDate.day) + str("%04d" %crawlerDate.year) + "\\Listing" ,'*.html')):
        lines.append(fileListing)

    for fileDescription in glob.glob(os.path.join (os.getcwd().replace("Initialization","") + forum + "\\HTML_Pages\\" + str("%02d" %crawlerDate.month) + str("%02d" %crawlerDate.day) + str("%04d" %crawlerDate.year) + "\\Description" ,'*.html')):
        lns.append(fileDescription)

    for index, line2 in enumerate(lns):
        str(line2)

        print ("Reading description folder of '" + forum + "', file '" + os.path.basename(line2) + "', index= " + str(index + 1) + " ... " + str(len(lns)))

        try:
            html = codecs.open(line2.strip('\n'), encoding='utf8')
            errorMessage = False
            soup = BeautifulSoup(html, "html.parser")
        except:
            try:
                html = open(line2.strip('\n'))
                soup = BeautifulSoup(html, "html.parser")
            except:
                print ("There was a problem to open the file " + line2)
                errorMessage = True
                nError += 1
                if createLog:
                   logFile.write(str(nError) + ". There was a problem to read the file " + line2 + ".\n")
                continue

        try:

           if forum == "BestCardingWorld":
               rmm = bestcardingworld_description_parser(soup, crawlerDate)
               #rmm = themajesticgarden_description_parser(soup, crawlerDate)

           key = u"Top:" + rmm[0].upper() + u" User:" + rmm[2][0].upper()
           #key = os.path.basename(line2).replace(".html","")

           if key not in detTopics:
               detTopics.append((rmm))
               detPage[key] = rmm

        except:

           if not errorMessage:
              print ("There was a problem to read the file " + line2 + " in the Description section!")
              nError += 1
              if createLog:
                 logFile.write(str(nError) + ". There was a problem to read the file " + line2 + " in the Description section.\n")

    for index, line1 in enumerate(lines):
        str(line1)

        print ("Reading listing folder of '" + forum + "', file '" + os.path.basename(line1) + "', index= " + str(index + 1) + " ... " + str(len(lines)))

        readError = False
        try:
            html = codecs.open(line1.strip('\n'), encoding='utf8')
            soup = BeautifulSoup(html, "html.parser")
        except:
            try:
                html = open(line1.strip('\n'))
                soup = BeautifulSoup(html, "html.parser")
            except:
                nError += 1
                if createLog:
                   logFile.write(str(nError) + ". There was a problem to read the file " + line1 + " in the Listing section.\n")
                print ("There was a problem to read the file " + line1 + " in the Listing section")
                readError = True

        if not readError:

            try:

                if forum == "BestCardingWorld":
                    rw = bestcardingworld_listing_parser(soup, line1, crawlerDate)
                   #rw = themajesticgarden_listing_parser(soup, line1, crawlerDate)

                for rec in rw:

                    rec = rec.split(',')

                    key = u"Top:" + rec[1].upper() + u" User:" + rec[5].upper()
                    #key = rec[16]

                    if key not in listTopics:

                        listTopics.append(key)

                        rec = mergePages(detPage, rec)

                        if isRussianForum(forum):
                           rec.append(str(predict(rec[1], getPosts(rec[8]), language='sup_russian')))
                        else:
                           rec.append(str(predict(rec[1], getPosts(rec[8]), language='sup_english')))

                        try:

                            persist_data(tuple(rec), cur)
                            con.commit()

                        except:

                            trace = traceback.format_exc()

                            if (trace.find("already exists") != -1):
                               con.commit()
                            else:
                               nError += 1
                               print ("There was a problem to persist the file " + line1 + " in the database.")
                               if createLog:
                                  logFile.write(str(nError) + ". There was a problem to persist the file " + line1 + " in the database.\n")
                               con.rollback()

            except:

                nError += 1
                print ("There was a problem to read the file " + line1 + " in the listing section")
                if createLog:
                   logFile.write(str(nError) + ". There was a problem to read the file " + line1 + " in the Listing section.\n")

    if createLog:
       logFile.close()

    #end = time.time()

    #finalTime = float(end-ini)

    #print (forum + " Parsing Perfomed Succesfully in %.2f" %finalTime + "!")

    input("Parsing the " + forum + " forum and data classification done successfully. Press ENTER to continue\n")


