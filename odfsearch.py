#-= coding:utf-8 =-
__author__ = 'Rainbow'

import getdb
import scprint

def getinput():
    inputstring = input('Type Key for ODF: ').strip().upper()
    inputstringlist = inputstring.split(' ')
    return inputstringlist

def madesqlsen(tablename,string):
    if len(string) > 0 :
        wheresen = 'where '
        wheresen = wheresen + "起始端位置 like '%" + string + "%' "
        sqlsen = "select distinct 光缆长度,起始端名称,起始端位置,光缆名称,对端位置,已经占用芯数,对端名称,对应芯数,维护单位,唯一标识 " \
                + "from " + tablename + " " + wheresen + "order by  起始端名称,起始端位置,唯一标识,光缆名称 " + ";" # 为了适应两个函数共用显示，调整了对端位置和对应芯数的查询位置。
        return sqlsen
    else:
        pass
    
def madesqldetailsen(tablename,string):
    if len(string) > 0 :
        wheresen = 'where '
        wheresen = wheresen + "光分配模块位置 like '%" + string + "%' "
        sqlsen = "select distinct 分局,光分配模块位置,光缆名称,对端局,业务名称,端子位置,长度 from " + tablename + \
                 " " + wheresen + " AND 业务名称 is not null order by  分局,光分配模块位置,光缆名称,端子位置 " + ";"
        return sqlsen
    else:
        pass

def getstrlongest(string): # 可以做成公共模块
    n = 0
    #for i in row:
    #print string
    for i in string:
        if i != None:
            if type(i) is not float and type(i) is not int:
                if len(i.strip()) > n:
                    n = len(i.strip())
            else:
                if len(str(i)) > n:
                    n = len(str(int(i)))
        else:
            pass
    return n


def displaytoscreen(datalist,odf):
    n0,n1,n2,n3,n4,n5,n6 = 0,0,0,0,0,0,0
    n0 = getstrlongest([i[0] for i in datalist])  #n0=>光缆长度
    n1 = getstrlongest([i[1] for i in datalist])  #n1=>起始端名称
    n2 = getstrlongest([i[2] for i in datalist])  #n2=>起始端位置
    n3 = getstrlongest([i[3] for i in datalist])  #n3=>光缆名称
    n4 = getstrlongest([i[4] for i in datalist])  #n4=>对应芯数
    n5 = getstrlongest([i[5] for i in datalist])  #n5=>已经占用芯数
    n6 = getstrlongest([i[6] for i in datalist])  #n6=>对端名称
    #n7 = getstrlongest([i[7] for i in datalist])  #n7=>对端位置
    #n8 = getstrlongest([i[8] for i in datalist])  #n8=>资源可用状态
    #n9 = getstrlongest([i[9] for i in datalist])  #n9=>唯一标识
    #print n0,n1,n2,n3,n4,n5,n6,n7,n8,n9
    scprint.print('--------------------------------------------------------------------', color='Grey85', bcolor = 'Grey7', end = ' ')
    scprint.print(odf, color='Grey85', bcolor = 'Grey7', end = ' ')
    scprint.print('--------------------------------------------------------------------', color='Grey85', bcolor = 'Grey7')
    for datarow in datalist:
    	#clr.print_yellow_text('==>:')
        scprint.print(format(datarow[0],'>'+str(n0)), color = 'Yellow', bcolor = 'Grey7', end = ' ')
        scprint.print(format(datarow[1],'<'+str(n1)), color = 'Blue', bcolor = 'Grey7', end = ' ')
        scprint.print(format(datarow[2],'<'+str(n2)), color = 'Yellow', bcolor = 'Grey7', end = ' ')
        scprint.print(format(datarow[5],'<'+str(n5)), color = 'Blue', bcolor = 'Grey7', end = ' ')
        scprint.print(format(datarow[3],'<'+str(n3)), color = 'Green', bcolor = 'Grey7', end = ' ')
        scprint.print(format(datarow[4],'>'+str(n4)), color = 'Yellow', bcolor = 'Grey7', end = ' ')
        scprint.print(format(datarow[6],'<'+str(n6)), color = 'Blue', bcolor = 'Grey7', end = ' ')
        print()
    scprint.print('--------------------------------------------------------------------', color='Grey85', bcolor = 'Grey7', end = ' ')
    scprint.print('Nodes of ODF: %d, Trunks of ODF: %d.'%(len(set([i[1] for i in datalist])),len(set([i[6] for i in datalist]))), color='Grey85', bcolor = 'Grey7', end = ' ')
    scprint.print('--------------------------------------------------------------------')

def searchodf():
    odflist = getinput()
    if len(odflist) > 0:
        for odf in odflist:
            if len(odf) > 0:
                #sqlsent = madesqlsen('all_fibre_201608_2',odf)
                sqlsent = madesqlsen('all_trunk_201608_double',odf)
                rowlist = getdb.getdatafromdb(sqlsent)
                #rowdecode = getdb.datedeunicode(rowlist)
                #for r in rowlist:
                #    print(r)
                displaytoscreen(rowlist,odf)
            pass
    else:
        pass

def searchodfdetial():
    odflist = getinput()
    if len(odflist) > 0:
        for odf in odflist:
            if len(odf) > 0:
                sqlsent = madesqldetailsen('all_fibre_201608_2',odf)
                rowlist = getdb.getdatafromdb(sqlsent)
                #rowdecode = getdb.datedeunicode(rowlist)
                #for r in rowlist:
                #    print(r)
                displaytoscreen(rowlist,odf)
            pass
    else:
        pass
    pass
