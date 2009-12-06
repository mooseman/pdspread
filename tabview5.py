#!/usr/local/bin/python

# tabview.py -- View a tab-delimited file in a spreadsheet-like display.
# Contributed by A.M. Kuchling <amk@amk.ca>
# 
# *******************************************************************
# Minor modification by mooseman (Andy Elvey) 
# The only mod that I've made was to put the cursor key names in 
# upper case, as they were not previously working for me (on Linux 
# anyway). 
# Acknowledgement - tabview.py was in AMK's "unmaintained" area and he 
# has very kindly agreed that I can "adopt" it. So, it now has a 
# home on my Git repo here. 
# Very many thanks to AMK for creating tabview.py - one of the neatest 
# and best Python (and curses) apps that I've seen! 

# He has also confirmed that this code is in the public domain. 
#********************************************************************

# The tab-delimited file is displayed on screen.  The highlighted
# position is shown in the top-left corner of the screen; below it are
# shown the contents of that cell.
#
#  Movement keys are:
#    Cursor keys: Move the highlighted cell, scrolling if required.
#    Q or q     : Quit
#    TAB        : Page right a screen
#    Home       : Move to the start of this line
#    End        : Move to the end of this line
#    PgUp/PgDn  : Move a page up or down
#    Insert     : Memorize this position
#    Delete     : Return to memorized position (if any)
#
# TODO : 
#    A 'G' for Goto: enter a cell like AA260 and move there
#    A key to re-read the tab-delimited file
#
# Possible projects:
#    Allow editing of cells, and then saving the modified data
#    Add formula evaluation, and you've got a simple spreadsheet
# program.  (Actually, you should allow displaying both via curses and
# via a Tk widget.)  
#

import curses, re, string, curses.ascii, curses.textpad, traceback, os

def yx2str(y,x):
    "Convert a coordinate pair like 1,26 to AA2"
    if x<26: s=chr(65+x)
    else:
	x=x-26
	s=chr(65+ (x/26) ) + chr(65+ (x%26) )
    s=s+str(y+1)
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

	
class keyhandler:
    def __init__(self, scr, filename="", column_width=20):
        self.scr = scr
        self.scr.keypad(1) 
        self.scr.scrollok(1)
        self.scr.idlok(1)             
        self.filename = filename         
        self.column_width = column_width
        f=open(filename, 'r')
        self.data = [] 
        self.stuff = "" 
        self.mytext = None 
        
        if filename != "": 
           while (1): 
              L=f.readline()
              if L == "": 
                 break 
              self.data.append( string.split(L, '\t') ) 
              self.x, self.y = 0,0 
              self.win_x, self.win_y = 0,0 
              self.max_y, self.max_x = self.scr.getmaxyx()
              self.num_columns = int(self.max_x/self.column_width)
              #self.scr.clear()	
              self.action()                     
              self.scr.refresh()
        else: 
           while (1): 
              self.action()                     
              self.scr.refresh()


    # This is simply the action done when the End key is pressed. 
    def move_to_end(self):	
       yp=self.y+self.win_y ; xp=self.x+self.win_x 
       if len(self.data)<=yp: end=0    
       else: end=len(self.data[yp])-1
	
	   # If the end column is on-screen, just change the
	   # .x value appropriately.
       if self.win_x <= end < self.win_x + self.num_columns:
           self.x = end - self.win_x
       else:
           if end<self.num_columns:
              self.win_x = 0 ; self.x = end
           else:
              self.x = self.num_columns-1
              self.win_x = end-self.x 
        
        
    # Set the string to be displayed in a cell.          
    def set_string(self):  
       (y, x) = self.scr.getyx()  
       yp=y+self.win_y ; xp=x+self.win_x
       if len(self.data)<=yp: self.s=""
       elif len(self.data[yp])<=xp: self.s=""
       else: self.s=self.data[yp][xp]
       self.s = string.ljust(self.s, 15)[0:15]
                             
    # Code needed to set up the sheet.     
    # This is what actually makes the app a spreadsheet instead of a 
    # text-editor.  
    def do_sheet(self):	
       self.scr.addstr(0,0, 
			yx2str(self.y + self.win_y, self.x+self.win_x)+'    ',
			curses.A_REVERSE)

       for y in range(0, self.max_y-3):
           self.scr.move(y+2,0) ; self.scr.clrtoeol()
           for x in range(0, int(self.max_x / self.column_width) ):
              self.scr.attrset(curses.A_NORMAL)
              self.set_string() 
                                          
              if x==self.x and y==self.y: self.scr.attrset(curses.A_STANDOUT)
              self.scr.addstr(y+2, x*self.column_width, self.s)

       self.set_string()         
       self.scr.move(1,0) ; self.scr.clrtoeol()
       self.scr.addstr(self.s[0:self.max_x])
       self.scr.refresh()
       

    def action(self): 
       while (1): 
          curses.echo()            
          self.scr.keypad(1) 
          self.do_sheet()             
          stdscr.move(self.y+2, self.x*self.column_width)     # Move the cursor
          c=stdscr.getch()		# Get a keystroke
          if 0<c<256:           
              curses.echo() 
              (y, x) = self.scr.getyx()  
              c=chr(c)   
              self.stuff += c 
              self.scr.addstr(y, x, str(self.stuff))               
              self.scr.refresh()             
          # Arrow keys
          elif c==curses.KEY_UP:
              curses.noecho()               
              if self.win_y>0: self.win_y = self.win_y - 1
              else: self.y=self.y-1
              self.scr.refresh()                  
          elif c==curses.KEY_DOWN:
             curses.noecho()  
             if self.y < self.max_y-3 -1: self.y=self.y+1
             else: self.win_y = self.win_y+1
             self.scr.refresh()
          elif c==curses.KEY_LEFT:
             curses.noecho()                
             if self.win_x>0: self.win_x = self.win_x - 1
             else: self.x=self.x-1
             self.scr.refresh()
          elif c==curses.KEY_RIGHT:
             curses.noecho()   
             if self.x < int(self.max_x/self.column_width)-1: self.x=self.x+1
             else: self.win_x = self.win_x+1
             self.scr.refresh()
          # Home key moves to the start of this line
          elif c==curses.KEY_HOME:
             curses.noecho()   
             self.win_x = self.x = 0
             self.scr.refresh()
          # End key moves to the end of this line
          elif c==curses.KEY_END:
             curses.noecho()   
             self.move_to_end()
             self.scr.refresh()

          # PageUp moves up a page
          elif c==curses.key_PPAGE:
             curses.noecho()   
             self.win_y = self.win_y - (self.max_y - 2)
             if self.win_y<0: self.win_y = 0
             self.scr.refresh()
          # PageDn moves down a page
          elif c==curses.key_NPAGE:
             curses.noecho()   
             self.win_y = self.win_y + (self.max_y - 2)
             if self.win_y<0: self.win_y = 0
             self.scr.refresh()	
          # Insert memorizes the current position
          elif c==curses.key_IC:
             curses.noecho()   
             self.save_y, self.save_x = self.y + self.win_y, self.x + self.win_x
          # Delete restores a saved position
          elif c==curses.key_DC:
             curses.noecho()   
             if hasattr(self, 'save_y'):
                self.x = self.y = 0
                self.win_y, self.win_x = self.save_y, self.save_x
                self.scr.refresh()
             else: 
                stdscr.addstr(0,50, curses.keyname(c)+ ' pressed')
                stdscr.refresh()
                pass 
          # Ctrl-G quits the app                  
          elif c==curses.ascii.BEL: 
             curses.noecho()  
             break       
        
        
        
def main(stdscr):
    import string, curses, curses.ascii, sys

    if len(sys.argv)==1:
	print 'Usage: tabview.py <filename>'
	return
    filename=sys.argv[1]
    # Clear the screen and display the menu of keys
    stdscr.clear()
    file = keyhandler(stdscr, filename)        
    file.action() 
    
    
if __name__=='__main__':
    import curses, traceback
    try:
	# Initialize curses
	stdscr=curses.initscr()    
	# Turn off echoing of keys, and enter cbreak mode,
	# where no buffering is performed on keyboard input
	curses.noecho() ; curses.cbreak()

	# In keypad mode, escape sequences for special keys
	# (like the cursor keys) will be interpreted and
	# a special value like curses.key_left will be returned
	stdscr.keypad(1)
	main(stdscr)			# Enter the main loop
	# Set everything back to normal
	stdscr.keypad(0)
	curses.echo() ; curses.nocbreak()
	curses.endwin()			# Terminate curses
    except:
        # In the event of an error, restore the terminal
	# to a sane state.
	stdscr.keypad(0)
	curses.echo() ; curses.nocbreak()
	curses.endwin()
	traceback.print_exc()		# Print the exception
    


