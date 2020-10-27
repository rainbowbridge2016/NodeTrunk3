#-= coding:utf-8 =-
__author__ = 'Rainbow'

import getdb
import scprint


def madegetnodeforwordsql(tablename,name):
    fname = "'%" + name + "%'"  #把字符串再用utf-8编码成utf8的码才能和下面的文本相加，才能传入数据库。
    sqlsen = "select distinct A.起始端名称 AS 局向, cast(count(A.唯一标识) as text) AS 数量 from " + \
             "(select distinct 起始端名称,对端名称,唯一标识 from " + tablename + " where 起始端名称 like " + fname + " or 对端名称 like " + fname + \
             " union " + \
             " select distinct 对端名称,起始端名称,唯一标识 from " + tablename + " where 起始端名称 like " + fname + " or 对端名称 like " + fname + " ) AS A " + \
             " where A.起始端名称 not like " + fname + " GROUP BY 局向 ORDER BY 数量 DESC;"
    return sqlsen

def nodefor():
    nameline = input('Type Name for nodes: ').strip()
    namelist = nameline.split(' ')
    for name in namelist:
        sqlse = madegetnodeforwordsql('all_trunk_201608_double',name)
        rowlist = getdb.getdatafromdb(sqlse)
        nn = 0 
        tat = 0 
        scprint.print('------------------------------',name,'------------------------------', color='Grey85', bcolor='Grey7')
        for r in rowlist:
            scprint.print('%4s='%r[0], end = '')
            scprint.print(str('%2s,'%r[1]), color = 'Blue', bcolor='Grey7', end = '')
            tat = tat + int(r[1])
            nn = nn + 1
            if nn > 9:
                nn = 0
                print()
                print()
        scprint.print(str('Forword:%4d,   Trunks:%4d'%(len(rowlist),tat)), color = 'Red', bcolor='Grey7')
        scprint.print('==============================',name,'==============================', color='Grey85', bcolor='Grey7')
