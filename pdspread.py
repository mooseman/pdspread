


#  pdspread.py 
#  A simple spreadsheet.  

# This code is released to the public domain.  
 
import sys, re, types, itertools, math, curses, curses.ascii, traceback, string, os 
   

# A data object. This has the properties of value, alignment and so on. 
class data(object):   
  def value(self, val): 
     self.value = val     
     
  def width(self, w): 
     self.width = w    
     
  def align(self): 
     if str(self.value).isdigit() == "True": 
        self.value.rjust(self.width) 
     elif str(self.value).isdigit() == "False":    
        self.value.ljust(self.width) 
               
                     
# A cell class. This has left and top boundaries. These are the leftmost 
# column and the topmost row. We will make the defaults 2 for lbound and 
# 2 for tbound. Coords is a tuple of the coordinates of the cell. 
# This is in the form (row, col).    
class cell(data): 
    def __init__(self, scr): 
       self.scr = scr     
       (y, x) = self.scr.getyx() 
       self.y = y 
       self.x = x   
       self.newy = y 
       self.newx = x   
       self.width = 7 
       self.value = ""
       
       # Specify the leftmost column and topmost row.
       self.lbound = 7
       self.tbound = 2                                  
              
       # Now, set up the cell "highlight" and refresh the screen. 
       self.scr.chgat(self.y, self.x, self.width, curses.A_STANDOUT)    
       #self.scr.addstr(self.y, self.x, str(self.y) + " " + str(self.x)  ) 
       self.scr.move(self.y, self.x)
       self.scr.refresh()                   
       
    # Move the cell in a given direction  
    # Note - to get the desired handling of the Enter key, the crucial 
    # setting is self.scr.leaveok(0). 
    # Notice here that we have a "direction" of "*". This is used when 
    # the Enter key is pressed. It moves the cursor to the beginning 
    # of the cell (highlight).                       
    def move(self, dir):               
       #(y, x) = self.scr.getyx() 
       self.dir=dir.upper()
       if self.dir == "L" and self.x-self.width >= self.lbound:           
          self.newx = self.x - self.width 
       else: 
          pass            
       if self.dir == "R":    
          self.newx = self.x + self.width 
       elif self.dir == "U" and self.y > self.tbound:    
          self.newy = self.y - 1 
       else: 
          pass    
       if self.dir == "D":    
          self.newy = self.y + 1 
       elif self.dir == "*": 
          self.newx = self.x 
          self.newy = self.y                     
       # Remove the highlight from the current cell. 
       self.scr.move(self.y, self.x)         
       self.scr.chgat(self.y, self.x, self.width, curses.A_NORMAL)         
       self.scr.refresh() 
       # Now move the highlight to the new coordinates.               
       self.scr.move(self.newy, self.newx)        
       (y, x) = self.scr.getyx() 
       self.y = y 
       self.x = x
       self.scr.chgat(self.y, self.x, self.width, curses.A_STANDOUT)  
       #self.text = ""  
       #self.text.rjust(self.width)          
       #self.text = self.text.rjust(self.width)          
       self.scr.refresh()  
                         
    # Write something in a cell and apply an attribute (curses.A_NORMAL, 
    # curses.A_STANDOUT etc) to it. You can also apply alignment 
    # (usually centering) here.     
    # We will do a "range" version of this function to write a list of 
    # text into a range of cells - just what is needed for headings and 
    # so on.                          
    # This just saves text to the cell's text string. 
    def write(self, text):         
       for x in text:   
          str(self.value) + str(x)                                                  
       self.scr.move(self.y, self.x)                   
       self.scr.addstr(self.y, self.x, str(self.value) )       
       self.scr.refresh() 
       self.value = ""       
                  
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
 
                                                      
#  A spreadsheet class. 
class sheet(cell):
    def __init__(self, scr): 
       self.scr = scr   
       (y, x) = self.scr.getyx()                            
       curses.noecho() 
       self.scr.keypad(1)            
       self.scr.scrollok(1)
       self.scr.idlok(1) 
       # Just added leaveok. 
       self.scr.leaveok(0)                      
       self.scr.setscrreg(0, 22) 
       self.stuff = ""          
       
       # Set the default column width. 
       self.colwidth = 7          
       # Move to the origin.        
       self.scr.move(1, 7)                       
       # Create a cell
       self.cell = cell(self.scr)                                            
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
       # The position (2, 7) puts the cell perfectly in position 
       # at cell "A1".                          
       self.scr.move(2, 7)
       self.cell = cell(self.scr)                                      
       self.scr.refresh()  
       
       self.cell.move("R")
       (y, x) = self.scr.getyx()                            
       self.cell.write("123") 
       self.align() 
       self.scr.refresh()  
       
       self.cell.move("D")
       (y, x) = self.scr.getyx()                            
       self.cell.write("abc") 
       self.align() 
       self.scr.refresh()  
       
       self.cell.move("D")
       (y, x) = self.scr.getyx()                            
       self.cell.write("456") 
       self.align() 
       self.scr.refresh()  
                
       self.cell.move("D")
       self.scr.addstr(y, x, str(self.value) )                
       self.scr.refresh()  
              
       self.cell.move("D")
       self.scr.addstr(y, x, str(self.value) )                       
       self.scr.refresh()  
                                          
       self.cell.move("D")
       self.scr.refresh()  

    # See if we can capture user input and then manipulate it. 
    def test(self):       
       self.cell.write("foo") 
       self.scr.refresh()   
                                  
                                          
    # We handle keystrokes here.                                                                                                                                                                                                                                                                                                                      
    def action(self):  
       while (1): 
          (y, x) = self.scr.getyx()            
          curses.echo()          
          # Get a keystroke. Note - to get alignment working, maybe 
          # we need to use getstr here (instead of getch) ?          
          c=self.scr.getch()		
          if c in (curses.KEY_ENTER, 10):                
             curses.noecho()  
             #self.testtext()  
             self.cell.move("D")   
             # To move the cursor to the start of the cell, comment out 
             # the above line, and uncomment the line below.         
             #self.cell.move("*")
             self.scr.refresh()                
          elif c==curses.KEY_UP:  
             curses.noecho()  
             #self.testtext()                
             self.cell.move("U")
             self.scr.refresh()
          elif c==curses.KEY_DOWN:
             curses.noecho()  
             #self.testtext()   
             self.cell.move("D")                  
             self.scr.refresh()   
          elif c==curses.KEY_LEFT: 
             curses.noecho()  
             #self.testtext()  
             self.cell.move("L")
             self.scr.refresh()
          elif c==curses.KEY_RIGHT: 
             curses.noecho() 
             #self.testtext()  
             self.cell.move("R")
             self.scr.refresh()                                                                 
          elif c==curses.KEY_F2: 
             pass                                                                     
          # Ctrl-G quits the app                  
          elif c==curses.ascii.BEL: 
             break   
          ######################################################   
          # This is where user-entered text is controlled from. 
          ######################################################          
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
     curses.noecho() ; curses.cbreak()
     stdscr.keypad(1)
     main(stdscr)  # Enter the main loop
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

