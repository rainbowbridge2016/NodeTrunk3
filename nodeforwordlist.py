#-= coding:utf-8 =-
__author__ = 'Rainbow'

import getdb
import scprint


def madegetnodeforwordsql(tablename,name):
    fname = "'" + name + "'"  #把字符串再用utf-8编码成utf8的码才能和下面的文本相加，才能传入数据库。去掉%适配符
    sqlsen = "select distinct A.起始端名称 AS 局向, cast(count(A.唯一标识) as text) AS 数量 from " + \
             "(select distinct 起始端名称,对端名称,唯一标识 from " + tablename + " where 起始端名称 = " + fname + " or 对端名称 = " + fname + \
             " union " + \
             " select distinct 对端名称,起始端名称,唯一标识 from " + tablename + " where 起始端名称 = " + fname + " or 对端名称 = " + fname + " ) AS A " + \
             " where A.起始端名称 != " + fname + " GROUP BY 局向 ORDER BY 局向 DESC;"
            #not like 换成 !=,like 换成了 =
    #print sqlsen 
    return sqlsen

def madegetnodeforworddetailsql(tablename,name):
    fname = "'" + name + "'"  #把字符串再用utf-8编码成utf8的码才能和下面的文本相加，才能传入数据库。
    sqlsen = "select distinct A.起始端名称 AS 局向,A.唯一标识,MAX(A.对应芯数),MAX(A.已经占用芯数) from " + \
             "(select distinct 起始端名称,对端名称,唯一标识,对应芯数,已经占用芯数 from " + tablename + " where 起始端名称 = " + fname + " or 对端名称 = " + fname + \
             " union " + \
             " select distinct 对端名称,起始端名称,唯一标识,对应芯数,已经占用芯数 from " + tablename + " where 起始端名称 = " + fname + " or 对端名称 = " + fname + " ) AS A " + \
             " where A.起始端名称 != " + fname + " GROUP BY 局向,A.唯一标识 ORDER BY 局向 DESC;"
             #not like 换成 !=,like 换成了 =
    #print sqlsen
    return sqlsen

def nodeforlist():
    nameline = input('Type Name for nodes: ').strip()
    namelist = nameline.split(' ')
    for name in namelist:
        sqlse = madegetnodeforwordsql('all_trunk_201803',name) #GBK解码，变成字符串。再用utf-8编码。  # 'all_trunk_201608'
        rowlist = getdb.getdatafromdb(sqlse)
        #unirows = getdb.data2unicodegen(rowlist)
        '''
        for r in unirows:
            for n in r:
                print n,
            print 
        '''
        nflist = dict()
        for d in rowlist:
            nflist[d[0]] = dict()
            nflist[d[0]]['trunknum'] = int(d[1])
            nflist[d[0]]['trunkid'] = list()
            nflist[d[0]]['trunkrl'] = list()
            nflist[d[0]]['trunkyy'] = list()
        #print nflist
        #for tn in nflist:
        #    print tn
        sqlse1 = madegetnodeforworddetailsql('all_trunk_201803',name) # 'all_trunk_201608'
        rowlist = getdb.getdatafromdb(sqlse1)
        #unirows = getdb.data2unicodegen1(rowlist)
        '''print '*******************************'
        print rowlist
        for r in unirows:
            for n in r:
                print n,
            print 
        '''
        for m in rowlist:
            nflist[m[0]]['trunkid'].append(m[1])
            nflist[m[0]]['trunkrl'].append(m[2])
            nflist[m[0]]['trunkyy'].append(m[3])
        #print nflist
        '''for tn1 in nflist:
            print tn1
        '''
        scprint.print('------------------------------------------------------------',name,'------------------------------------------------------------', color = 'Red', bcolor = 'Grey7')
        nfa = len(sorted(nflist.keys()))
        nra = 0
        nya = 0
        nia = 0
        for nn in sorted(nflist.keys()):
            scprint.print(format(nn,'>12'), color = 'Yellow3', bcolor = 'Grey7', end = ' ')
            #print '%12s'%nn,
            ni = 0
            ni = ni + len(nflist[nn]['trunkid'])
            nia = nia + ni
            nr = 0
            for nrn in nflist[nn]['trunkrl']:
                nr = nr + nrn
            nra = nra + nr # 局点所有光纤总数
            ny = 0
            for nyn in nflist[nn]['trunkyy']:
                ny = ny + nyn
            nya = nya + ny # 局点所有使用光纤总数
            scprint.print('(%3d/%4d=%.2f)'%(ny,nr,float(ny)/float(nr)), color = 'Green4', bcolor = 'Grey7', end = ' ')
            scprint.print('<', end = ' ')
            for ti in nflist[nn]['trunkid']:
                scprint.print(str('%4s'%ti), color = 'Blue', bcolor = 'Grey7', end = ' ')
                #print '%4s'%ti,
            scprint.print('> <', end = ' ')
            for tr in nflist[nn]['trunkrl']:
                scprint.print(str('%3s'%tr), color = 'Green', bcolor = 'Grey7', end = ' ')
                #print '%3s'%tr,
            scprint.print('> <', end = ' ')
            for tyy in nflist[nn]['trunkyy']:
                scprint.print(str('%3s'%tyy), color = 'Orange1', bcolor = 'Grey7', end = ' ')
                #print '%3s'%tyy,
            scprint.print('>', end = ' ')
            print()
        try:
            scprint.print(str('The Node have Forword:%4d,  Trunks:%4d,  Fibers:%6d/%4d/%2d,  InUse:%6d,  Rate:%.4f'%(nfa,nia,nra,nra/12,nra/(12*6),nya,float(nya)/float(nra))), color = 'Red', bcolor = 'Grey7')
        except ZeroDivisionError:
            scprint.print('*************Please type fullname of Node. Once again.*************', color = 'Red', bcolor = 'Grey7')
        #print 'Trunks:%2d  Fibers:%4d  InUse:%4d  Rate:%.2f'%(nia,nra,nya,float(nya)/float(nra))
        scprint.print('--------------------------------------------------------------------------------------------------------------------------------', color = 'Yellow3', bcolor = 'Grey7')
        #print nflist