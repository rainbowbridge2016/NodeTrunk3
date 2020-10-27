#-= coding:utf-8 =-
__author__ = 'Rainbow'


import jieba
import getdb
import scprint

def getinput():
    inputstring = input('Type Key for Services: ').strip().upper()
    inputstringlist = inputstring.split(' ')
    return inputstringlist

def jiebasplit(stringlist):
    stringset = set()
    for string in stringlist:
        string_seg_list = jieba.cut_for_search(string)
        string_seg_set = set(string_seg_list)
        stringset = stringset | string_seg_set
    return stringset

def jiebasplit2(stringlist):   # 测试关键词或运算的分组结果，不理想。
    stringsetlist = list()
    for string in stringlist:
        substringset = set()
        string_seg_list = jieba.cut_for_search(string)
        substringset = set(string_seg_list)
        stringsetlist.append(substringset)
    return stringsetlist

def madesqlsen(tablename,stringset):
    wheresen = 'where '
    n = 0 
    str_seg_list = list(stringset)
    m = len(str_seg_list)
    for strseg in str_seg_list:
        wheresen = wheresen + "业务名称 like '%" + strseg + "%' "
        n = n + 1
        if n < m:
            wheresen = wheresen  + " AND "
        else:
            pass
    sqlsen = "select distinct 维护单位,分局,统一编号,来源,光分配模块位置,端子位置,光缆名称,纤序,业务名称,落地设备标记,对端局,长度,跳接光分配模块位置,跳接端子位置 " \
            + "from " + tablename + " " + wheresen + "order by " +  "来源,分局,光分配模块位置,端子位置,业务名称,对端局 " + ";"
    return sqlsen


def getstrlongest(string): # 可以做成公共模块
    n = 0
    #for i in row:
    #print string
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

def displaytoscreen(datalist,keyset):
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
        try:
            scprint.print(k, end = ' ')
        except UnicodeEncodeError:
            print()
            scprint.print("*************Some words in truble by decode or encode.*************", color = 'Red', bcolor = 'Grey7')
            print()
    scprint.print('--------------------------------------------------------------------')
    for datarow in datalist:
        scprint.print('==>:', color = 'Yellow', bcolor = 'Grey7', end = ' ')
        scprint.print(format(datarow[3],'>'+str(n3)), color = 'Yellow3', bcolor = 'Grey7', end = ' ')
        scprint.print(format(datarow[1],'<'+str(n1)), color = 'Grey85', bcolor = 'Grey7', end = ' ')
        scprint.print(format(datarow[4],'<'+str(n4)), color = 'Green4', bcolor = 'Grey7', end = ' ')
        scprint.print(format(datarow[5],'>'+str(n5)), color = 'Grey85', bcolor = 'Grey7', end = ' ')
        scprint.print(format(datarow[8],'<'+str(int(n8*1.3))), color = 'Chartreuse3', bcolor = 'Grey7', end = ' ')
        scprint.print(format(datarow[7],'<'+str(n7)), color = 'Green4', bcolor = 'Grey7', end = ' ')
        scprint.print(format(datarow[10],'<'+str(n10)), color = 'Yellow3', bcolor = 'Grey7', end = ' ')
        scprint.print(format(datarow[6],'<'+str(n6)), color = 'DodgerBlue1', bcolor = 'Grey7', end = ' ')
        scprint.print(format(datarow[11],'<'+str(n11)), color = 'Green4', bcolor = 'Grey7', end = ' ')
        print()
    scprint.print('--------------------------------------------------------------------', color = 'Grey85', bcolor = 'Grey7', end = ' ')
    #print ('Trunk num: %d, Node num: %d.'%(len(cablelist),len(nodelist))),
    scprint.print('Total of Recoder: %d.'%len(datalist), color = 'Grey85', bcolor = 'Grey7', end = ' ')
    scprint.print('--------------------------------------------------------------------', color = 'Grey85', bcolor = 'Grey7')

def madegraph(dataarray):
    nodepeerset = set()
    nodeset = set()
    for row in dataarray:
        np = tuple()
        np = (row[1],row[10])
        nodepeerset.add(np)
        nodeset.add(row[1])
        nodeset.add(row[10])
    return nodeset,nodepeerset

def paintgraph(nodeset,peerset,keylist):
    import time
    import os
    import pygraphviz as pgv

    home = os.chdir(u'd:\\trunkcheckpngtemp')
    time = time.localtime()
    filetime = str(time[0]) + '-' + str(time[1]) + '-' +str(time[2]) + '-' +str(time[3]) + '-' +str(time[4]) + '-' +str(time[5])
    keys = ''
    for n in keylist:
        keys = keys + '_' + n#.decode('GBK')
    flname = filetime + keys#.encode('utf-8') + keyjieba
    #print flname
    
    edgelist = list(peerset)
    edgelist.sort()
    nodelist = list(nodeset)
    nodelist.sort()
    
    j = 0 
    for i in range(len(nodelist)):
        if nodelist[j] == '' or len(nodelist[j]) == 0:
            nodelist.pop(j)
        else:
            j += 1
    
    j = 0
    for i in range(len(edgelist)):
        if edgelist[j][0] == '' or edgelist[j][1] == '' or len(edgelist[j][0]) == 0 or len(edgelist[j][1]) == 0:
            edgelist.pop(j)
        else:
            j += 1

    G=pgv.AGraph()
    G=pgv.AGraph(strict=False,directed=True)
    '''
    for n in edgelist:
        print(n, end = ' ')
        print('---%d',len(n))
    '''
    G.add_nodes_from(nodelist)
    G.add_edges_from(edgelist)

    G.graph_attr['center'] = True
    G.graph_attr['rankdir'] = 'LR'
    G.graph_attr['bgcolor'] = "#808080"
    G.graph_attr['layout'] = 'dot'
    G.graph_attr['label'] = 'Key:' + keys
    G.graph_attr['fontname'] = "Sans"
    G.graph_attr['lheight'] = 0.3
    G.graph_attr['dpi'] = 300
    
    G.edge_attr['dir']='none'
    
    G.node_attr['fontname'] = "Sans"
    #G.node_attr['fontname'] = "Miecrosoft YaHei"
    G.node_attr['fontsize'] = 12
    G.node_attr['fontcolor'] = 'white'
    
    try:
        G.layout()
    except 'Pango-WARNING **':
        pass
    
    G.write(flname + '.' + 'dot')
    G.draw(flname + '.' + 'png')
    #G.draw(flname + '.' + 'svg',format='svg') #输出的矢量图很大，很怪异。
    #G.draw(flname + '.' + 'svg')
    G.clear()


def madeGraphTheorylist(rowarray):
    rlist = list()
    for r in rowarray:
        temppeer = list() 
        startname = r[1]
        endname = r[10]
        lang = r[11]
        temppeer.append(startname)
        temppeer.append(endname)   
        temppeer.append(int(lang)) 
        rlist.append(tuple(temppeer))
    return rlist



def searchsev():
    stringlist = getinput()
    #print stringlist
    if len(stringlist) > 0 :
        serset = jiebasplit(stringlist)
        #serset = jiebasplit2(stringlist)
        #print serset
        if len(serset) > 0:
            sqlsent = madesqlsen('all_fibre_201608_2',serset)
            #sqlsent = madesqlsen2('all_fibre_201608_2',serset)
            #print sqlsent
            rowlist = getdb.getdatafromdb(sqlsent)
            #rowdecode = getdb.datedeunicode(rowlist)
            displaytoscreen(rowlist,serset)
        else:
            pass
        mg = input('Make top for all route? please type or "g" or "n".:').strip()
        if mg == 'g' or mg == 'G':
            nodes,edges = madegraph(rowlist)
            #print stringlist
            #print serset

            paintgraph(nodes,edges,stringlist)
        else:
            pass
        tg = input('Do you want to display all route link? please type or "y" or "n".:').strip()
        if tg == 'Y' or tg =='y':
            rowroute = madeGraphTheorylist(rowlist)
            import graphtheory
            graphtheory.mainfuntion(rowroute)
        else:
            pass
    else:
        pass


