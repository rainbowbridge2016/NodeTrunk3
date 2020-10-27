#-= coding:utf-8 =-
__author__ = 'Rainbow'

import getdb
import scprint

def madegetnodeodfsql(tablename,name):
    #fname = "'%" + name.encode('utf-8') + "%'"  #把字符串再用utf-8编码成utf8的码才能和下面的文本相加，才能传入数据库。
    #print fname
    #print type(name)
    #print name.decode('utf-8')
    #print name.encode('GBK')
    #print type(name.encode('utf-8'))
    #把字符串再用utf-8编码成utf8的码才能和下面的文本相加，才能传入数据库。
    sqlsen = " select distinct A.起始端名称,A.起始端位置,A.唯一标识,A.光缆名称,A.对端名称,A.对端位置 from " + \
             " ( select 起始端名称,起始端位置,唯一标识,光缆名称,对端名称,对端位置 from " + tablename + \
             " union select 对端名称,对端位置,唯一标识,光缆名称,起始端名称,起始端位置 from " + tablename + \
             " ) AS A   where A.起始端名称 like '%" + name + "%' order by A.起始端名称,A.起始端位置,A.唯一标识,A.对端名称,A.对端位置 " + ";"


            
            #  "select distinct 起始端名称,起始端位置,唯一标识,光缆名称,对端名称,对端位置 from " + tablename + \
            #  " where 起始端名称 like '%" + name.encode('utf-8') + "%' order by 起始端名称,起始端位置,唯一标识,对端名称,对端位置 " + ";"
    return sqlsen

def getstrlongest(string): # 可以做成公共模块
    n = 0
    for i in string:
        if i != None:
            if type(i) is not float:
                if len(i.strip()) > n:
                    n = len(i.strip())
            else:
                if len(str(i)) > n:
                   n = len(str(int(i)))
        else:
            pass
    return n

def nodeodf():
    nameline = input('Type Name for nodes: ').strip()
    namelist = nameline.split(' ')
    for name in namelist:
        sen = madegetnodeodfsql('all_trunk_201803',name) #GBK解码，变成字符串。再用utf-8编码。
        rowlist = getdb.getdatafromdb(sen)
        #for ll in rowlist:
        #    print(ll)
        n0,n1,n2,n3,n4,n5 = 0,0,0,0,0,0
        n0 = getstrlongest([i[0] for i in rowlist])
        n1 = getstrlongest([i[1] for i in rowlist])
        n2 = getstrlongest([i[2] for i in rowlist])
        n3 = getstrlongest([i[3] for i in rowlist])
        n4 = getstrlongest([i[4] for i in rowlist])
        n5 = getstrlongest([i[5] for i in rowlist])
        print(n0,n1,n2,n3,n4,n5)
        scprint.print('--------------------------------------------------------------------',name + ' ODF','--------------------------------------------------------------------', color='Grey85', bcolor='Grey7')
        for row in rowlist:
            scprint.print(format(row[0],'>'+str(n0)), color = 'Yellow', bcolor = 'Grey7', end = '' )
            if row[1] == None:
                scprint.print(format(row[1],'<'+str(n1)), color = 'Green', bcolor = 'Grey7', end = '')
            elif row[1] != None:
                scprint.print(format(row[1],'<'+str(n1)), color = 'Green', bcolor = 'Grey7', end = '')
            else:
                pass
            scprint.print(format(row[2],'<'+str(n2)), color = 'Red', bcolor = 'Grey7', end = '')
            #clr.print_skyblue_text(format(row[3].decode('utf-8'),'<'+str(n3/2)))
            scprint.print(format(row[4],'<'+str(n4)), color = 'Yellow', bcolor = 'Grey7', end = '')
            if row[5] == None:
                scprint.print(format(row[5],'<'+str(n5)), color = 'Green', bcolor = 'Grey7', end = '')
            elif row[5] != None:
                scprint.print(format(row[5],'<'+str(n5)), color = 'Green', bcolor = 'Grey7', end = '')
            else:
                pass
            scprint.print(format(row[3],'<'+str(n3)), color = 'Blue', bcolor = 'Grey7', end = '')
            print()
        cablelist = set([i[2] for i in rowlist])
        nodelist = set([i[4] for i in rowlist])
        scprint.print('--------------------------------------------------------------------', color='Grey85', bcolor='Grey7', end = '')
        scprint.print('Trunk num: %d, Forword Node num: %d.'%(len(cablelist),len(nodelist)), color='Grey85', bcolor='Grey7', end = '')
        scprint.print('--------------------------------------------------------------------', color='Grey85', bcolor='Grey7')
