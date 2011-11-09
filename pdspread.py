


#  pdspread.py 
#  The spreadsheet is in the process of a major rewrite. 
#  Emphasis is now on making the sheet class store the data, 
#  store the currently-visible range of the sheet, show the 
#  data in that range and handle keystrokes.  
#  The cell class is now not derived from sheet - it simply 
#  stores data there.   

 
import sys, types, math, curses, curses.ascii, string, os 
# Set the topmost and the leftmost boundaries for a cell.  
lbound = 7
tbound = 3                                     
cellwidth = 7 


# Do a function to convert numeric references e.g. (10, 5) to 
# cell references e.g. J5. Also a function to do the reverse.  
# See here - http://en.wikipedia.org/wiki/Bijective_numeration 

# Each digit position represents a power of twenty-six, so for 
# example AB is "one 26**1, plus two units (26**0)" 
# since "A" is worth one, "B" is worth two, "C" is worth three,...
# Z is worth 26.   
# chr(65) is 'A'.  chr(90) is 'Z'.   


# Use divmod here.   
def numtoletter(num):  
   if num <= 0: 
      res = "Too small" 
   elif 1 <= num <= 26: 
      res = str( ' ' + chr(num + 64) ) 
   elif 26 < num <= 702: 
      a = divmod(num, 26) 
      if a[1] == 0: 
         res = str( chr( (a[0]-1) + 64) + 'Z' )       
      else: 
         res = str( chr( (a[0]) + 64) + chr( a[1] + 64) ) 
   else: 
      res = "Too large"  
   return res              
      

# Convert a column letter (e.g. "BD") to the corresponding 
# column number.   
def lettertonum(letter): 
   if len(letter) == 2: 
      num1 = ord(letter[0]) - 64 
      num2 = ord(letter[1]) - 64       
      res = (num1 * 26**1) + (num2 * 26**0) 
   elif len(letter) == 1: 
      num1 = ord(letter) - 64
      res = (num1 * 26**0) 
   return res    


# Split the address of a cell into column and row 
def splitaddress(cell): 
   col = "" 
   row = 0
   index = 0      
   for x in cell: 
      if x.isalpha():  
         col = col + x
         index += 1
      else: 
         row = int(cell[index:]) 
   splitaddress = [col, row]          
   return splitaddress


# A test class to manipulate cell references 
# Look up the cell address (e.g. "C7"), get the screen 
# position, and do something with it. 
# H is a highlight flag - "Y" or "N" 
class cell(object): 
   def __init__(self, scr, y, x, data):
      self.scr = scr 
      self.y = y
      self.x = x       
      self.data = data 
      self.width = 7 
      self.scr.chgat(self.y, self.x, self.width, curses.A_STANDOUT) 
      self.scr.refresh()           
                                    
   # Change data.     
   def update(self, data): 
      self.data = data 
      self.scr.addstr(self.y, self.x, str(self.data) )       
      self.scr.refresh()            
      

# A range class, derived from cell.  
class crange(cell): 
   def __init__(self, scr, y_range, x_range, datalist): 
      self.scr = scr 
      self.poslist = list( (y,x) for y in y_range for 
         x in x_range)        
      self.datalist = datalist 
      for x,y in zip(self.datalist, self.poslist):
             self.scr.addstr(y[0], y[1], str(x) ) 
      self.scr.refresh() 
      

#  A highlight class, derived from cell.  
# This class has a "move" method. 
class hlight(cell): 
   def show(self): 
      self.scr.chgat(self.y, self.x, self.width, curses.A_STANDOUT) 
      self.scr.refresh()           
               
   # Move the highlight   
   def move(self, direction):       
      # Remove the highlight from the current cell. 
      self.scr.chgat(self.y, self.x, self.width, curses.A_NORMAL) 
      if direction == "U": 
         self.y -= 1 
      elif direction == "D":     
         self.y += 1 
      elif direction == "L": 
         self.x -= self.width 
      elif direction == "R": 
         self.x += self.width 
      # Show the highlight at the destination
      self.scr.chgat(self.y, self.x, self.width, curses.A_STANDOUT)    
      self.scr.refresh()    
   
   
# Sheet class. This stores the data for all cells.    
# It also has a visible range. 
# It is the sheet which displays the data.  
class sheet(object): 
   def __init__(self, scr): 
      self.scr = scr   
      (y, x) = self.scr.getyx()
      curses.noecho()
      self.scr.keypad(1)
      self.scr.scrollok(1)
      self.scr.idlok(1)      
      self.scr.leaveok(0)
      self.scr.setscrreg(0, 22) 
     
      self.datadict = {}     
      # Row and column headings 
      self.rowheads = crange(self.scr, list(range(2,30)), 
          list(range(3,4)), list(range(1, 29)) ) 
          
      self.colheads = crange(self.scr, list( range(1, 2) ),   
          list(range(10, 83, 7) ),  list( chr(x) for 
          x in range(65, 76) ) )  
                    
      # The cell highlight        
      self.h = hlight(self.scr, 2, 7, '') 
      self.h.show()       
      self.scr.refresh()                       
                           
   # Handle keystrokes here.  
   def action(self):  
      while (1):   
          # Display data on visible part of sheet.           
          self.h.show() 
          (y, x) = self.scr.getyx()             
          c=self.scr.getch()		
          if c in (curses.KEY_ENTER, 10):                
             curses.noecho()                 
             #h.move("D")   
             self.scr.refresh()   
          elif c==curses.KEY_UP:  
             curses.noecho()               
             self.h.move("U")             
             self.scr.refresh()
          elif c==curses.KEY_DOWN:
             curses.noecho()               
             self.h.move("D")                               
             self.scr.refresh()   
          elif c==curses.KEY_LEFT: 
             curses.noecho()               
             self.h.move("L")             
             self.scr.refresh()
          elif c==curses.KEY_RIGHT: 
             curses.noecho()              
             self.h.move("R")
             self.scr.refresh()     
          # Page Up. 
          elif c==curses.KEY_PPAGE: 
             #self.changerowheads(-20) 
             self.scr.refresh()                   
          # Page Down. 
          elif c==curses.KEY_NPAGE: 
             #self.changerowheads(20)
             self.scr.refresh()      
          elif c==curses.KEY_RESIZE: 
             (y, x) = self.scr.getmaxyx() 
             self.maxrows = str(y) 
             self.maxcols = str(x)             
             self.scr.addstr(5, 10, ( self.maxrows + ',' + self.maxcols ) )   
             self.scr.refresh()                                                   
          elif c==curses.KEY_F2: 
             #self.cell.create_win() 
             self.scr.refresh()                                                                  
                                                                           
          # Ctrl-G quits the app                  
          elif c==curses.ascii.BEL: 
             break   
          ######################################################   
          # This is where user-entered text is controlled from. 
          ######################################################          
          elif 0<c<256: 
             c=chr(c) 
             #self.cell.value += c              
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
     # curses.start_color()           
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
     


