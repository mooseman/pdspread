


#  pdspread.py 
#  The spreadsheet is in the process of a major rewrite. 
#  Emphasis is now on making the sheet class store the data, 
#  store the currently-visible range of the sheet, show the 
#  data in that range and handle keystrokes.  
#  The cell class is now not derived from sheet - it simply 
#  stores data there.   

 
import sys, re, types, itertools, math, curses, curses.ascii, traceback, string, os 
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
   print res              
      

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
   print res    


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


# Sheet class. This stores the data for all cells.    
# It also has a visible range. 
# It is the sheet which displays the data.  
class sheet(object): 
   def __init__(self, scr): 
      self.scr = scr 
      (y, x) = self.scr.getmaxyx() 
      # Variables to store the maxrows and maxcols on screen.  
      # These will change if the window changes size. 
      self.maxrows = str(y) 
      self.maxcols = str(x)                   
      self.mydict = {} 
      # Make the upper limit one more than the actual boundary. 
      self.y_range = [1, 21]
      self.x_range = [1, 11]
            
   # Update the visible range 
   def update(self, direction):       
      if direction == "U": 
         self.y_range[0] -= 1 
         self.y_range[1] -= 1 
      elif direction == "D": 
         self.y_range[0] += 1    
         self.y_range[1] += 1 
      elif direction == "L": 
         self.x_range[0] -= 1    
         self.x_range[1] -= 1 
      elif direction == "R": 
         self.x_range[0] += 1    
         self.x_range[1] += 1    
   
   # Display the data if it is in the visible range.  
   def show(self):  
      for key in self.mydict: 
            if self.mydict[key][0] in self.y_range and self.mydict[key][1] in self.x_range: 
               self.scr.addstr(key[0], key[1], str(self.mydict[key][2]) )   
               self.scr.refresh()                       
            else: 
               pass                    
         
   # Handle keystrokes here.  
   def action(self):  
      while (1):   
          # Display data on visible part of sheet.           
          self.show() 
          (y, x) = self.scr.getyx()             
          c=self.scr.getch()		
          if c in (curses.KEY_ENTER, 10):                
             curses.noecho()                 
             #self.cell.move("D")   
             self.scr.refresh()   
          elif c==curses.KEY_UP:  
             curses.noecho()               
             #self.cell.move("U")             
             self.scr.refresh()
          elif c==curses.KEY_DOWN:
             curses.noecho()               
             #self.cell.move("D")                               
             self.scr.refresh()   
          elif c==curses.KEY_LEFT: 
             curses.noecho()               
             #self.cell.move("L")             
             self.scr.refresh()
          elif c==curses.KEY_RIGHT: 
             curses.noecho()              
             #self.cell.move("R")
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
   
   
   
# Cell class.  
# Has an address.  Has methods to set and get data. 
# Data is stored in the sheet class. 
class cell(object): 
   # Address ( e.g. "E8", "AB123" ) 
   def __init__(self, scr, address):    
      self.data = None     
   # Split the address into col and row. 
      self.splitaddress = splitaddress(self.address)
      self.numaddress = [lettertonum(self.splitaddress[0]), self.splitaddress[1]] 
      self.y = self.numaddress[1]
      self.x = self.numaddress[0] 
   # The SCREEN position of the cell. This is used to display it.  
      (y, x) = self.scr.getyx()               
      self.scr_y = y 
      self.scr_x = x 
      
   #  Store data in the sheet dictionary 
   def setdata(self, data):       
      sheet.mydict.update({(self.y, self.x) : [self.scr_y, self.scr_x, self.data]})  
      
   # Get the data for a cell.  
   def getdata(self):  
      return sheet.mydict[self.y, self.x][2]  
     
   def setpos(self, ypos, xpos): 
      pass    
      
   # Set the position of the cell on the screen. 
   # May want to check if the cell is in the y_range and x_range 
   # of the sheet first.      
   def updatepos(self, direction):    
      if self.scr_y in screen.yrange and self.scr_x in screen.x_range:  
         if direction == "U": 
            self.scr_y += 1 
         elif direction == "D": 
            self.scr_y -= 1 
         elif direction == "L": 
            self.scr_x += cellwidth 
         elif direction == "R": 
            self.scr_x -= cellwidth                  
      
      
# A headings class that will eventually be able to update itself.      
class headings(object):     
   def __init__(self, scr): 
      self.colheads = None 
      self.rowheads = None 
      
   def update(self, direction): 
      pass           



# Highlight. When this moves, the cell address could update. 
class highlight(): 
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
     traceback.print_exc()  # Print the exception


