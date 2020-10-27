#-= coding:utf-8 =-
__author__ = 'Rainbow'

import networkx as nx
import getdb
import scprint

GG = []
finger = 0
orignodelist = []
allnodedist = {}

def madeG(nodelistweigh):
    G = nx.Graph()
    G.add_weighted_edges_from(nodelistweigh)
    return G

def clearallspace(text):
    return ''.join((text.strip()).split())


def pathadddistance(patharray,GGG):
    #global allnodedist_S
    
    for p in patharray:
        nodepeer = zip(p[::1], p[1::1]) #参考高手的代码。将list的元素两两一组，重叠组成tuple。下面也有同样代码，最后的数字是2。
        ttlong = 0 #累加路径长度。
        for np in nodepeer:
            dd = 0 #缓存清零。保证数值方便排障。
            dd = nx.astar_path_length(GGG,np[0],np[1])#各个算法都尝试过了，结果一致。再观察。
            #dd = nx.dijkstra_path_length(GGG,np[0],np[1])
            #dd = allnodedist_S[np[0]][np[1]] #路径上每2个节点间的最短距离。其实不是最短距离，这个全局变量给点值很疑惑。
            ttlong  += dd #在节点直连字典中查找两点之间的距离，并累加。
            p.insert(p.index(np[1]),dd) #在路径上每两个节点之间插入距离数值。
        p.append(ttlong)
    return patharray



def pathadddistance(patharray,GGG):
    #global allnodedist
    
    for p in patharray:
        nodepeer = zip(p[::1], p[1::1]) #参考高手的代码。将list的元素两两一组，重叠组成tuple。下面也有同样代码，最后的数字是2。
        ttlong = 0 #累加路径长度。
        for np in nodepeer:
            dd = 0 #缓存清零。保证数值方便排障。
            dd = nx.astar_path_length(GGG,np[0],np[1])#各个算法都尝试过了，结果一致。再观察。
            #dd = nx.dijkstra_path_length(GGG,np[0],np[1])
            #dd = allnodedist[np[0]][np[1]] #路径上每2个节点间的最短距离。其实不是最短距离，这个全局变量给点值很疑惑。
            ttlong  += dd #在节点直连字典中查找两点之间的距离，并累加。
            p.insert(p.index(np[1]),dd) #在路径上每两个节点之间插入距离数值。
        p.append(ttlong)
    return patharray

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
            scprint.print(('<%s>---><%s>')%(strn,endn), color = 'DarkOrange3', bcolor='Grey7' )
            sqlsent = "select 唯一标识,起始端名称,起始端位置,光缆名称,对端位置,对端名称,光缆长度,对应芯数,已经占用芯数,占用率,主要敷设方式,建设年份,资源可用状态,维护单位 " + \
                      " from " + trunktablename + \
                      " where (起始端名称 in (" + "'" + strn + "','" + endn + "'" + ") and 对端名称 in (" + "'" + strn + "','" + endn + "'" + ")) and (唯一标识 <> " + "'" + "K135" + "')" + \
                      " order by 唯一标识,维护单位,起始端名称;"
            #print sqlsent
            routeinfo = getdb.getdatafromdb(sqlsent)
            for ris in routeinfo:
                space = ' '
                n = 0
                for ri in ris:
                    n = n + 1
                    if n == 7 or n == 8 or n == 9 or n == 10 or n == 4 or n == 13 or n == 3 or n == 5:
                        if type(ri)==str:
                            if ri == 'N':
                                scprint.print(ri, color = 'Red', bcolor='Grey7', end='')
                                scprint.print(space, bcolor='Grey7', end='')
                            elif n == 3 or n == 5:
                                scprint.print(ri, color = 'DarkOliveGreen1', bcolor='Grey7', end='')
                                scprint.print(space, bcolor='Grey7', end='')
                            else:
                                scprint.print(ri, color = 'Green4', bcolor='Grey7', end='')
                                scprint.print(space, bcolor='Grey7', end='')
                        else:
                            if ri > 90 and n ==8:
                                scprint.print(ri, color = 'Turquoise2', bcolor='Grey7', end='')
                                scprint.print(space, bcolor='Grey7', end='')
                            elif ri > 70 and n ==9:
                                scprint.print(ri, color = 'Green4', bcolor='Grey7', end='')
                                scprint.print(space, bcolor='Grey7', end='')
                            elif ri > 0.6 and n ==10:
                                scprint.print(ri, color = 'Orange1', bcolor='Grey7', end='')
                                scprint.print(space, bcolor='Grey7', end='')
                            else:
                                scprint.print(ri, color = 'Green4', bcolor='Grey7', end='')
                                scprint.print(space, bcolor='Grey7', end='')
                    else:
                        if type(ri)==str:
                            scprint.print(ri, bcolor='Grey7', end='')
                            scprint.print(space, bcolor='Grey7', end='')
                        else:
                            scprint.print(ri, bcolor='Grey7', end='')
                            scprint.print(space, bcolor='Grey7', end='')
                print()
            scprint.print('---------------------------------------------Trunks info--------------------------------------------------------------------', color = 'Grey70', bcolor='Grey7')


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
            pathshort = list(nx.all_shortest_paths(G,startname,endname, weight='weight')) #加weight是按距离选择，选出一条最短路由。
            #print(pathshort)
            pathshortlong = pathadddistance(pathshort,G)#在节点之间加上最短距离数据。
            displayformatpath(pathshortlong,'Short') #将路由节点和距离显示在终端上。
        except nx.NetworkXNoPath:
            scprint.print('**********Short Route Attention! %s to %s have no route in this G.**********'%(startname))
        try:
            pathalllist = list(nx.all_shortest_paths(G,startname,endname)) #不加weight按照节点最少为最短，加weight是按距离选择。
            pathalllist.sort()
            pathalllistlong = pathadddistance(pathalllist,G) #给路由组分别加上距离int。返回带距离的路由array。
            displayformatpath(pathalllistlong) #将节点名字传入函数，方便输出错误信息。
        except nx.NetworkXNoPath:
            scprint.print('**********Route Attention! %s to %s have no route in this G.**********'%(startname))
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
    nodeslist = nx.nodes(G) # 获取图中节点的list。
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


def mainfuntion(allrows):
    # global GG_S
    # global finger_S
    # global orignodelist_S
    # global allnodedist_S # is not use,add in here is clear global for next recall model.
    #import trunkroute
    GTotal = madeG(allrows)
    GG.append(GTotal)
    allnodedist = nx.all_pairs_dijkstra_path_length(GG[0])
    trunkui() #正式进入程序功能入口。

