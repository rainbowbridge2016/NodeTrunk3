#-= coding:utf-8 =-
__author__ = 'Rainbow'

import psycopg2
import scprint

def getdatafromdb(sentence):
    dbname = "nodetrunk201803"  # "trunk201608"
    username = "postgres"
    passwd = "000000"
    hostip = "127.0.0.1"
    portnum = "5432"
    scprint.print('Now, connecting database, please wating......', color='Yellow3', bcolor='Grey7', end='')
    connecter = psycopg2.connect(database=dbname, user=username, password=passwd, host=hostip, port=portnum)
    if connecter.status == 1:
        scprint.print('Database has connected!', color='Yellow3', bcolor='Grey7', end='')
    else:
        scprint.print('and Wating......', color='Yellow3', bcolor='Grey7', end='')
    cur = connecter.cursor()
    cur.execute(sentence)
    rows = cur.fetchall()
    connecter.close()
    scprint.print('...... Datas have been got from Database.', color='Yellow3', bcolor='Grey7')
    #for r in rows:
    #    for n in r:
    #        if type(n) == str:
    #            n.replace(' ','')
    return rows