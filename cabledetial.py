#-= coding:utf-8 =-
__author__ = 'Rainbow'


import getdb

password = False

def getinput():
    inputstring = input('Type Key for TrunkID: ').strip().upper()
    inputstringlist = inputstring.split(' ')
    return inputstringlist

def madesqlsen(tablename,stringlist):
    global password

    for string in stringlist:
        #print len(string)
        if len(string) > 2:
            password = True
        else:
            password = False
        #print password
    if password == True:
        wheresen = 'where '
        n = 0 
        m = len(stringlist)
        for strseg in stringlist:
            wheresen = wheresen + "统一编号 like '%" + strseg + "%' "
            n = n + 1
            if n < m:
                wheresen = wheresen  + " OR "
            else:
                pass
        sqlsen = "select distinct 维护单位,分局,统一编号,来源,光分配模块位置,端子位置,光缆名称,纤序,业务名称,落地设备标记,对端局,长度,跳接光分配模块位置,跳接端子位置 " \
                + "from " + tablename + " " + wheresen + "order by " +  "统一编号,来源,分局,光分配模块位置,端子位置,业务名称,对端局 " + ";"
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


def displaytoscreen(datalist,keyset):
    import scprint
    n0,n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,n12,n13 = 0,0,0,0,0,0,0,0,0,0,0,0,0,0
    n0 = getstrlongest([i[0] for i in datalist]) #n0=>维护单位
    n1 = getstrlongest([i[1] for i in datalist]) #n1=>分局
    n2 = getstrlongest([i[2] for i in datalist]) #n2=>统一编号
    n3 = getstrlongest([i[3] for i in datalist]) #n3=>来源
    n4 = getstrlongest([i[4] for i in datalist]) #n4=>光分配模块位置
    n5 = getstrlongest([i[5] for i in datalist]) #n5=>端子位置
    n6 = getstrlongest([i[6] for i in datalist]) #n6=>光缆名称
    n7 = getstrlongest([i[7] for i in datalist]) #n7=>纤序
    n8 = getstrlongest([i[8] for i in datalist]) #n8=>业务名称
    n9 = getstrlongest([i[9] for i in datalist]) #n9=>落地设备标记
    n10 = getstrlongest([i[10] for i in datalist]) #n10=>对端局
    n11 = getstrlongest([i[11] for i in datalist]) #n11=>长度
    n12 = getstrlongest([i[12] for i in datalist]) #n12=>跳接光分配模块位置
    n13 = getstrlongest([i[13] for i in datalist]) #n13=>跳接端子位置
    #print n0,n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,n12,n13 
    scprint.print('--------------------------------------------------------------------', end = ' ')
    for k in list(keyset):
        scprint.print(k, end = ' ')
    scprint.print('--------------------------------------------------------------------')
    for datarow in datalist:
        scprint.print('==>:', color = 'Yellow', bcolor = 'Grey7', end = ' ')
        scprint.print(format(datarow[3],'>'+str(n3)), color = 'Blue', bcolor = 'Grey7', end = ' ')
        scprint.print(format(datarow[1],'<'+str(n1)), color = 'Yellow', bcolor = 'Grey7', end = ' ')
        scprint.print(format(datarow[4],'<'+str(n4)), color = 'Green', bcolor = 'Grey7', end = ' ')
        scprint.print(format(datarow[5],'>'+str(n5)), color = 'Yellow', bcolor = 'Grey7', end = ' ')
        scprint.print(format(datarow[8],'<'+str(int(n8*1.3))), color = 'Blue', bcolor = 'Grey7', end = ' ')
        scprint.print(format(datarow[7],'<'+str(n7)), color = 'Green', bcolor = 'Grey7', end = ' ')
        scprint.print(format(datarow[10],'<'+str(n10)), color = 'Yellow', bcolor = 'Grey7', end = ' ')
        scprint.print(format(datarow[6],'<'+str(n6)), color = 'Blue', bcolor = 'Grey7', end = ' ')
        scprint.print(format(datarow[11],'<'+str(n11)), color = 'Green', bcolor = 'Grey7', end = ' ')
        print()
    scprint.print('--------------------------------------------------------------------', end = ' ')
    #print ('Trunk num: %d, Node num: %d.'%(len(cablelist),len(nodelist))),
    scprint.print('Total of Recoder: %d.'%len(datalist), end = ' ')
    scprint.print('--------------------------------------------------------------------')

def TrunkCableInfo():
    global password
    stringlist = getinput()
    #print len(stringlist)
    if len(stringlist) > 0:
        sqlsent = madesqlsen('all_fibre_201608_2',stringlist)
        if password == True:
            rowlist = getdb.getdatafromdb(sqlsent)
            #rowdecode = getdb.datedeunicode(rowlist)
            displaytoscreen(rowlist,stringlist)
        else:
            pass
    else:
        pass
