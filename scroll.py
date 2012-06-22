


#  scroll.py 
#  A VERY basic app to test scrolling in curses. 
#  I have a LOT of problems with scrolling in curses, so this is for 
#  self-reference. 
#  This code is released to the public domain. 
#  "Share and enjoy...."  ;)  
 
 
import sys, itertools, types, math, curses, curses.ascii, string, os 
# Set the topmost and the leftmost boundaries for a cell.  
lbound = 7
tbound = 3                                     


# A cell class. 
class cell(object): 
   def __init__(self, scr, y, x, width, data):
      self.scr = scr 
      curses.noecho() 
      curses.cbreak()
      stdscr.keypad(1)
      self.scr.scrollok(1)
      self.scr.idlok(1)      
      self.scr.leaveok(0)
      
      # These are the SCREEN positions.            
      self.y = y
      self.x = x   
      
      # The ABSOLUTE positions. 
      self.absy = 0 
      self.absx = 0 
      
      # The boundaries of the screen 
      (y, x) = self.scr.getmaxyx() 
      
      # These are the maximum values that self.y and self.x 
      # can have. However, self.absy and self.absx can be 
      # larger than these (due to scrolling). 
      self.maxrows = y  
      self.maxcols = x  
      self.scr.setscrreg(0, self.maxrows-1)
             
      self.width = width   
      self.data = data     
      self.scr.addstr(self.y, self.x, str(self.data) )   
      self.scr.chgat(self.y, self.x, self.width, curses.A_STANDOUT) 
      self.scr.refresh()   
      
   # Move the highlight   
   def move(self, direction):   
      # Find the position of the highlight 
      (self.y, self.x) = self.scr.getyx()           
      # Remove the highlight from the current cell. 
      self.scr.chgat(self.y, self.x, self.width, curses.A_NORMAL) 
      if direction == "U": 
         if self.y > 0: 
            self.y -= 1  
            self.absy -= 1         
         elif self.y == 0 and self.absy > 0: 
            self.scr.scroll(1)   
            self.scr.refresh()  
         elif self.y == 0 and self.absy == 0:     
            pass    
      elif direction == "D":   
         # This is VERY important. 
         # Having this statement correct enables scrolling to work.    
         if self.y < (self.maxrows-1): 
            self.y += 1  
            self.absy += 1            
         else:                
            self.scr.scroll(1)   
            self.scr.refresh()         
               
      elif direction == "L": 
         if self.x >= self.width:  
            self.x -= self.width 
            self.absx -= self.width 
         else: 
            pass    
      elif direction == "R": 
         if self.x < (self.maxcols - self.width): 
            self.x += self.width 
            self.absx += self.width 
         else: 
            pass    
      # Show the highlight at the destination
      self.scr.chgat(self.y, self.x, self.width, curses.A_STANDOUT)  
      # Show the ABSOLUTE position of the cell 
      # self.data = str( '(' + self.absy + ',' + self.absx + ')' ) 
      
      #self.scr.addstr(self.y, self.x, str(self.data) ) 
        
      self.scr.refresh()               
   
   # Handle keystrokes here.  
   def action(self):  
      while (1):   
          # Display data on visible part of sheet.                     
          (self.y, self.x) = self.scr.getyx()             
          c=self.scr.getch()		
          if c in (curses.KEY_ENTER, 10):                
             curses.noecho()                 
             #h.move("D")   
             self.scr.refresh()   
          elif c==curses.KEY_UP:  
             curses.noecho()               
             self.move("U")             
             self.scr.refresh()
          elif c==curses.KEY_DOWN:
             curses.noecho()               
             self.move("D")                               
             self.scr.refresh()   
          elif c==curses.KEY_LEFT: 
             curses.noecho()               
             self.move("L")             
             self.scr.refresh()
          elif c==curses.KEY_RIGHT: 
             curses.noecho()              
             self.move("R")
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
       a = cell(stdscr, 3, 20, 7, "foo")            
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
     


