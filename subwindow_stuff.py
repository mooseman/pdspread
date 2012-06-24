

#  pdspread.py 
#  The beginnings of a Python spreadsheet. 
#  This code is released to the public domain. 
#  "Share and enjoy...."  ;)  
 
import sys, itertools, types, math, curses, curses.ascii, string, os 
# Set the topmost and the leftmost boundaries for a cell.  
lbound = 7
tbound = 3                                     



# A class for the headings window.
class mywin(object): 
   def __init__(self, scr):
      self.scr = scr       
      # Create a long subwindow to enter commands in. 
      # Needs to be 3 rows high to have a border. 
      self.cmdwin = self.scr.subwin(3, 90, 2, 5) 
      self.cmdwin.box()
      
      # Create a "main" subwindow for the spreadsheet.       
      self.mainwin = self.scr.subwin(26, 90, 6, 5) 
      self.mainwin.box() 
      self.mainwin.addstr(5, 15, "A string....") 
      # NOTE! - in order to see the cursor move in the subwindow, 
      # we MUST first refresh the **parent** window, and **then** 
      # the subwindow. 
      self.mainwin.move(7, 17) 
      self.scr.refresh()   
      # OK - now we will see that the cursor has moved in mainwin.      
      self.mainwin.refresh()       
      
      # Draw some text in the parent window 
      self.scr.addstr(1, 20, "Menus could be put up here...") 
      #V Move cursor in parent window 
      self.scr.move(2, 45) 
      self.scr.refresh() 
      
      # Move the cursor into the main window 
      #self.mainwin.move(3, 10) 
      self.mainwin.addstr(3, 10, "X <--- I moved here...") 
      #self.mainwin.move(10, 25) 
      self.mainwin.addstr(10, 25, "X <--- and then I moved here...") 
      
      self.scr.refresh()   
      # OK - now we will see that the cursor has moved in mainwin.      
      self.mainwin.refresh() 
      
      self.cmdwin.addstr(1, 5, "This is the command window.") 
      self.cmdwin.refresh()
      
            
      # Handle keystrokes here.  
      # I have made this the job of the sheet. 
      # It was the job of the highlight before.   
   def action(self):  
      while (1):   
          # Display data on visible part of sheet.                     
          (self.y, self.x) = self.scr.getyx()             
          c=self.scr.getch()		
          if c in (curses.KEY_ENTER, 10):                
             curses.noecho()                 
             #h.move("D")   
             self.scr.refresh()   
                                                                                                         
          # Ctrl-G quits the app                  
          elif c==curses.ascii.BEL: 
             sys.exit(0) 
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
    while(1):  
       a = mywin(stdscr)  
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
     





