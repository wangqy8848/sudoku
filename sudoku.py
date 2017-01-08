#!/usr/bin/python
#coding=utf-8 
import sys
class sudoku(object):
    def __init__(self,filename=""):
        self.filename = filename
        self.numlist = [0]*81
        self.ready_flag = False
        self.change_flag = False
        self.cache_row={}
        self.cache_col={}
        self.cache_blk={}
        self.complate_num=0
    def clear_cache(self):
        self.cache_row={}
        self.cache_col={}
        self.cache_blk={}
        for i in range(1,10):
            self.cache_row[i]={}
            self.cache_col[i]={}
            self.cache_blk[i]={}
    def topline(self):
        print('┌───┬───┬───┬───┬───┬───┬───┬───┬───┐')
    def midline(self):
        print('├───┼───┼───┼───┼───┼───┼───┼───┼───┤')
    def butline(self):
        print('└───┴───┴───┴───┴───┴───┴───┴───┴───┘')
    def numline(self,numlist):
        print('│'),
        for i in numlist:
            if i!=0:
                print('%d │'%i),
            else:
                print('  │'),
        print("")
    def show(self):
        self.topline()
        for i in range(8):
            self.numline(self.numlist[i*9:(i*9+9)])
            self.midline()
        self.numline(self.numlist[72:81])
        self.butline()
    def set_val(self,row,col,val):
        self.numlist[(row-1)*9+col-1]=val
    def set_val2(self,ncount,val):
        self.numlist[ncount-1]=val
        #self.show()
    def numlist_check(self):
        numcount = 1
        for i in self.numlist:
            if i<0 or i>9:
                print("num row(%d) col(%d) value (%d) is illegal."%(numcount/9+1,numcount%9,int(i)))
                return False
            elif i!=0:
                self.complate_num=self.complate_num+1
                
        if len(self.numlist)!=81:
            print("the count of numlist (%d) is illegal."%len(self.numlist))
            return False
        return True
    def get_puzzle(self,filename=""):
        if not filename:
            filename=self.filename
        fp=open(filename)
        readlist = fp.read().split()
        fp.close()
        try:
            self.numlist = [int(i) for i in readlist]
        except Exception,e:
            print e
            return False
        if self.numlist_check():
            print("input puzzle sucess, ready to compute.complate %d/81."%self.complate_num)
            self.ready_flag = True
        self.show()
        
        
    def get_col(self,col):
        return [self.numlist[i*9+col-1] for i in range(9)]
    def get_row(self,row):
        return self.numlist[(row-1)*9:row*9]
    def get_blk(self,blk):
        blk_row = (blk-1)/3
        blk_col = (blk-1)%3
        res=self.numlist[blk_row*3*9+blk_col*3:blk_row*3*9+blk_col*3+3]
        res=res+ self.numlist[blk_row*3*9+9+blk_col*3:blk_row*3*9+9+blk_col*3+3]
        res=res+ self.numlist[blk_row*3*9+18+blk_col*3:blk_row*3*9+18+blk_col*3+3]
        return res
    
    def get_site(self,num):
        row = (num-1)/9+1
        col = (num-1)%9+1
        blk = (row-1)/3*3+(col-1)/3+1
        return row,col,blk
    def compute(self,i,val):
        if val != 0:
            return
        else:
            r,c,b = self.get_site(i)
            rlist=self.get_row(r)
            clist=self.get_col(c)
            blist=self.get_blk(b)
            baselist=list(set(rlist+clist+blist))
            baselist.remove(0)
            #print baselist
            a=range(1,10)
            tobelist=list(set(a)-set(baselist))
            return tobelist
    def complate_puzzle(self):
        self.clear_cache()
        if not self.ready_flag:
            print("puzzle not ready, cant do that.")
            return False
        self.change_flag = True
        while(self.change_flag):
            numcount=1
            self.clear_cache()
            print("computing... %d/81 complated."%self.complate_num)
            if self.complate_num>=81:
                self.show()
                break
            self.change_flag = False
            for val in self.numlist:
                if val!=0:
                    numcount=numcount+1
                    continue
                tobe = self.compute(numcount,val)
                r,c,b = self.get_site(numcount)
                self.cache_row[r][numcount]=tobe
                self.cache_col[c][numcount]=tobe
                self.cache_blk[b][numcount]=tobe
                if len(tobe)==1:
                    self.change_flag=True
                    self.set_val(r,c,tobe[0])
                    self.complate_num=self.complate_num+1
                #print("r %d, c %d, b %d to be %s"%(r,c,b,str(tobe)))
                numcount=numcount+1
            if self.change_flag:
                continue
            for i in range(1,10):
                for c,cval in self.cache_row[i].iteritems():
                    cmpcache = []
                    for other,cmpval in self.cache_row[i].iteritems():
                        if other == c:
                            continue
                        else:
                            cmpcache = list(set(cmpcache+cmpval))
                    c_tobe = list(set(cval)-set(cmpcache))
                    #print("row %d, count %d, c_tobe %s"%(i,c,c_tobe))
                    if len(c_tobe)==1:
                        #print("row %d, count %d, c_tobe %s"%(i,c,c_tobe))
                        #print("seting value,row %d count %d, c_tobe %d"%(i,c,c_tobe[0]))
                        self.set_val2(c,c_tobe[0])
                        self.complate_num=self.complate_num+1
                        self.change_flag=True
            if self.change_flag:
                continue        
            for i in range(1,10):
                for c,cval in self.cache_col[i].iteritems():
                    cmpcache = []
                    for other,cmpval in self.cache_col[i].iteritems():
                        if other == c:
                            continue
                        else:
                            cmpcache = list(set(cmpcache+cmpval))
                    c_tobe = list(set(cval)-set(cmpcache))
                    #print("col %d, count %d, c_tobe %s"%(i,c,c_tobe))
                    if len(c_tobe)==1:
                        self.set_val2(c,c_tobe[0])
                        self.complate_num=self.complate_num+1
                        self.change_flag=True
            if self.change_flag:
                continue           
            for i in range(1,10):
                for c,cval in self.cache_blk[i].iteritems():
                    cmpcache = []
                    for other,cmpval in self.cache_blk[i].iteritems():
                        if other == c:
                            continue
                        else:
                            cmpcache = list(set(cmpcache+cmpval))
                    c_tobe = list(set(cval)-set(cmpcache))
                    #print("blk %d, count %d, c_tobe %s"%(i,c,c_tobe))
                    if len(c_tobe)==1:
                        self.set_val2(c,c_tobe[0])
                        self.complate_num=self.complate_num+1
                        self.change_flag=True            
                            
def main():
    print("hello")
    mysudo=sudoku()

    mysudo.get_puzzle(sys.argv[1])
    
    mysudo.complate_puzzle()

if __name__=="__main__":
    main()