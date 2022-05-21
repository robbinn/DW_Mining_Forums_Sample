__author__ = 'DarkWeb'

import psycopg2
import traceback
import time
from datetime import date

def connectDataBase():

    try:

        return psycopg2.connect(host='localhost', user='postgres', password='1234',dbname='darkweb_markets_forums')

    except:

        print ("Data base (darkweb_forums) not found.")
        raise SystemExit


def verifyForum(cur, nameForum):

    try:

        cur.execute("select id from forums where name = %(nameForum)s limit 1", {'nameForum': nameForum})

        recset = cur.fetchall()

        if recset:
            return recset[0][0]
        else:
            return 0

    except:

        trace = traceback.format_exc()
        print (trace)

def verifyBoard(cur, forum, nameBoard):

    try:

        cur.execute("select id from boards where forum_id = %(forum)s and name = %(nameBoard)s limit 1",
                    {'forum': forum, 'nameBoard': nameBoard})

        recset = cur.fetchall()

        if recset:
            return recset[0][0]
        else:
            return 0

    except:

        trace = traceback.format_exc()
        print (trace)

def verifyTopic(cur, forum, board, nameTopic):

    try:

        cur.execute("select id from topics where forum_id = %(forum)s and board_id = %(board)s and "
                    "name = %(nameTopic)s limit 1",{'forum': forum, 'board': board, 'nameTopic': nameTopic})

        recset = cur.fetchall()

        if recset:
            return recset[0][0]
        else:
            return 0

    except:

        trace = traceback.format_exc()
        print (trace)

def verifyUser(cur, nameUser):

    try:

        cur.execute("select id from users where name = %(nameUser)s limit 1", {'nameUser': nameUser})

        recset = cur.fetchall()

        if recset:
            return recset[0][0]
        else:
            return 0

    except:

        trace = traceback.format_exc()
        print (trace)

def getLastForum(cur):

    try:

        cur.execute("select id from forums order by id desc limit 1")

        recset = cur.fetchall()

        if recset:
            return recset[0][0]
        else:
            return 0

    except:

        trace = traceback.format_exc()
        print (trace)

def getLastBoard(cur):

    try:

        cur.execute("select id from boards order by id desc limit 1")

        recset = cur.fetchall()

        if recset:
            return recset[0][0]
        else:
            return 0

    except:

        trace = traceback.format_exc()
        print (trace)

def getLastTopic(cur):

    try:

        cur.execute("select id from topics order by id desc limit 1")

        recset = cur.fetchall()

        if recset:
            return recset[0][0]
        else:
            return 0

    except:

        trace = traceback.format_exc()
        print (trace)

def getLastUser(cur):

    try:

        cur.execute("select id from Users order by id desc")

        recset = cur.fetchall()

        if recset:
            return recset[0][0]
        else:
            return 0

    except:

        trace = traceback.format_exc()
        print (trace)

def getLastPost(cur):

    try:

        cur.execute("select id from Posts order by id desc limit 1")

        recset = cur.fetchall()

        if recset:
            return recset[0][0]
        else:
            return 0

    except:

        trace = traceback.format_exc()
        print (trace)

def create_forum(cur, row):

    forum = verifyForum(cur, row[0])

    if not forum:

       forum = int(getLastForum(cur) + 1)

       sql = "Insert into forums (id, name, date_Inserted) Values (%s, %s, %s)"

       recset = [forum, row[0], time.asctime()]

       cur.execute(sql, recset)

    return forum

def create_board(cur, row, forum):

    board = verifyBoard(cur, forum, row[2])

    if not board:

       board = int(getLastBoard(cur) + 1)

       sql = "Insert into boards (id, forum_id, name, date_inserted) Values (%s, %s, %s, %s)"

       recset = [board, forum, row[2], time.asctime()]

       cur.execute(sql, recset)

    return board

def create_topic(cur, row, forum, board, user):

    topic = verifyTopic(cur, board, forum, row[2])

    if not topic:

       topic = int(getLastTopic(cur) + 1)

       sql = "Insert into topics (id, forum_id, board_id, author_id, name, classification, date_added, date_inserted) " \
             "Values (%s, %s, %s, %s, %s, %s, %s, %s)"

       recset = [topic, forum, board, user, row[1], row[17], row[6] if row[6]!= '-1' else None, time.asctime()]

       cur.execute(sql, recset)

    return topic

def create_user(cur, nameUser):

    user = verifyUser(cur, nameUser)

    if not user:

       user = int(getLastUser(cur) + 1)

       sql = "Insert into users (id, name, date_Inserted) Values (%s, %s, %s)"

       recset = [user, nameUser, time.asctime()]

       cur.execute(sql, recset)

    return user

def create_posts(cur, row, forum, board, topic):

    if row[8] != "-1":

        for i in range(len(row[8])):

            id = int(getLastPost(cur) + 1)

            user = create_user(cur, row[9][i])

            sql = "Insert into posts (id, forum_id, board_id, topic_id, user_id, content, rule, date_added, reputation_user, " \
                  "status_user, feedback_user, interest_user, date_inserted) Values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            recset = [id, forum, board, topic, user, row[8][i] if row[8][i]!= '-1' else None,
                      row[14][i] if row[14][i]!= '-1' else None, row[10][i] if row[10][i]!= '-1' else None,
                      row[13][i] if row[13][i]!= '-1' else None, row[12][i] if row[12][i]!= '-1' else None,
                      row[11][i] if row[11][i]!= '-1' else None, row[15][i] if row[15][i]!= '-1' else None,

                      str("%02d" %date.today().month) + "/" + str("%02d" %date.today().day) + "/" +
                      str("%04d" %date.today().year) + " " + time.strftime("%I:%M:%S")]

            cur.execute(sql, recset)

def create_database(cur, con):

    try:

        sql = "create table forums (id integer NOT NULL, name character varying(255) NOT NULL, " \
              "date_inserted timestamp(6) with time zone NOT NULL, constraint forums_pk primary key (id))"
        cur.execute(sql)

        sql = "create table boards (id integer NOT NULL, forum_id integer NOT NULL, name character varying(255) NOT NULL," \
              "date_inserted timestamp(6) with time zone NOT NULL, constraint boards_pk primary key (id), " \
              "constraint boards_forum_id_fkey foreign key (forum_id) references forums (id))"
        cur.execute(sql)

        sql = "create table users (id integer NOT NULL, name character varying(255) NOT NULL, " \
              "date_inserted timestamp(6) with time zone NOT NULL, constraint users_pk primary key (id))"
        cur.execute(sql)

        sql = "create table topics(id integer NOT NULL, forum_id integer NOT NULL, board_id integer NOT NULL, " \
              "author_id integer NOT NULL, name character varying(255) NOT NULL, classification double precision not null, " \
              "date_added timestamp(6) with time zone, date_inserted timestamp(6) with time zone NOT NULL, " \
              "constraint topics_pk primary key (id), constraint topics_author_id_fkey foreign key (author_id) references users (id), " \
              "constraint topics_board_id_fkey foreign key (board_id) references boards (id), " \
              "constraint topics_forum_id_fkey foreign key (forum_id) references forums (id))"
        cur.execute(sql)

        sql = "create table posts(id integer NOT NULL, forum_id integer NOT NULL, board_id integer NOT NULL, " \
              "topic_id integer NOT NULL, user_id integer NOT NULL, content character varying(100000), rule character varying(5000), " \
              "reputation_user character varying(100), status_user character varying(255), feedback_user integer, " \
              "interest_user character varying(1000), date_added timestamp(6) with time zone, date_inserted timestamp(6) with time zone NOT NULL, " \
              "constraint posts_pk primary key (id), constraint posts_author_id_fkey foreign key (user_id) references users (id), " \
              "constraint posts_board_id_fkey foreign key (board_id) references boards (id), " \
              "constraint posts_forum_id_fkey foreign key (forum_id) references forums (id)," \
              "constraint posts_topic_id_fkey foreign key (topic_id) references topics (id))"
        cur.execute(sql)

        con.commit()

    except:

        con.rollback()

        trace = traceback.format_exc()

        if (trace.find("already exists")==-1):
            print ("There was a problem during the database creation." )
            raise SystemExit