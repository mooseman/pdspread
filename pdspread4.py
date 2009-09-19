

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

#  NOTE - TO FIND THE UPPER-CASE LETTER FOR ALL NUMBERS BIGGER THAN 
#  90, USE THIS FORMULA - 
#  LETTER = chr(NUM % 90 % 26) + 65.  
#  For example - chr(90) = 'Z' 
#  91 % 90 % 26 = 1    95 % 90 % 26 = 5 
#  116 % 90 % 26 = 0   117 % 90 % 26 = 1  and so on.    

import sys, curses, curses.ascii, curses.textpad, traceback, string, os

# Set some important properties of the display 
# Allow 8-bit characters to be input 
curses.meta(1) 
# Make cursor invisible 
curses.leaveok(1) 


     
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
    # Set the initial address of the highlighted cell 
    self.col = self.row = 0 
    # Set the maximum size of a sheet 
    self.maxcols = 200 
    self.maxrows = 1000 
                
  def col_headings(self): 
    self.col_headings = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"] 
    return self.col_headings 
    
  def row_headings(self): 
    self.row_headings = range(1, 21) 
    return self.row_headings
            
  def address(self): 
    return (self.col, self.row) 
    
  def move(self, col, row): 
    self.col = col 
    self.row = row 
    
  # Highlight the currently-active cell 
  # May need to take cell address as an argument 
  def highlight(self): 
    pass     
    
  # Manage the keys so we can input data and move from cell to cell.     
  def key_mgr(self, ch):     
    self.ch = ch 
    # Move the cell highlight according to which key is pressed 
    if self.ch == curses.KEY_LEFT: 
       self.move(col-1, row) 
    elif self.ch == curses.KEY_RIGHT: 
       self.move(col+1, row)  
    elif self.ch == curses.KEY_UP: 
       self.move(col, row-1)
    elif self.ch == curses.KEY_DOWN: 
       self.move(col, row+1) 
    else: 
       pass               
                   
                       
  def write(self, col, row, text): 
    self.move(col, row)     
    cell.set(self, text)                       
           
  def create(self):     
    # Draw the column and row headings, and create the grid  
    
    
    
    for val in x: 
      for val in y: 
        self.display()            
           
               
               
                  
myscreen = curses.initscr()
myscreen.border(0) 
myscreen.addstr(1, 25, "*** P.D. Spreadsheet ***") 

# Add stuff here to set up sheet 



# Put cursor at bottom-right 
myscreen.addstr(21, 78, "", curses.A_STANDOUT)

myeditor = curses.textpad.Textbox(myscreen) 
myeditor.edit() 

   
myscreen.refresh()
myscreen.getch() 


curses.endwin()

