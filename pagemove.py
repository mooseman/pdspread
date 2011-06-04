

#  pagemove.py  

import sys, re, types, itertools, math, curses, curses.ascii, traceback, string, os

# If cell has an x value of 0 and a cellx value of 1: 
#  Moving left is forbidden. Moving right uses standard 
#  move command. 
# If cell has an x value of 0 and a cellx value of > 1: 
#  There are still columns off the left of the screen. 
#  Scroll left, update the col headings and decrement the value of cellx.   
# If cell has an x value of 80 (no metter what cellx is): 
#  There are columns off the right of the screen. 
#  Scroll right, update the col headings and increment the value of cellx.   
# If cell has a y value of 0 and a celly value of 1:  
# Moving up is forbidden. Moving down uses the standard 
# move command.  
# If cell has a y value of 0 and a celly value of > 1: 
#  There are still rows off the top of the screen. 
#  Scroll up, update the row headings and decrement the value of celly.   
# If cell has a y value of MAX (no metter what celly is): 
#  There are rows off the bottom of the screen. 
#  Scroll down, update the row headings and increment the value of celly.   

class rowheads(object): 
   def __init__(self, data): 
      self.data = range(1, 29) 
      
   def update(self, inc):  
      for x in self.data: 
         x += inc 
         
   def display(self): 
      print self.data  
      

class colheads(object): 
   def __init__(self, data): 
      self.data = range(1, 12) 
      
   def update(self, inc):  
      for x in self.data: 
         x += inc 
         
   def display(self): 
      print self.data  
      
            

               





     


# Write a list of data into a range of cell positions. 
class myrange(object): 
    def __init__(self, xstart, xend, ystart, yend): 
       self.xstart = xstart
       self.xend = xend 
       self.ystart = ystart 
       self.yend = yend 
       
       
       
       
    
    def write_range(datalist, poslist, attr=None, align=None): 
       self.datalist = [] 
       self.poslist = poslist    
       # Apply alignment (if any) 
       if align == None: 
          for x in datalist: 
             self.datalist.append(x) 
       elif align == "center": 
          for x in datalist: 
             self.datalist.append(str(x).center(self.width)) 
       else: 
          pass                   
       # Get the position of the cursor. 
       (y, x) = self.scr.getyx() 
       # Write the text, applying the attribute (if used) 
       if attr == None: 
          for x,y in zip(self.datalist, self.poslist): 
             self.scr.addstr(y[0], y[1], str(x) ) 
       else:   
          for x,y in zip(self.datalist, self.poslist):         
             self.scr.addstr(y[0], y[1], str(x), attr ) 
       # Refresh the screen 
       self.scr.refresh()                                                                  
   
   
   
   #  A spreadsheet class. 
class sheet(cell):
    def __init__(self, scr): 
       # Do all of the curses stuff first.  
       self.scr = scr   
       (y, x) = self.scr.getyx()                            
       curses.noecho() 
       self.scr.keypad(1)            
       self.scr.scrollok(1)
       self.scr.idlok(1) 
       # Just added leaveok. 
       self.scr.leaveok(0)                      
       self.scr.setscrreg(0, 28) 
            
    # Row headings 
       self.scr.move(3, 0)         
       self.rowheads = list(range(1,29))  
       self.plist = list( (y,x) for y in range(3, 31) for 
          x in range(0, 1) )
       self.cell.write_range(self.rowheads, self.plist, 
            curses.A_STANDOUT, "center")  
       self.scr.refresh() 	         
   




