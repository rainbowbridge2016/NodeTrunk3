#-= coding:utf-8 =-
__author__ = 'Rainbow'

#import curses
#import psycopg2
import networkx as nx
#import cchardet as chardet
import platform
#import cmdcolor
import getdb
#import copy
import scprint


GG = []
finger = 0
orignodelist = []
allnodedestdict = {}
#trunkdbname = 'trunk201608'
trunktablename = 'all_trunk_201803' # 'all_trunk_201608'


def systeminfo():
    sysinfo = platform.uname()
    print(sysinfo[0],sysinfo[2],'on',sysinfo[4],', machine name is',sysinfo[1],)

def clearallspace(text):
    return ''.join((text.strip()).split())

def dbselectchoose():
    #choose = {}
    choose = dict()
    choose['fiber'] = '24' #芯数定的太高，影响网络通达性。应显示整个图的通达情况，以后有机会再编写。
    choose['rate'] = '0.85' #自己定的占用率。
    choose['withoutid'] = ['K135','K133'] #K135,K133是288芯，实际使用情况混乱，资源不清，新的通道都不使用K135了。
    choose['yesorno'] = 'Y' #语句实现的时候还包括 is null的记录。
    typetextc = input('Please type a choose, for used is u or U, for new is n or N.: ')
    #资源核查是选择富裕光缆是N，传输环路查找是在所有光缆中找是U。
    cablecy = clearallspace(typetextc)
    if cablecy == 'u' or cablecy == 'U':
        choose['uandn'] = cablecy
    else:
    #elif cablecy == 'n' or cablecy == 'N' or cablecy == '': 
        choose['uandn'] = 'n'
        typetextf = input('Please type cable capacity, (sample:72, is choose >= 72 fiber. Default is 24, type 0 is all, Enter is Default.): ')
        cablecy = clearallspace(typetextf)
        if cablecy != '0' and cablecy != '':
            choose['fiber'] = cablecy
        typetextr = input('Please type cable rate, (sample:0.7, is choose =< 0.7 using. Default is 0.85, type 0 is all, Enter is Default.): ')
        cablerate = clearallspace(typetextr)
        if cablerate != '0' and cablerate != '':
            choose['rate'] = cablerate
    #print choose
    return choose

def selectcent(choose,tablename=trunktablename):
    if choose['uandn'] == 'u' or choose['uandn'] == 'U':
        
        return " select distinct A.起始端名称,A.对端名称,MAX(A.光缆长度) AS 最长距离 from \
               ( \
               select distinct 起始端名称,对端名称,唯一标识,光缆长度 from " + trunktablename + \
               " where 光缆长度 is not null and 光缆长度 <> 0 \
               union \
               select distinct 对端名称,起始端名称,唯一标识,光缆长度 from " + trunktablename + \
               " where 光缆长度 is not null and 光缆长度 <> 0 \
               ) AS A \
               GROUP BY A.起始端名称,A.对端名称 \
               ORDER BY A.起始端名称,A.对端名称 \
               ; "
    else:
        return " select distinct A.起始端名称,A.对端名称,MAX(A.光缆长度) AS 最长距离 from \
               ( \
               select distinct 起始端名称,对端名称,唯一标识,光缆长度 from " + trunktablename + \
               " where (唯一标识 <> " + "'" + choose['withoutid'][0] + "'" + " and 唯一标识 <> " + "'" + choose['withoutid'][1] + "'" + ")" + \
               " and 对应芯数 >= " + choose['fiber'] + " and 占用率 <= " + choose['rate'] + \
               " and (资源可用状态 = " + "'" + choose['yesorno'] + "'" + \
               " or 资源可用状态 is null)" + \
               " and (光缆长度 is not null and 光缆长度 <> 0) \
               union \
               select distinct 对端名称,起始端名称,唯一标识,光缆长度 from " + trunktablename + \
               " where (唯一标识 <> " + "'" + choose['withoutid'][0] + "'" + " and 唯一标识 <> " + "'" + choose['withoutid'][1] + "'" + ")" + \
               " and 对应芯数 >= " + choose['fiber'] + " and 占用率 <= " + choose['rate'] + \
               " and (资源可用状态 = " + "'" + choose['yesorno'] + "'" + \
               " or 资源可用状态 is null)" + \
               " and (光缆长度 is not null and 光缆长度 <> 0) \
               ) AS A \
               GROUP BY A.起始端名称,A.对端名称 \
               ORDER BY A.起始端名称,A.对端名称 \
               ; "        

def data2unicodegen(rows):
    #rlist = []
    # 用集合过滤冗余数据行。程序结构不好，只能放在这里了。
    noderelationset = set()
    for r in rows:
        temp = list(r)
        tempnum = temp.pop()
        temp.sort()
        temp.append(tempnum)
        # print(list(r),temp,tuple(temp))
        noderelationset.add(tuple(temp))
    noderelationlist = list(noderelationset)
    return noderelationlist

def dboperation():
    chooselist = dbselectchoose()
    select = selectcent(chooselist) #default = trunktablename
    rowlist = getdb.getdatafromdb(select) #.decode('UTF-8')) # 为了适应在WIN32系统上运行，将包含中文的查询语句指明用'UTF-8'解码，WIN32系统缺省用'GBK'解码。
    rowsuni = data2unicodegen(rowlist)
    return rowsuni

def Goperatio(trunklist):
    G = nx.Graph()
    G.add_weighted_edges_from(trunklist)
    return G

def displayformatpath(pathgroup,distance='General'):
    global finger

    #pathgroup = pathsequence(pathgrouparray)
    cutline = '---------------------------------'
    scprint.print(cutline, color = 'Grey70', bcolor='Grey7',end='')
    scprint.print('The following is all of route.', color = 'Grey70', bcolor='Grey7', end='')
    scprint.print(cutline, color = 'Grey70', bcolor='Grey7')

    t = len(pathgroup) #传入的pathgroup，已经是array格式，不是对象了。
    n = 0
    for path in pathgroup:
        n += 1
        if distance == 'Short':
            #clr.print_intense_green_text(('Short<%d>[%d/%d]:')%(len(path)/2,n,t))
            scprint.print(('Short<%d>[%d/%d]:')%(len(path)/2,n,t), color = 'Green3', bcolor='Grey7', end = '')
            #print ('Short<%d>:')%len(path),
        else:
            scprint.print(('General<%d>[%d/%d]:')%(len(path)/2,n,t), color = 'Yellow3', bcolor='Grey7', end = '')
            #print ('General<%d>:')%(len(path)/2),
        for node in path:
            if type(node) is int:
                if distance == 'Short':
                    scprint.print(str('<%.3fkm>'%(float(node)/1000)), color = 'Green4', bcolor='Grey7', end = '')
                else:
                    scprint.print(str('<%.3fkm>'%(float(node)/1000)), color = 'Yellow4', bcolor='Grey7', end = '')
                    #print ('<%.3fkm>'%(float(node)/1000)),
            else:
                scprint.print('=[%s]='%node, color = 'Grey70', bcolor='Grey7', end='')
        print()
    scprint.print(cutline, color = 'Grey70', bcolor='Grey7', end = '')
    scprint.print('......Above in G[%d].......'%(finger + 1), color = 'Grey70', bcolor='Grey7', end='')
    scprint.print(cutline, color = 'Grey70', bcolor='Grey7')

    scprint.print(cutline, color = 'Grey70', bcolor='Grey7', end = '')
    scprint.print('如果未出现预期的中继路由，可能是中继光缆的状态异常。', color = 'Grey70', bcolor='Grey7', end='')
    scprint.print(cutline, color = 'Grey70', bcolor='Grey7')

def pathadddistance(patharray,GGG):
    #global allnodedestdict
    
    for p in patharray:
        nodepeer = zip(p[::1], p[1::1]) #参考高手的代码。将list的元素两两一组，重叠组成tuple。下面也有同样代码，最后的数字是2。
        ttlong = 0 #累加路径长度。
        for np in nodepeer:
            dd = 0 #缓存清零。保证数值方便排障。
            # dd = nx.astar_path_length(GGG,np[0],np[1])#各个算法都尝试过了，结果一致。再观察。
            # 上面的算法出现邻接距离异常，返回距离值小于邻接表中的距离，尝试其他算法依然如此，只有利用邻接矩阵查找邻接最大距离。最长距离，已经用SQL筛选出来，union正反两边，确保字典查找不出错。
            for n, nbrs in GGG.adj.items():
                # if n == np[0] or n == np[1]:
                if n == np[0] :
                    # print n,# nbrs
                    for nbr, eattr in nbrs.items():
                        #if n == np[0] or n == np[1]:
                        if nbr == np[1]:
                            # print nbr,eattr
                            dd = eattr["weight"]
            # 上面是用邻接矩阵找出邻接距离，最长距离。迭代性，相当厉害。
            #dd = nx.dijkstra_path_length(GGG,np[0],np[1])
            #dd = allnodedestdict[np[0]][np[1]] #路径上每2个节点间的最短距离。其实不是最短距离，这个全局变量给点值很疑惑。
            ttlong  += dd #在节点直连字典中查找两点之间的距离，并累加。
            p.insert(p.index(np[1]),dd) #在路径上每两个节点之间插入距离数值。
        p.append(ttlong)
    return patharray

def trunkselectdisplay(sp,pg): #中继信息显示模块。
    watchdog = False
    intotrunk = input('Display trunks for route? please type "y" or "n".:').strip()
    if intotrunk == 'y' or intotrunk == 'Y' or intotrunk == 'S' or intotrunk == 's':
        watchdog = True
    else:
        watchdog = False
    while watchdog:#
        routetype = input('Please type route number."s" or "number":').strip()
        if routetype.isdigit() is True:
            route = int(routetype)  #增加判断内容。str 非str。回来再加。
            if route == 0 :
                return
            else:
                if route <= len(pg):
                    croute = pg[route-1]
                else:
                    return
        elif routetype.isalpha() is True:
            if routetype == 'S' or routetype == 's':
                croute = sp[0]
            else:
                return
        else:
            return

        croutepeer = zip(croute[::2], croute[2::2])
        for np in croutepeer:
            strn = np[0] 
            endn = np[1] 
            sqlsent = "select 唯一标识,起始端名称,起始端位置,光缆名称,对端位置,对端名称,光缆长度,对应芯数,已经占用芯数,占用率,主要敷设方式,建设年份,资源可用状态,维护单位 " + \
                      " from " + trunktablename + \
                      " where (起始端名称 in (" + "'" + strn + "','" + endn + "'" + ") and 对端名称 in (" + "'" + strn + "','" + endn + "'" + ")) and (唯一标识 <> " + "'" + "K135" + "')" + \
                      " order by 唯一标识,维护单位,起始端名称;"
            #print sqlsent
            routeinfo = getdb.getdatafromdb(sqlsent)

            tidset = set()
            for t in routeinfo:
                tidset.add(t[0])
            tidlist = list(tidset)
            tidlist.sort()
            trunksnumber = len(tidlist)
            scprint.print(('--==<%s>---><%s>,')%(strn,endn), color = 'DarkOrange3', bcolor='Grey7', end='')
            scprint.print(('between has %d trunks.==--')%(trunksnumber), color = 'DarkOrange3', bcolor='Grey7')
            linebackground = ['Grey15','Grey7']

            '''
            for i in tidlist:
                print(i, end = ' ')
                print(linebackground[tidlist.index(i) % 2])
            '''
            for ris in routeinfo:
                space = ' '
                n = 0
                bkcolor = linebackground[tidlist.index(ris[0]) % 2]
                for ri in ris:
                    n = n + 1
                    if n == 7 or n == 8 or n == 9 or n == 10 or n == 4 or n == 13 or n == 3 or n == 5:
                        if type(ri)==str:
                            if ri == 'N':
                                scprint.print(ri, color = 'Red', bcolor=bkcolor, end='')
                                scprint.print(space, bcolor=bkcolor, end='')
                            elif n == 3 or n == 5:
                                scprint.print(ri, color = 'DarkOliveGreen1', bcolor=bkcolor, end='')
                                scprint.print(space, bcolor=bkcolor, end='')
                            else:
                                scprint.print(ri, color = 'Green4', bcolor=bkcolor, end='')
                                scprint.print(space, bcolor=bkcolor, end='')
                        else:
                            if ri > 90 and n ==8:
                                scprint.print(ri, color = 'Turquoise2', bcolor=bkcolor, end='')
                                scprint.print(space, bcolor=bkcolor, end='')
                            elif ri > 70 and n ==9:
                                scprint.print(ri, color = 'Green4', bcolor=bkcolor, end='')
                                scprint.print(space, bcolor=bkcolor, end='')
                            elif ri > 0.6 and n ==10:
                                scprint.print(ri, color = 'Orange1', bcolor=bkcolor, end='')
                                scprint.print(space, bcolor=bkcolor, end='')
                            else:
                                scprint.print(ri, color = 'Green4', bcolor=bkcolor, end='')
                                scprint.print(space, bcolor=bkcolor, end='')
                    else:
                        if type(ri)==str:
                            scprint.print(ri, color = 'Grey70', bcolor=bkcolor, end='')
                            scprint.print(space, color = 'Grey70', bcolor=bkcolor, end='')
                        else:
                            scprint.print(ri, color = 'Grey70', bcolor=bkcolor, end='')
                            scprint.print(space, color = 'Grey70', bcolor=bkcolor, end='')
                print()
            scprint.print('---------------------------------------------Trunks info--------------------------------------------------------------------', color = 'Grey70', bcolor='Grey7')

def exportGtop(routegroup,start,end):
    
    import time
    import os
    import pygraphviz as pgv

    home = os.chdir(u'd:\\trunkcheckpngtemp')
    time = time.localtime()
    filetime = str(time[0]) + '-' + str(time[1]) + '-' +str(time[2]) + '-' +str(time[3]) + '-' +str(time[4]) + '-' +str(time[5])
    flname = filetime + '_' + start + '-' + end

    nodeset = set()
    for n in routegroup:
        for m in n[::2]:
            nodeset.add(m)
    nodes = sorted(nodeset)
    edgeset = set()
    for e in routegroup:
        for ee in zip(e[::2],e[2::2]):
            edgeset.add(ee)
    edges = sorted(edgeset)

    G=pgv.AGraph()
    G=pgv.AGraph(strict=False,directed=True)
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    G.graph_attr['center'] = True
    G.graph_attr['rankdir'] = 'LR'
    G.graph_attr['bgcolor'] = "#808080"
    G.graph_attr['layout'] = 'dot'
    G.graph_attr['label'] = start + '==>' +end
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
    
    return None

def trunkroute(G,nodelist): 
    #print(nodelist)
    nodes = len(nodelist)
    #print(nodes)
    for i in range(0,(nodes-1)):
        startname = nodelist[i]
        endname = nodelist[i+1]
        #print(startname, end='')
        #print("---",end='')
        #print(endname)
        try:
            pathshort = []
            pathshort = list(nx.all_shortest_paths(G,startname,endname, weight='weight')) #加weight是按距离选择，选出一条最短路由。
            #print(pathshort)
            pathshortlong = pathadddistance(pathshort,G)#在节点之间加上最短距离数据。
            displayformatpath(pathshortlong,'Short') #将路由节点和距离显示在终端上。
        except nx.exception.NetworkXNoPath:
            scprint.print('**********Short Route Attention! %s to %s have no route in this G.**********'%(startname,endname))
        try:
            pathalllist = []
            pathalllist = list(nx.all_shortest_paths(G,startname,endname)) #不加weight按照节点最少为最短，加weight是按距离选择。
            pathalllist.sort()
            pathalllistlong = pathadddistance(pathalllist,G) #给路由组分别加上距离int。返回带距离的路由array。
            displayformatpath(pathalllistlong) #将节点名字传入函数，方便输出错误信息。
        except nx.exception.NetworkXNoPath:
            scprint.print('**********Route Attention! %s to %s have no route in this G.**********'%(startname,endname))
        if len(pathshort) != 0 and len(pathalllist) != 0 : #输出多路由的png的拓扑图，不输出最短路径的拓扑图。缺省在D盘，start - 中间 - end的格式。
            mtg = input('Make top for all route? please type "s" or "g" or "n".:').strip()
            if mtg == 'g' or mtg == 'G':
                exportGtop(pathalllist,startname,endname)
            elif mtg == 's' or mtg == 'S':
                pass
            else:
                pass

        if len(pathshort) != 0 and len(pathalllist) != 0 :
            trunkselectdisplay(pathshort,pathalllist)#加入光缆选择函数。


def detectnodeinG(G,nameline):  #检测节点列表内的节点是否在已知的图中
    nodeslist = list(nx.nodes(G)) # 获取图中节点的list。
    nodeslist.sort()
    isorno = list()
    for n in nameline:
        isorno.append(nodeslist.__contains__(n))

    return isorno


def nodedetectinG(nodelists):
    global GG
    global finger

    iftruelist = detectnodeinG(GG[finger],nodelists) #检测输入的节点是否在图中。并返回内容为True或False的list。
    if iftruelist.__contains__(False): #节点判断list中如果有false，则指明错误位置，并重新输入所有节点序列。
        scprint.print('Some NodeName is not available in Graph of getting.=>: ', end='')
        errorlocal = [i for (i,j) in enumerate(iftruelist) if j==False] #找出False节点序号，并形成list。python处理枚举类型绝妙方法。
        for n in errorlocal:
            scprint.print(nodelists[n], end='')
        print()
        return True  #节点输入有错误，重新输入所有节点。
    else:
        return False

def importnodes(nodeoredge):
    ifloop = True 
    while ifloop: #这个循环接收节点输入，并检测节点是否正确，指出错误并重新输入。
        if nodeoredge == 'node':
            nameline = input('Type Name list with space, for nodes: ').strip()#千万不能用clearallspace()函数，会清掉所有空格。
        elif nodeoredge == 'edge':
            nameline = input('Type Name list with space, for edge: ').strip()#千万不能用clearallspace()函数，会清掉所有空格。
        namelist = nameline.split() #将空格分开的节点转换成list。
        ifloop = nodedetectinG(namelist)
    return namelist # 返回node列表

def pushaGinlist(removelist,nodeoredge):
    global GG
    global finger

    #Gtemp = copy.deepcopy(GG[finger])
    Gtemp = (GG[finger]).copy() #nx自带的G拷贝工具。
    if nodeoredge == 'node':
        Gtemp.remove_nodes_from(removelist)
    elif nodeoredge == 'edge':
        tempobj = iter(removelist) # 另一位大神推荐的据说是list较大时，高效率的运行。两两组成tuple对，但要求输入的list是偶数，奇数失败返回为空。
        removepeerlist = [(x,tempobj.__next__()) for x in tempobj] # 另一位大神推荐的据说是list较大时，高效率的运行。
        #removepeerlist = zip(removelist[::2], removelist[1::2]) #最神奇的方式，网上找到的，高手的语法。两个元素组成一个tuple，奇数甩掉最后一个。
        Gtemp.remove_edges_from(removepeerlist)
    GG.append(Gtemp)
    finger = finger + 1

def popaGoutlist():
    global GG
    global finger
    
    GG.pop()
    finger = finger - 1


def trunkui():
    global GG
    global finger
    global orignodelist

    orignodelist = importnodes('node')
    #print(orignodelist)
    trunkroute(GG[finger],orignodelist)
    #print GG[finger].number_of_nodes()
    allofall = True
    while allofall:#这是程序整体循环包括删除节点，删除边，以及回退，退出。
        delnodes = input('Node DELETED in routing, changed all. please type "y" or "n".:')
        delnode = clearallspace(delnodes)
        if delnode == 'y' or delnode == 'Y':
            allofall = True
            activefor = 'node'
            delnodelist = importnodes(activefor)
            pushaGinlist(delnodelist,activefor)
            trunkroute(GG[finger],orignodelist)
        else:
            allofall = False
        
        deledges = input('Edge DELETED in routeing, change all. please type "y" or "n".: ')
        deledge = clearallspace(deledges)
        if deledge == 'y' or deledge == 'Y':
            allofall = True
            activefor = 'edge'
            deledgelist = importnodes(activefor)
            pushaGinlist(deledgelist,activefor)
            trunkroute(GG[finger],orignodelist)
        else:
            allofall = False
        
        if finger != 0 :
            gobacks = input('Do you want to BACK. please type "y" or "n".: ')
            goback = clearallspace(gobacks)
            if goback == 'y' or goback == 'Y':
                allofall = True
                popaGoutlist()
                trunkroute(GG[finger],orignodelist)
            else:
                allofall = False

        goons = input('Do you to be CONTINUE. please type "y" or "n".: ')
        goon = clearallspace(goons)
        if goon == 'n' or goon == 'N':
            allofall = False
        else:
            allofall = True

def startup():
    global GG
    global finger
    global orignodelist
    global allnodedestdict

    GG = []
    finger = 0
    orignodelist = []
    allnodedestdict = {}

    systeminfo()
    nodedestlist = dboperation() #从数据库中得到全网网络拓扑数据
    nodedestlist.sort()
    GG.append(Goperatio(nodedestlist)) #生成全网全图
    allnodedestdict = dict(nx.all_pairs_dijkstra_path_length(GG[0])) #生成全网各节点之间最短直连距离。不随拓扑改变而变化。
    #但上面这个函数得到的两个节点之间的距离，不是最短距离。纠结，继续看手册去。改完了在这里再描述
    trunkui() #正式进入程序功能入口。