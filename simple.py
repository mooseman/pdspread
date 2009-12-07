

#  pdspread.py 
#  A simple spreadsheet.  

#  This code is released to the public domain.  

import sys, re, math, curses, curses.ascii, traceback, string, os 
   
# Helper functions to convert y,x coords to a column, row reference 
# and vice-versa. 
def yx2str(y,x):
    "Convert a coordinate pair like 1,26 to AA2"
    if x<26: s=chr(65+x)
    else:
	x=x-26
	s=chr(65+ (x/26) ) + chr(65+ (x%26) )
    s=s+str(y+1)
    return s
    
def x2str(x, width): 
    myval = int(x/width) 
    s=chr(65+myval)    
    return s     
    
coord_pat = re.compile('^(?P<x>[a-zA-Z]{1,2})(?P<y>\d+)$')

def str2yx(s):
    "Convert a string like A1 to a coordinate pair like 0,0"
    match = coord_pat.match(s)
    if not match: return None
    y,x = match.group('y', 'x')
    x = string.upper(x)
    if len(x)==1: x=ord(x)-65
    else:
	x= (ord(x[0])-65)*26 + ord(x[1])-65 + 26
    return string.atoi(y)-1, x

assert yx2str(0,0) == 'A1'
assert yx2str(1,26) == 'AA2'
assert str2yx('AA2') == (1,26)
assert str2yx('B2') == (1,1)
   
         
#  A spreadsheet class. This class also handles keystrokes  
class sheet(object):
    def __init__(self, scr): 
       self.scr = scr                       
       # Dictionary to store our data in.   
       self.data = {}           
       self.indexlist = [] 
       self.linelist = []            
       self.stuff = ""   
       self.width = 15  
       self.cursor = " " * self.width               
       
       # A variable to save the line-number of text. 
       self.win_y = self.win_x = 0  
       # The screen size (number of rows and columns). 
       (self.max_y, self.max_x) = self.scr.getmaxyx()
                        
       # Set up row and column headings 
       (y, x) = self.scr.getyx() 
       # Column headings 
       for x in range(7, self.max_x-1, self.width): 
          self.colhead = x2str(x, self.width)           
          self.scr.addstr(2, x, str(self.colhead), curses.A_STANDOUT) 
          self.scr.refresh() 
       # Row headings    
       for y in range(3, self.max_y-1): 
          self.rowhead = y-2 
          self.scr.addstr(y, 0, str(self.rowhead), curses.A_STANDOUT)           
          self.scr.refresh()    
       self.scr.move(3, 1)                     
       self.scr.refresh()                                                                                                                                                  
       curses.noecho() 
       self.scr.keypad(1)            
       self.scr.scrollok(1)
       self.scr.idlok(1)  
       self.scr.setscrreg(0, self.max_y-1)                                
       self.scr.refresh()	    
           
    def move(self, myy, myx): 
       self.cursor = ""
       (y, x) = self.scr.getyx() 
       if x > self.width+1:       
          self.scr.addstr(y, x-self.width, str(" " * self.width), curses.A_NORMAL)  
       else: 
          self.scr.addstr(y, 0, str(" " * self.width), curses.A_NORMAL)               
       self.scr.refresh() 
                                     
       self.scr.move(myy, myx)  
       (y, x) = self.scr.getyx() 
       if x > self.width+1:
          self.scr.addstr(y, x-self.width, str(" " * self.width), curses.A_STANDOUT)  
       else:    
          self.scr.addstr(y, 0, str(" " * self.width), curses.A_STANDOUT)  
       self.scr.refresh()                               
       
    def newmove(self, source, target): 
       (y, x) = self.scr.getyx()   
       source = yx2str(y, x) 
          
       
                                                                                                                                                                                                                             
    def action(self):  
       while (1): 
          (y, x) = self.scr.getyx()             
          #self.scr.addstr(y, x, str(self.cursor), curses.A_STANDOUT)                         
          curses.echo()                           
          c=self.scr.getch()		# Get a keystroke                                                                                  
          if c in (curses.KEY_ENTER, 10):  
             self.move(y-1, x)                                           
          elif c==curses.KEY_UP:  
             curses.noecho()                
             if y > 0:                 
                self.move(y-1, x)                                    
             elif y == 0 and self.win_y > 0:   
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
             if x > self.width + 1:                 
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
             self.scr.move(y, 0) 
             self.scr.refresh() 
          elif c==curses.KEY_END: 
             curses.noecho() 
             self.scr.move(y, 79) 
             self.scr.refresh()                                                            
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

