
# cell2.py 


import sys, re, types, itertools, math, curses, curses.ascii, traceback, string, os 
   

# Get the letter or numeric part of a cell address (so that we can 
# manipulate it). 
def getpart(cell, part): 
  letters = "" 
  numbers = "" 
        
  for x in cell: 
     if x.isalpha(): 
        letters += x 
     elif x.isdigit(): 
        numbers += x 
     else: 
        pass    
        
  numbers = int(numbers)         
     
  if part.upper() == "A": 
     return letters
  elif part.upper() == "N":
     return numbers 
   
      
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

# Convert a "column number" to the column letter(s) 
def num2str(n):
    #assert isinstance(n,int) and n > 0
    digits = "-ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    res = [] 
    while True:
        n, r = divmod(n, 26)
        if r == 0:    # Adjust the quotient and remainder
            n, r = n-1, 26
        res[0:0] = digits[r]
        if n == 0:            
            return str("".join(res))
    

# Convert "column letter(s)" to the column number   
def str2num(str): 
    num = 0 
    mylen = len(str) 
    # A list of the powers of 26 that we need for the calculations
    powerlist = range(mylen-1, -1, -1) 
    for a,b in zip(str.upper(), powerlist):
       num += (ord(a)-64) * (26**b)       
    return num    
    

# This function returns the cell in the given direction from the 
# supplied cell.  
def dir(cell, dir):   
   letters = getpart(cell, "A") 
   numbers = getpart(cell, "N")   
   # Convert the letter part of the address to a number 
   colnum = str2num(letters) 
   
   if dir.upper() == "L": 
      if colnum > 1: 
         colnum -= 1 
         result = str(num2str(colnum) + str(numbers)) 
      else: 
         result = None 
   elif dir.upper() == "R": 
      colnum += 1 
      result = str(num2str(colnum) + str(numbers)) 
   elif dir.upper() == "U": 
      if numbers > 1: 
         numbers -= 1 
         result = str(num2str(colnum) + str(numbers))             
      else: 
         result = None 
   elif dir.upper() == "D": 
      numbers += 1 
      result = str(num2str(colnum) + str(numbers))                   
   return result    
      
         
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
    width = 6
    '''if x == "A": width = 0
    else: width = 6 '''   
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
  
   def getitem(self, row, col):
       return self.matrix[row-1][col-1]
  
   def __repr__(self):
       outStr = ""
       for i in range(self.rows):
           outStr += 'Row %s = %s\n' % (i+1, self.matrix[i])
       return outStr
  
  
#  Create a matrix for our spreadsheet. This will hold the positions 
#  of each cell. 
b = matrix(21, 11) 
c = [] 

colnums = range(65, 75)
for x in colnums: 
  c.append(chr(x))    

# Set the column headings 
for a in range(2, 12):  
  b.setitem(1, a, c[a-2]) 

# Set the row headings 
for e in range(2, 22): 
  b.setitem(e, 1, e-1) 

# Now, store the cell positions in the matrix 
for r in range(2, 22): 
  for c in range(2, 12): 
     b.setitem(r, c, (r, (c*7)-7))       


# A cell class 
# Note - Look at removing the code for the positions of the neighbouring 
# cells. These could be found by a dict lookup instead. Similarly, the 
# values in those cells could be looked up as well. 
class cell(object): 
   def init(self, scr):
      self.scr = scr   
      self.width = 6 
      (y, x) = self.scr.getyx() 
      # The position of the cell
      self.pos = (y, x)                                   
      self.scr.chgat(y, x, self.width, curses.A_STANDOUT)   
      self.scr.refresh()
      # The name of the cell (e.g. "A1") 
      self.name = str(num2str(x-self.width) + str(y-1))                    
      # Store the cell POSITIONS bordering this cell              
      if getpart(self.name, "A") != "A": 
          self.leftpos = (y, x-self.width)          
      else: 
          self.leftpos = None    
      if getpart(self.name, "N") != 1: 
          self.abovepos = (y-1, x)          
      else: 
          self.abovepos = None       
      self.belowpos = (y+1, x) 
      self.rightpos = (y, x+self.width)   
              
      # Store data 
      self.data = {}       
      self.scr.refresh() 
                    
   # Set a given attribute    
   def set(self, attr, val): 
      if hasattr(self, attr): 
          setattr(self, attr, val)  
      else: 
          pass  
       
   # Move to another cell 
   def cellmove(self, dir): 
      # First, go to the "home" position of the cell 
      self.scr.move(self.pos[0], self.pos[1]) 
      (y, x) = self.scr.getyx() 
      self.scr.chgat(y, x, self.width, curses.A_NORMAL)                      
      self.scr.refresh()                                
      if dir.upper() == "L": 
          if self.leftpos != None:              
             self.scr.move(self.leftpos[0], self.leftpos[1]) 
             (y, x) = self.scr.getyx() 
             self.scr.chgat(y, x, self.width, curses.A_STANDOUT)    
             a = cell() 
             a.init(self.scr)
             self.scr.refresh()                                
          else: 
             pass              
      elif dir.upper() == "R":           
          self.scr.move(self.rightpos[0], self.rightpos[1]) 
          (y, x) = self.scr.getyx() 
          self.scr.chgat(y, x, self.width, curses.A_STANDOUT)   
          a = cell() 
          a.init(self.scr)
          self.scr.refresh() 
      elif dir.upper() == "U": 
          if self.abovepos != None:              
             self.scr.move(self.abovepos[0], self.abovepos[1]) 
             (y, x) = self.scr.getyx() 
             self.scr.chgat(y, x, self.width, curses.A_STANDOUT)   
             a = cell() 
             a.init(self.scr)
             self.scr.refresh() 
          else: 
             pass                 
      elif dir.upper() == "D":           
          self.scr.move(self.belowpos[0], self.belowpos[1]) 
          (y, x) = self.scr.getyx() 
          self.scr.chgat(y, x, self.width, curses.A_STANDOUT)   
          a = cell() 
          a.init(self.scr)
          self.scr.refresh() 
                                                                                                                    
   def display(self, attr): 
      (y, x) = self.scr.getyx()           
      strattr = str(getattr(self, attr)) 
      self.scr.addstr(y, x, str(strattr) ) 
      
      
class sheet(cell):
    def __init__(self, scr): 
       self.scr = scr  
       self.stuff = "" 
       (y, x) = self.scr.getyx()           
       self.width = 6 
       # A variable to save the line-number of text. 
       self.win_y = self.win_x = 0  
       # The screen size (number of rows and columns). 
       (self.max_y, self.max_x) = self.scr.getmaxyx()
          
       # calculate the number of columns 
       # We subtract self.width to cater for the width of the row headings
       self.numcols = int((self.max_x-self.width)/self.width)                        
       curses.noecho() 
       self.scr.move(2, 7) 
       # Create a cell 
       a = cell() 
       a.init(self.scr)        
       # Look at adding headings code here to create the column and 
       # row headings. 
              
       self.scr.keypad(1)            
       self.scr.scrollok(1)
       self.scr.idlok(1)  
       self.scr.setscrreg(0, self.max_y-1)                                
       self.scr.refresh()	     
    
    # to "normal" background, and highlights the new cell.             
    def move(self, mydir):    
       a = cell() 
       a.init(self.scr)        
       a.cellmove(mydir) 
    
    def action(self):  
       while (1): 
          (y, x) = self.scr.getyx()            
          curses.echo()                           
          c=self.scr.getch()		# Get a keystroke                                                                                  
          if c in (curses.KEY_ENTER, 10):                
             curses.noecho()        
             (y, x) = self.scr.getyx()                   
             self.move("D")                 
             self.scr.refresh()                                                                                                        
          elif c==curses.KEY_UP:  
             curses.noecho()                
             if y > 2:   
                self.move("U")                                
             elif y == 2 and self.win_y > 0:   
                self.scr.scroll(-1)                                   
             else: 
                pass                                                                                     
             self.scr.refresh()
          elif c==curses.KEY_DOWN:
             curses.noecho()   
             (y, x) = self.scr.getyx()           
             if y < self.max_y-1:                    
                self.move("D")  
                self.scr.refresh()                                                                 
             else:                                          
                self.scr.scroll(1)                                                 
             self.scr.refresh()   
          elif c==curses.KEY_LEFT: 
             curses.noecho()  
             if x >= 7 + self.width:                 
                self.move("L")  
             else: 
                pass 
             self.scr.refresh()
          elif c==curses.KEY_RIGHT: 
             curses.noecho() 
             if x < self.max_x-self.width-1:                 
                self.move("R")                  
             else: 
                pass                 
             self.scr.refresh() 
          elif c==curses.KEY_HOME: 
             curses.noecho() 
             (y, x) = self.scr.getyx() 
             self.scr.chgat(y, x, self.width, curses.A_NORMAL)                      
             self.scr.refresh()                                
             self.scr.move(y, 7) 
             a = cell()
             a.init(self.scr) 
             self.scr.refresh() 
          elif c==curses.KEY_END: 
             curses.noecho() 
             (y, x) = self.scr.getyx() 
             self.scr.chgat(y, x, self.width, curses.A_NORMAL)                      
             self.scr.refresh()                                
             self.scr.move(y, self.max_x - self.width-1) 
             a = cell()
             a.init(self.scr) 
             self.scr.refresh()  
          elif c==curses.KEY_F5: 
             (y, x) = self.scr.getyx() 
             a = cell()
             a.init(self.scr) 
             name = a.name                           
             self.scr.addstr(y, x, str(name))                                  
             self.scr.refresh()  
          elif c==curses.KEY_F6: 
             (y, x) = self.scr.getyx() 
             self.test = yx2str(y, x, self.width) 
             self.scr.addstr(y, x, str(self.rowheadnames))                     
             self.scr.refresh()  
          elif c==curses.KEY_F7: 
             self.test() 
          elif c==curses.KEY_F8: 
             self.test2() 
          elif c==curses.KEY_F9: 
             self.test4("A1")    
             
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



   
       
       
       
