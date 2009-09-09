




import sys, curses, curses.ascii, curses.textpad, traceback, string, os

#  A cell class 
class cell(object): 
  def __init__(self): 
     self.data = self.row = self.col = None 
     self.width = 8 
     self.height = 2 
     
  def add(self, data): 
     self.data = data      
     
  def display(self): 
     print self.data      
     
#  A sheet class 
class sheet(cell):  
  def setup(self): 
     self.maxrows = 20 
     self.maxcols = 10 
     self.curraddress = [1,1]
     self.next = None
     for y in range(1, self.maxrows): 
        for x in range(1, self.maxcols):            
           if y == 1: 
              print str(y) 
           else: 
              print "" 
           if x == 1: 
              self.colname = chr(x+64) 
              print self.colname  
           else: 
              print "" 
                                   
  def move(self, key): 
     pass   # To be done              


# Test the code 
a=sheet() 
a.setup()  



