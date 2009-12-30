

#  pdspread.py 
#  A simple spreadsheet.  

# This code is released to the public domain.  

# Acknowledgement: This code would not have been possible without 
# Andrew M. Kuchling's excellent "tabview.py" app. Some code from 
# that application is used here. Very many thanks to Andrew for 
# doing that application!   
# Also, very many thanks to those in pythonforum.org who have helped
# me with my questions there. In particular, Bill there supplied the
# code used in the num2str function here. 
# Many thanks also to "bvdet" from bytes.com. The matrix code in this 
# app is based on the code that he posted here -  
# http://bytes.com/topic/python/answers/594203-please-how-create-matrix-python
 

import sys, re, types, itertools, math, curses, curses.ascii, traceback, string, os 
   
# A cell class. This has left and top boundaries. These are the leftmost 
# column and the topmost row. We will make the defaults 2 for lbound and 
# 2 for tbound. Coords is a tuple of the coordinates of the cell. 
# This is in the form (row, col).    
class cell(object): 
    def __init__(self, scr, lbound, tbound, coords): 
       self.scr = scr
       self.lbound = lbound 
       self.tbound = tbound    
       self.coords = coords
       self.row = self.coords[0]
       self.col = self.coords[1]
       # Methods to store the cells bordering this cell. 
       self.left = self.right = self.above = self.below = None 
       # Store data 
       self.data = {} 
       # A cell's name (e.g. E5)  
       self.addr = None 
       # A cell's position (e.g. 7, 28) 
       self.pos = None 
       # Set up the appearance of the cell
       self.width = 7
       self.scr.chgat(self.row, self.col, self.width, curses.A_STANDOUT)    
       self.scr.refresh()                   
       
    # Set a given attribute    
    def set(self, attr, val): 
       setattr(self, attr, val)  
                     
    def move(self, name): 
       self.scr.move(name[0], name[1]) 
       self.scr.refresh() 
                                  
    def display(self, attr): 
       (y, x) = self.scr.getyx()           
       strattr = str(getattr(self, attr)) 
       self.scr.addstr(y, x, str(strattr) )       
      
                
# A matrix class 
class matrix(cell):
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
       cells = list(itertools.product(range(rows[0], rows[1]), 
          range(cols[0], cols[1]) ) ) 
       mydata = list(data)    
       mylist = zip(cells, mydata)       
       for x in mylist:
           self.setitem(x[0][0], x[0][1], x[1])                    
       
   def getitem(self, row, col):
       return self.matrix[row-1][col-1]
  
   def __repr__(self):
       outStr = ""
       for i in range(self.rows):
           outStr += str(self.matrix[i]) + "\n"   
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
       # Set the default column width. 
       self.colwidth = 7        
       # Move to the origin. 
       self.scr.move(0, 0)                
       # Create a cell
       self.cell = cell(self.scr, 1, 1, (1,7))         
       self.scr.refresh()	                         
       
       # Create a matrix for the column and row headings. 
       a = matrix(21,11) 
       self.colheads = list(chr(x) for x in range(65,76)) 
       self.rowheads = list(range(1,21))  
       a.setrange((1,2), (2,12), self.colheads)      
       a.setrange((2,22), (1,2), self.rowheads)   
       # Another matrix for the cell coordinates. 
       b = matrix(8,5) 
       coords = list(itertools.product(range(0, 8), 
          range(0, 5) ) ) 
       b.setrange((1,9), (1,6), coords)   
       # A third matrix for cell names ("C5", "C6", ...)  
       # This matrix has 7 rows and 5 cols. It contains the cell names 
       # "A1" to "G5"       
       c = matrix(7,5)                      
       # Doing the cell names like this ensures that we get the 
       # transpose of what itertools.product would give us (which is 
       # not what we want here). 
       cellnames = list( str(y + str(x)) for x in self.rowheads[0:7] for 
          y in self.colheads[0:5])                             
       c.setrange( (1,8), (1,6), cellnames) 
       # A matrix for the initial cells and their (y,x) coordinates. 
       d = matrix(7,5) 
       coords = list( (y,x) for y in range(0,7) for x in range(0, 
           5*self.colwidth, self.colwidth) ) 
       d.setrange( (1,8), (1,6), coords)   
                                                        
       '''b = matrix(21,11) 
       coords = list(itertools.product(range(0, 22), 
          range(0, 11) ) ) 
       b.setrange((1,22), (1,11), coords) '''   
       
       # Display the matrix. Note - at present, this only displays the
       # matrix as a text string. We need to display the "live" matrix 
       # so that we can interact with it.    
       #self.scr.addstr(0, 0, str(a) )                      
       #self.scr.addstr(0, 0, str(d) )                      
       #self.cell.move((12, 40))       
       self.scr.refresh()	    
          
    def move(self, dir):
       pass           
          
          
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
       
       stuff = ["The", "quick", "brown", "fox", "jumps", "over", 
          "the", "lazy", "dog"] 
       c.setrange((3,6), (3,6), stuff)                        
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
          elif c==curses.KEY_F6: 
             (y, x) = self.scr.getyx()                           
             self.scr.addstr(y, x, str(self.colheads))                     
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

