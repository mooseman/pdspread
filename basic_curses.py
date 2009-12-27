

#  pdspread.py 
#  A simple spreadsheet.  

# Acknowledgement: This code would not have been possible without 
# Andrew M. Kuchling's excellent "tabview.py" app. Some code from 
# that application is used here. Very many thanks to Andrew for 
# doing that application!   
# Also, *very many thanks* to those in pythonforum.org who have helped
# me with my questions there. In particular, Bill there supplied the
# code used in the num2str function here.
 
# This code is released to the public domain.  

import sys, re, types, itertools, math, curses, curses.ascii, traceback, string, os 
   

# A matrix class 
class matrix(object):
   def __init__(self, rows, cols):
       self.rows = rows
       self.cols = cols
       
       # initialize matrix and fill with zeroes
       self.matrix = []
       for i in range(rows):
           ea_row = []
           for j in range(cols):
               ea_row.append(0)
           self.matrix.append(ea_row)
  
   def setitem(self, row, col, v):
       self.matrix[row-1][col-1] = v
  
   def setrange(self, rows, cols, data):                     
       for x, y, z in zip(rows[0:1], cols[0:1], data):               
          self.setitem(x, y, z)                     
  
   def getitem(self, row, col):
       return self.matrix[row-1][col-1]
  
   def __repr__(self):
       outStr = ""
       for i in range(self.rows):
           outStr += 'Row %s = %s\n' % (i+1, self.matrix[i])
       return outStr
  
                                                       
#  A spreadsheet class. This class also handles keystrokes  
class sheet(matrix):
    def __init__(self, scr): 
       self.scr = scr                              
       curses.noecho() 
       self.scr.keypad(1)            
       self.scr.scrollok(1)
       self.scr.idlok(1)  
       self.scr.setscrreg(0, 22)    
       self.scr.move(2, 2)   
       self.scr.clrtoeol()                          
       self.scr.refresh()	    
          
    # This function moves the cell highlight. It restores the old cell 
    # to "normal" background, and highlights the new cell.             
    def do_matrix(self):        
       self.scr.move(2, 2)   
       self.scr.refresh()
       (y, x) = self.scr.getyx()    
       c = matrix(6, 6) 
       l = []
       colnums = range(65, 70)

       for x in colnums: 
          s = chr(x) 
          l.append(s) 

       c.setrange((1,2), (2,7), l)      

       rownums = range(1, 6)
       c.setrange((2,7), (1,2), rownums)      
                     
       self.scr.addstr(2, 0, str(c) )                      
       self.scr.refresh()                                                                                   
                                                                                                                                                                                                                                      
    def action(self):  
       while (1): 
          (y, x) = self.scr.getyx()            
          curses.echo()                           
          c=self.scr.getch()		# Get a keystroke                                                                                  
          if c in (curses.KEY_ENTER, 10):                
             pass                                     
          elif c==curses.KEY_F5: 
             (y, x) = self.scr.getyx()              
             self.do_matrix()
             #self.scr.addstr(y, x, "test")                     
             self.scr.refresh()                                    
          # Ctrl-G quits the app                  
          elif c==curses.ascii.BEL: 
             break                             
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

