#C:\Users\XLXJ\anaconda3\envs\nodetrunk_37\python
#-= coding:utf-8 =-
__author__ = 'Rainbow'

import cmd
#import scprint
#import os
#import sys
#import tabulate


class nodetrunkinfo(cmd.Cmd):
    """Simple command processor example."""
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "Node&Trunk_3 Info:>> "    # define command prompt
    
    def do_listnode(self,line):
    	import listnode
    	listnode.nodelist()

    def do_nodefor(self,line):
    	import nodeforword
    	nodeforword.nodefor()

    def do_nodeforlist(self,line):
    	import nodeforwordlist
    	nodeforwordlist.nodeforlist()

    def do_route(self,line):
        import trunkroute
        trunkroute.startup()

    def do_nodeodf(self,line):
    	import nodeforodf
    	nodeforodf.nodeodf()
    	
    def do_yewu(self,line):
    	import servicesearch
    	servicesearch.searchsev()
    
    def do_odf(self,line):
    	import odfsearch
    	odfsearch.searchodf()

    def do_odfdl(sefl,line):
        import odfsearch
        odfsearch.searchodfdetial()

    def do_trunkd(slef,line):
    	import cabledetial
    	cabledetial.TrunkCableInfo()

    def do_Enter():
    	pass

    def do_nt(self, line):
        import scprint
        scprint.print('..................---===Thanks, Bye. ===---..................', color='DarkSeaGreen4', bcolor='Grey7')
        return True
    def do_NT(self, line):
        import scprint
        scprint.print('..................---===Thanks, Bye. ===---..................', color='DarkSeaGreen4', bcolor='Grey7')
        return True

if __name__ == '__main__':
    nodetrunkinfo().cmdloop()
