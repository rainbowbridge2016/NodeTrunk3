#-= coding:utf-8 =-
__author__ = 'Rainbow'

import getdb
import scprint
def madesqlsen(tablename,name = "设备"):
    fc = " '%" + name + "%' "
    sqlsent = " select a.局名,cast(count(a.唯一标识) as text) as 缆数 from (" + \
              " select distinct 起始端名称 AS 局名,唯一标识 from " + tablename + " where 起始端名称 not like " + fc + \
              " union " + \
              " select distinct 对端名称 AS 局名,唯一标识 from " + tablename + " where 对端名称 not like " + fc +  \
              " order by 局名,唯一标识 ) as a " + \
              " group by a.局名 " + \
              " order by count(a.唯一标识) DESC ;"
    return sqlsent

def nodelist():
    sqlsen = madesqlsen('all_trunk_201803')
    rowlist = getdb.getdatafromdb(sqlsen)
    #rowlist = getdatafromdb(sqlsentence)
    #unirow = getdb.data2unicodegen(rowlist)
    noden = len(rowlist)
    idn = 0
    ll = 0
    for li in rowlist:
        '''for n in li:
            print '%4s'%n,'''
        scprint.print('%4s=--%2s'%(li[0],li[1]), end = ' ')
        idn = idn + int(li[1])
        ll = ll + 1
        if ll > 9:
            ll = 0
            print()
            print()
    print()
    scprint.print(str('Nodes:%4d,  TrunkID: <%4d'%(noden,idn/2)), color = 'Red', bcolor = 'Grey7', end = ' ')
    print()
    #print "hello"