

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
    def __init__(self, scr): 
       self.scr = scr     
       (y, x) = self.scr.getyx() 
       self.y = y 
       self.x = x         
       # Methods to store the cells bordering this cell. 
       self.left = self.right = self.above = self.below = None 
       # Store data 
       self.data = {} 
       # Attributes for moving the cell 
       self.newy = self.y 
       self.newx = self.x 
       # A cell's name (e.g. E5)  
       self.addr = None 
       # A cell's position (e.g. 7, 28) 
       self.pos = None 
       # Set up the appearance of the cell
       self.width = 7
       # Now, set up the cell "highlight" and refresh the screen. 
       self.scr.chgat(self.y, self.x, self.width, curses.A_STANDOUT)    
       #self.scr.addstr(self.y, self.x, str(self.y) + " " + str(self.x)  ) 
       self.scr.move(self.y, self.x)
       self.scr.refresh()                   
       
    # Set a given attribute    
    def set(self, attr, val): 
       setattr(self, attr, val)                    
    # Move the cell in a given direction  
    # Note - to get the desired handling of the Enter key, the crucial 
    # setting is self.scr.leaveok(0). 
    # Notice here that we have a "direction" of "*". This is used when 
    # the Enter key is pressed. It moves the cursor to the beginning 
    # of the cell (highlight).                       
    def move(self, dir): 
       self.dir = dir.upper() 
       #(y, x) = self.scr.getyx() 
       if self.dir == "L": 
          self.newx = self.x - self.width 
       elif self.dir == "R":    
          self.newx = self.x + self.width 
       elif self.dir == "U":    
          self.newy = self.y - 1 
       elif self.dir == "D":    
          self.newy = self.y + 1 
       elif self.dir == "*": 
          self.newx = self.x 
          self.newy = self.y                     
       # Remove the highlight from the current cell. 
       self.scr.move(self.y, self.x)         
       self.scr.chgat(self.y, self.x, self.width, curses.A_NORMAL)                      
       self.scr.refresh() 
       # Now move the highlight to the new coordinates. 
       #self.scr.move(5, 10)
       #self.scr.addstr(5, 10, str(self.newy) + " " + str(self.newx)  )  
       
       self.scr.move(self.newy, self.newx) 
       #a = cell(self.scr, (self.newy, self.newx))
       (y, x) = self.scr.getyx() 
       self.y = y 
       self.x = x
       self.scr.chgat(self.y, self.x, self.width, curses.A_STANDOUT)    
       self.scr.refresh()  
                         
    # Write something in a cell and apply an attribute (curses.A_NORMAL, 
    # curses.A_STANDOUT etc) to it. You can also apply alignment 
    # (usually centering) here.     
    # We will do a "range" version of this function to write a list of 
    # text into a range of cells - just what is needed for headings and 
    # so on.                          
    def write(self, text, attr=None, align=None):    
       # Apply alignment (if any) 
       if align == None: 
          self.text = text 
       elif align == "center": 
          self.text = text.center(self.width)  
       else: 
          pass                   
       # Get the position of the cursor. 
       (y, x) = self.scr.getyx() 
       # Write the text, applying the attribute (if used) 
       if attr == None: 
          self.scr.addstr(y, x, str(self.text) ) 
       else:           
          self.scr.addstr(y, x, str(self.text), attr)  
       # Refresh the screen 
       self.scr.refresh()                                      
                  
    # Write a list of data into a range of cell positions. 
    def write_range(self, datalist, poslist, attr=None, align=None): 
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
       # Just added leaveok. 
       self.scr.leaveok(0)                      
       self.scr.setscrreg(0, 22)    
       # Set the default column width. 
       self.colwidth = 7   
       # Store any entered text. 
       self.stuff = ""             
       # Move to the origin. 
       #self.scr.move(0, 0)                
       self.scr.move(5, 10)                
       # Create a cell
       self.cell = cell(self.scr)         
       # Write something 
       self.cell.write("Here is some text")   
       self.scr.refresh() 
       	                         
       self.scr.move(7, 15)                
       self.cell.write("Foo", curses.A_STANDOUT, "center") 
       self.scr.refresh() 
          
       self.scr.move(9, 15)  
       #self.mytext = curses.has_colors()  
       #self.mytext = curses.can_change_color()                     
       #self.cell.write(self.mytext)       
       self.cell.write("Testing", curses.A_NORMAL, "center")   
       self.scr.refresh() 
       
       self.scr.move(11, 15)                       
       self.cell.write("5", curses.A_UNDERLINE, "center")                                     
       #self.cell.move("*")
       self.scr.refresh() 	                         
                     
       # Write some data to a range
       self.scr.move(0, 0)         
       # Write the row and column headings.                             
       self.colheads = list(chr(x) for x in range(65,75)) 
       self.plist = list( (y,x) for y in range(1, 2) for 
          x in range(7, 75, 7) )
       self.cell.write_range(self.colheads, self.plist, 
            curses.A_STANDOUT, "center")  
       self.scr.refresh() 	
       # Row headings 
       self.scr.move(2, 0)         
       self.rowheads = list(range(1,21))  
       self.plist = list( (y,x) for y in range(2, 22) for 
          x in range(0, 1) )
       self.cell.write_range(self.rowheads, self.plist, 
            curses.A_STANDOUT, "center")  
       self.scr.refresh() 	
                                                                       
       # Create a matrix for the column and row headings. 
       a = matrix(21,11)               
       self.colheads = list(chr(x) for x in range(65,76)) 
       self.rowheads = list(range(1,21))  
       a.setrange((1,2), (2,12), self.colheads)      
       a.setrange((2,22), (1,2), self.rowheads)   
       # Apply attributes to the headings 
       # First, center the text 
       
       
       
       
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
                                                               
       # Display the matrix. Note - at present, this only displays the
       # matrix as a text string. We need to display the "live" matrix 
       # so that we can interact with it.    
       #self.scr.addstr(0, 0, str(a) )                      
       #self.scr.addstr(0, 0, str(d) )                      
       #self.cell.move((12, 40))       
       self.scr.refresh()	    
          
                                                                                                                                                                                                                                                  
    def action(self):  
       while (1): 
          (y, x) = self.scr.getyx()            
          curses.echo()                 
          c=self.scr.getch()		# Get a keystroke                                                                                  
          if c in (curses.KEY_ENTER, 10):                
             curses.noecho()    
             self.cell.move("D")   
             # To move the cursor to the start of the cell, comment out 
             # the above line, and uncomment the line below.         
             #self.cell.move("*")
             self.scr.refresh()                
          elif c==curses.KEY_UP:  
             curses.noecho()                
             self.cell.move("U")
             self.scr.refresh()
          elif c==curses.KEY_DOWN:
             curses.noecho()   
             self.cell.move("D")                  
             self.scr.refresh()   
          elif c==curses.KEY_LEFT: 
             curses.noecho()  
             self.cell.move("L")
             self.scr.refresh()
          elif c==curses.KEY_RIGHT: 
             curses.noecho() 
             self.cell.move("R")
             self.scr.refresh()                                                                 
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
     #curses.use_default_colors()
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

