

#  pdspread.py  
#  A simple Python spreadsheet using curses.   
#  This code is released to the public domain. 

#  Note - The Control keys are as follows - 
#  'SOH', 'STX', 'ETX', 'EOT', 'ENQ', 'ACK', 'BEL', 'BS', 
#  'HT', 'LF', 'VT', 'FF', 'CR', 'SO', 'SI', 'DLE', 'DC1', 
#  'DC2', 'DC3', 'DC4', 'NAK', 'SYN', 'ETB', 'CAN', 'EM', 'SUB' 
#  
#   We use the following here -  
#  ^Q (Quit),  ^H (Backspace),  ^S(Save), ^A(save As),  
#  ^B (Left-arrow) ^F(Right-arrow), ^P(Up-arrow), ^N(Down-arrow)      

import sys, curses, curses.ascii, curses.textpad, traceback, string, os

     
class cell(object): 
  def __init__(self): 
    self.width = 7 
    self.height = 2    
    self.text = "       " 
   
  def set(self, text): 
    self.text = text 
    
  def display(self):     
    return self.text      
               
               
class sheet(cell): 
  def init(self): 
    self.col = self.row = 0 
    # Draw the column and row headings 
    x = range(1, 11)
    y = range(1, 11)
    
    for val in x: 
      for val in y: 
        self.display() 
            
  def address(self): 
    return (self.col, self.row) 
    
  def move(self, col, row): 
    self.col = col 
    self.row = row 
            
  def write(self, col, row, text): 
    self.move(col, row)     
    cell.set(self, text)                       
               
               
                  
myscreen = curses.initscr()
myscreen.border(0) 
myscreen.addstr(1, 25, "*** P.D. Spreadsheet ***") 

# Create a new window. This will be our "cell". We will try to 
# create a key-handler to move the cell around the screen. To do this
# it may be necessary (for now) to create new windows each time an 
# arrow-key is pressed.

x = 2 
y = 3 
myscreen.move(y, x) 
  

# curses.newwin([nlines, ncols], begin_y, begin_x)
# Return a new window, whose left-upper corner is at (begin_y, begin_x), 
# and whose height/width is nlines/ncols. 
# By default, the window will extend from the specified position to the
# lower right corner of the screen. 
# create an instance of a cell 
a = cell() 
b = curses.newwin(1, 7, 3, 2) 
c = b.box(curses.ACS_VLINE, curses.ACS_HLINE) 

# Here, we can use str(a.display()), str(b) or str(c) 
myscreen.addstr(y, x, str(a.display()), curses.A_REVERSE) 


# myscreen.refresh() 

# myscreen.addstr(y, x, str(a.display()), curses.A_REVERSE) 


#  Do the column and row labels and set up the sheet 
#  Note - ord("A") = 65, ord("Z") is 90 
#  chr(65) = 'A' , chr(90) = 'Z' 

# Move cursor to bottom-right of screen 
myscreen.addstr(21, 78, "", curses.A_STANDOUT)

# myeditor = curses.textpad.Textbox(myscreen) 
# myeditor.edit() 

   
myscreen.refresh()
myscreen.getch() 


curses.endwin()

