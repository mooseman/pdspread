

#  pdspread.py  
#  A simple Python spreadsheet using curses.   
#  This code is released to the public domain. 

#  Note - The Control keys are as follows - 
#  'SOH', 'STX', 'ETX', 'EOT', 'ENQ', 'ACK', 'BEL', 'BS', 
#  'HT', 'LF', 'VT', 'FF', 'CR', 'SO', 'SI', 'DLE', 'DC1', 
#  'DC2', 'DC3', 'DC4', 'NAK', 'SYN', 'ETB', 'CAN', 'EM', 'SUB' 
#  
#   We use the following here -  
#  ^Q (Quit),  ^H (Backspace),  ^S(Save), ^A(save As),  
#  ^B (Left-arrow) ^F(Right-arrow), ^P(Up-arrow), ^N(Down-arrow)      


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
  def __init__(self): 
     self.maxrows = 100 
     self.maxcols = 50 
     self.curraddress = [1,1]
     self.next = None
     for y in range(1, self.maxrows): 
        for x in range(1, self.maxcols): 
           self.window.move(y, x) 
           if y == 1: 
              self.screen.addstr(y, x, str(y) )
           else: 
              self.screen.addstr(y, x, "" ) 
           if x == 1: 
              self.colname = chr(x+64) 
              self.screen.addstr(y, x, str(self.colname) ) 
           else: 
              self.screen.addstr(y, x, "" )               
                                   
  def move(self, key): 
     pass   # To be done              
     
             
myscreen = curses.initscr()
myscreen.border(0) 
myscreen.addstr(1, 25, "*** P.D. Editor ***") 

#  Create a new pad of 100 lines and 40 cols 
mypad = curses.newpad(100, 40) 
mywin = curses.newwin(20, 60, 0, 0) 

#  Do the column and row labels and set up the sheet 
#  Note - ord("A") = 65, ord("Z") is 90 
#  chr(65) = 'A' , chr(90) = 'Z' 




mywin.addstr(2, 1, "", curses.A_STANDOUT)

myeditor = curses.textpad.Textbox(mywin) 
myeditor.edit() 

mywin.refresh()
mywin.getch() 

a = sheet() 
a.__init__() 

curses.endwin()

