


#  pdspread.py 
#  A simple spreadsheet.  

# This code is released to the public domain.  
 
import sys, re, types, itertools, math, curses, curses.ascii, traceback, string, os 
   
# A cell class. This contains the data in a cell, and also formats it
# (numeric format, alignment and so on).     
class cell(object): 
    def __init__(self): 
       self.address = None 
       self.data = None 
       self.width = 7 
       self.align = None 
    
    # Set an attribute (e.g. the cell address).    
    def set(self, attr, val): 
      setattr(self, attr, val) 
            
    # Get an attribute (e.g. the cell address or data). 
    def get(self, attr): 
      return getattr(self, attr)       
    
    # Write data to the cell. This is a separate method because we 
    # may want to use a particular alignment for the data. 
    def write(self, stuff, align="right"):                
       self.data = str(stuff) 
       self.align = align 
                        
    # Align data.                         
    def align(self): 
       if self.data.isdigit() == "True": 
          self.data = self.data.rjust(self.width) 
       elif self.data.isdigit() == "False":    
          self.data = self.data.ljust(self.width)              
   
   
# A range class. This allows us to manage a range of cells. 
class range(cell): 
    def __init__(self): 
       self.rangelist = [] 
       self.datalist = [] 
       
    def set(self, cells): 
       self.rangelist = cells 
       
    def write(self, alist): 
       self.datalist = alist 
          
    def get(self): 
       return self.datalist  
       
                       
# A highlight class. This has left and top boundaries. These are the leftmost 
# column and the topmost row. We will make the defaults 2 for lbound and 
# 2 for tbound. Coords is a tuple of the coordinates of the cell. 
# This is in the form (row, col).    
class highlight(range): 
    def __init__(self):             
       self.scr = scr 
       (y, x) = self.scr.getyx() 
       self.y = 0 
       self.x = 0   
       self.newy = self.y 
       self.newx = self.x   
       self.address = "A1" 
       
       # Specify the leftmost column and topmost row.
       self.lbound = 7
       self.tbound = 2                                  
       # Set up the appearance of the cell
       self.width = 7
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
       self.scr.refresh()  
    
    # Enter text into a cell. This will then be handled by the 
    # cell methods. 
    def store(self, stuff): 
       pass 
       
                                 
                                                       
#  A spreadsheet class. 
class sheet(highlight):
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
       self.myhighlight = highlight()                                            
       # Write the row and column headings.                             
       self.colheads = list(chr(x) for x in range(65,75)) 
       self.plist = list( (y,x) for y in range(1, 2) for 
          x in range(7, 75, 7) )
                    
       self.range.write(self.plist, self.colheads)  
       self.scr.refresh() 	
       
       # Row headings 
       self.scr.move(2, 0)         
       self.rowheads = list(range(1,21))  
       self.plist = list( (y,x) for y in range(2, 22) for 
          x in range(0, 1) )
       self.range.write(self.plist, self.rowheads)   
       self.scr.refresh() 	
       
       
       # The position (2, 7) puts the cell perfectly in position 
       # at cell "A1".                          
       self.scr.move(2, 7)
       self.myhighlight = highlight(self.scr)                                      
       self.scr.refresh()  
       
       
       self.cell.move("R")
       (y, x) = self.scr.getyx()                            
       self.cell.write("123") 
       #self.align() 
       self.scr.refresh()  
       
       
       self.cell.move("D")
       (y, x) = self.scr.getyx()                            
       self.cell.write("abc") 
       #self.align() 
       self.scr.refresh()  
       
       
       self.cell.move("D")
       (y, x) = self.scr.getyx()                            
       self.cell.write("456") 
       #self.align() 
       self.scr.refresh()  
       
                
       self.cell.move("D")
       self.scr.addstr(y, x, str(self.cell.text) )                
       self.scr.refresh()  
       
              
       self.cell.move("D")
       self.scr.addstr(y, x, str(self.cell.text) )                       
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

