

#  pdspread.py 
#  A simple spreadsheet.  

# Acknowledgement: This code would not have been possible without 
# Andrew M. Kuchling's excellent "tabview.py" app. Some code from 
# that application is used here. Very many thanks to Andrew for 
# doing that application!   

#  This code is released to the public domain.  

import sys, re, types, itertools, math, curses, curses.ascii, traceback, string, os 
   
# Helper functions to convert y,x coords to a column, row reference 
# and vice-versa. 
def yx2str(y,x, width):
    "Convert a coordinate pair like 1,26 to AA2"    
    if int(x/width)<26: s=chr(65+int(x/width))
    else:
	x=x-26
	s=chr(65+ (x/26) ) + chr(65+ (x%26) )
    s=s+str(y)
    return s
    
def colnum2str(x): 
    if x<26: s=chr(65+x)
    else:
	x=x-26
	s=chr(65+ (x/26) ) + chr(65+ (x%26) )    
    return s    
        
def x2str(x, width): 
    myval = int(x/width) 
    s=chr(65+myval)    
    return s     
    
coord_pat = re.compile('^(?P<x>[a-zA-Z]{1,2})(?P<y>\d+)$')


# NOTE - We want to convert this function so that it can give a 
# position for any cell reference. 
# A sheet has columns with the properties of name, width and position. 
# We also have values for numcols - this is the number of cols that can
# be fitted onto the page, given their current width. 
# It is the width of the screen divided by the default column width.

# Each individual column can have a width associated with it. 
# The position of a column can therefore be found like this - 

# Col. A. Is *always* located at x=8. (Remember that the first few cols 
# are needed for the row headings). It will have a width (which can very). 
# So we have Col. A at x=8, and it has a width of (say) 7. 
# Col. B will be at x=(8 plus the current width of col. A) So, col B 
# will ALWAYS be at x=(8 plus width(column A). So, B is at 15 in this example. 
# Col. C will ALWAYS be at x=(8 plus the current widths of 
# cols. A and B)  
# Col. D will be at x=(8 plus the current width of cols. A, B and C)  
# .... and so on.  

def str2yx(s):    
    "Convert a string like A1 to a coordinate pair like 0,0"
    match = coord_pat.match(s)
    if not match: return None
    y,x = match.group('y', 'x')
    x = string.upper(x)
    if x == "A": width = 0
    else: width = 7    
    if len(x)==1: x=ord(x)-58 + ( (ord(x)-65) * width) 
    else:
	x= (ord(x[0])-58+width)*26 + ord(x[1])-58+width + 26
    return string.atoi(y)+1, x

#assert yx2str(2,1,7) == 'A1'
#assert yx2str(3,27,7) == 'D2'
#assert str2yx('AA2') == (1,26)
#assert str2yx('B2') == (1,1)
  
   
# This code snippet will help in getting the data storage set up.          
# >>> d = {"foo": [43, 17, 68],  "bar": ["test", "this", "stuff"], 
#   "baz": [98, 123, 892, 50]}
# >>> d["foo"]
# [43, 17, 68]
# >>> d["foo"][0]
# 43
# >>> d["foo"][1]
# 17

# NOTE! THE WINDOW.CHGAT FUNCTION IS EXTREMELY USEFUL. IT APPLIES AN 
# ATTRIBUTE TO A SELECTED RANGE OF CELLS.  
                  
#  A spreadsheet class. This class also handles keystrokes  
class sheet(object):
    def __init__(self, scr): 
       self.scr = scr                       
       # Dictionary to store our data in.   
       self.biglist = [] 
       # The position of A1, the "origin". All cells are positioned with 
       # reference to this. 
       self.origin = (2,9)
       # The position of the cell highlight. This is shown at the 
       # top-left of the screen. 
       self.width = 7  
        
       (y, x) = self.scr.getyx()           
       self.pos = yx2str(y, x, self.width) 
              
       self.data = {}           
       self.indexlist = [] 
       self.linelist = [] 
       self.stuff = "" 
       # The position list 
       self.poslist = [] 
       
       # These lists have the ACTUAL headings (which INCLUDE the 
       # spaces! ) 
       self.rowheadlist = []
       self.colheadlist = []                   
       
       # These lists have the NAMES of the headings (which EXCLUDE the 
       # spaces! ) 
       self.rowheadnames = []
       self.colheadnames = []
              
       # A variable to save the line-number of text. 
       self.win_y = self.win_x = 0  
       # The screen size (number of rows and columns). 
       (self.max_y, self.max_x) = self.scr.getmaxyx()
          
       # calculate the number of columns 
       # We subtract self.width to cater for the width of the row headings
       self.numcols = int((self.max_x-self.width)/self.width)   
          
       #for x in range(1, self.max_x-self.width, self.width): 
       for x in range(0, self.numcols): 
          #self.colheadname = x2str(x, self.width) 
          self.colheadname = colnum2str(x) 
          self.colheadnames.append(self.colheadname)         
       # Start at 3 to make room for the edit line and cell highlight
       # at the top of the screen.    
       for y in range(1, self.max_y-2): 
          self.rowheadname = str(y) 
          self.rowheadnames.append(self.rowheadname)            
       for c in list(itertools.product(self.colheadnames, self.rowheadnames)): 
          d = str(c[0]+c[1]) 
          self.poslist.append(str2yx(d)) 
          self.biglist.append(d) 
       # The dict holds the following data (in this order) - 
       # Key - cell name 
       # Values - cell name, cell (y,x) position, contents, value of contents 
       # (for formulas - this is the formula value), format, colour, font, 
       # font-size.    
       # Position of cell A1 is at (2,7). We can move to other columns by
       # moving by the width of the current column.
       self.origin = (2,7)
                                                                  
       for a, b in zip(self.biglist, self.poslist):    
          self.data.update({a: [a, b, None, None, 
                    None, None, None]})               
          
                                                                                 
       for x in range(7, self.max_x-self.width, self.width): 
          self.colheadname = x2str(x-6, self.width)
          self.colhead = x2str(x-6, self.width).center(self.width)   
          self.colheadlist.append(self.colhead)    
          self.colheadnames.append(self.colheadname)        
          self.scr.addstr(1, x, str(self.colhead), curses.A_STANDOUT) 
          (y, x) = self.scr.getyx()           
          self.scr.refresh() 
                              
       # Row headings    
       for y in range(2, self.max_y-1): 
          self.rowheadname = str(y-1)
          self.rowhead = str(y-1).center(self.width)    
          self.rowheadlist.append(self.rowhead)        
          self.rowheadnames.append(self.rowheadname)        
          self.scr.addstr(y, 0, str(self.rowhead), curses.A_STANDOUT) 
          (y, x) = self.scr.getyx() 
          self.cell = yx2str(y, x, self.width) 
          self.data.update({self.cell: [self.cell, None, None, None, None]})            
          
          self.scr.addstr(0, 0, str(self.pos), curses.A_REVERSE)                    
          self.scr.refresh()                                         
       
       # Move to cell A1 - This is at (2, 9).                     
       self.scr.move(2, 7) 
       (y, x) = self.scr.getyx() 
       self.scr.chgat(y, x, self.width, curses.A_STANDOUT)                      
       # Move cursor to start of cell. 
       #self.scr.move(2, 10) 
       self.scr.refresh()                                                                                                                                                  
       curses.noecho() 
       self.scr.keypad(1)            
       self.scr.scrollok(1)
       self.scr.idlok(1)  
       self.scr.setscrreg(0, self.max_y-1)                                
       self.scr.refresh()	    
          
    # This function moves the cell highlight. It restores the old cell 
    # to "normal" background, and highlights the new cell.             
    def move(self, myy, myx):        
       (y, x) = self.scr.getyx()        
       self.scr.chgat(y, x, self.width, curses.A_NORMAL)                      
       self.scr.refresh() 
                                     
       self.scr.move(myy, myx)  
       (y, x) = self.scr.getyx() 
       self.scr.chgat(y, x, self.width, curses.A_STANDOUT)    
       self.scr.refresh()                   
       (y, x) = self.scr.getyx()    
       self.scr.addstr(0, 0, yx2str(y, x, curses.A_REVERSE) )            
       self.scr.move(myy, myx)  
       self.scr.refresh()                               
              
    # Highlight the currently-active cell    
    def highlight(self): 
       (y, x) = self.scr.getyx() 
       self.cursorstart = (y, x) 
       self.cursorend = (y, x+self.width)
       self.scr.attrset(curses.A_STANDOUT) 
       self.scr.refresh()                               
       #self.scr.addstr(y, x, str(" " * self.width), curses.A_STANDOUT)  
                                   
    def test(self): 
       (y, x) = self.scr.getyx()
       test = str( str(y) + "," + str(x) )
       #self.scr.addstr(y, x, str(self.data["A1"][1]) )  
       self.scr.addstr(y, x, str(self.poslist[0:4]) )  
       self.scr.addstr(y+1, x, str(self.biglist[0:4]) )  
       self.scr.addstr(y+2, x, str(test) )  
       
       '''if self.data.has_key(test): 
          self.scr.addstr(y, x, str(self.data[test][1]) )  
       else: 
          pass '''                                                 
              
    def test2(self): 
       (y, x) = self.scr.getyx()  
       for k in self.data.keys(): 
       #for k, v in self.data.items(): 
          self.scr.addstr(y, x, str(k) )  
          y + 1  
          (y, x) = self.scr.getyx()        
          self.scr.refresh()          
          
    def test3(self): 
       (y, x) = self.scr.getyx()  
       mydata = str2yx("E12") 
       self.scr.addstr(y, x, str(mydata) )  
                           
          
    def showpos(self): 
       (y, x) = self.scr.getyx()                       
       self.scr.addstr(0, 0, yx2str(y, x, curses.A_REVERSE) )         
                                             
    def putdata(self, myy, myx, mydata):     
       self.scr.move(myy, myx)  
       (y, x) = self.scr.getyx()    
       #self.width = 20                   
       self.posname = yx2str(y, x, self.width) 
       # Try window.chgat([y, x][, num], attr) 
       # THIS WORKS!! IT HIGHLIGHTS (OR PUTS BACK TO NORMAL) 
       # A SELECTED AREA!  
       self.scr.chgat(y, x, 10, curses.A_STANDOUT) 
       self.mydata = mydata        
       self.scr.addstr(y, x, str(self.mydata) )         
       self.scr.refresh()  
       #self.cursorend = (y, x+self.width)
       #self.thiscell.attrset(curses.A_STANDOUT) 
       #self.mydata = 123        
       #self.scr.refresh()  
         
                                                                                                                                                                                                                             
    def action(self):  
       while (1): 
          (y, x) = self.scr.getyx()            
          curses.echo()                           
          c=self.scr.getch()		# Get a keystroke                                                                                  
          if c in (curses.KEY_ENTER, 10):                
             curses.noecho()  
             self.scr.chgat(y, x, self.width, curses.A_NORMAL)                                  
             self.move(y+1, x)                 
             self.scr.refresh()                                                                                                        
          elif c==curses.KEY_UP:  
             curses.noecho()                
             if y > 2:                 
                self.move(y-1, x)                                    
             elif y == 2 and self.win_y > 0:   
                self.scr.scroll(-1)                   
                self.move(y, x)                  
             else: 
                pass                                                                                     
             self.scr.refresh()
          elif c==curses.KEY_DOWN:
             curses.noecho()   
             (y, x) = self.scr.getyx()           
             if y < self.max_y-1:                    
                self.move(y+1, x)                   
                self.scr.refresh()                                                                 
             else:                                          
                self.scr.scroll(1)                                 
                self.move(y, x)                  
             self.scr.refresh()   
          elif c==curses.KEY_LEFT: 
             curses.noecho()  
             if x >= 7 + self.width:                 
                self.move(y, x-self.width) 
             else: 
                pass 
             self.scr.refresh()
          elif c==curses.KEY_RIGHT: 
             curses.noecho() 
             if x < self.max_x-self.width-1:                 
                self.move(y, x+self.width) 
             else: 
                pass                 
             self.scr.refresh() 
          elif c==curses.KEY_HOME: 
             curses.noecho() 
             self.scr.move(y, 8) 
             self.scr.refresh() 
          elif c==curses.KEY_END: 
             curses.noecho() 
             self.scr.move(y, self.max_x - self.width-1) 
             self.scr.refresh()  
          elif c==curses.KEY_F5: 
             (y, x) = self.scr.getyx() 
             self.test = yx2str(y, x, self.width) 
             self.scr.addstr(y, x, str(self.test))                     
             self.scr.refresh()  
          elif c==curses.KEY_F6: 
             (y, x) = self.scr.getyx() 
             self.test = yx2str(y, x, self.width) 
             self.scr.addstr(y, x, str(self.rowheadnames))                     
             self.scr.refresh()  
          elif c==curses.KEY_F7: 
             self.test() 
          elif c==curses.KEY_F8: 
             self.putdata(10, 30, "This is a test!")    
             
             
             #self.test2()                    
          # Ctrl-G quits the app                  
          elif c==curses.ascii.BEL: 
             break      
          # Ctrl-A prints the data in the dict 
          elif c==curses.ascii.SOH:               
             (y, x) = self.scr.getyx()   
             self.scr.addstr(y, x, str(self.myval) )               
             self.scr.refresh() 
             #self.pagedowntemp() 
             #self.print_ys()                            
             #self.displaydict()    
             #self.displaylists()                        
          elif 0<c<256:               
             c=chr(c)   
             if x < self.max_x-2:  
                self.stuff += c                           
             else:                 
                pass 
             
                          
#  Main loop       
def main(stdscr):  
    a = sheet(stdscr)          
    a.action() 
                                   
#  Run the code from the command-line 
if __name__ == '__main__':  
  try: 
     stdscr = curses.initscr()   
     #curses.start_color()      
     curses.noecho() ; curses.cbreak()
     stdscr.keypad(1)
     main(stdscr)      # Enter the main loop
     # Set everything back to normal
     stdscr.keypad(0)
     curses.echo() ; curses.nocbreak()
     curses.endwin()  # Terminate curses
  except:
     # In the event of an error, restore the terminal
     # to a sane state.
     stdscr.keypad(0)
     curses.echo() ; curses.nocbreak()
     curses.endwin()
     traceback.print_exc()  # Print the exception

