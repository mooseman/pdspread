

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

     
             
myscreen = curses.initscr()
myscreen.border(0) 
myscreen.addstr(1, 25, "*** P.D. Spreadsheet ***") 

#  Set up the sheet 
a = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"] 

b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 
      17, 18, 19, 20] 

y = 2 
x = 7 

myscreen.move(y, x) 

for chr in a: 
   myscreen.addstr(y, x, str(chr) ) 
   x += 7 
   myscreen.move(y, x) 

# Finished the column headings. Move to the left of the screen to 
# do the row labels.   
myscreen.refresh()   


myscreen.move(15, 2) 
myscreen.refresh()            
         
y = 3 
x = 2          
for chr in b: 
   myscreen.addstr(y, x, str(chr) ) 
   y += 1 
   myscreen.move(y, x) 


#  Do the column and row labels and set up the sheet 
#  Note - ord("A") = 65, ord("Z") is 90 
#  chr(65) = 'A' , chr(90) = 'Z' 

myscreen.addstr(21, 78, "", curses.A_STANDOUT)

myeditor = curses.textpad.Textbox(myscreen) 
myeditor.edit() 

   
myscreen.refresh()
myscreen.getch() 


curses.endwin()

