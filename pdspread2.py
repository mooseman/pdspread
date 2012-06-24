


#  pdspread.py 
#  The beginnings of a Python spreadsheet. 
#  This code is released to the public domain. 
#  "Share and enjoy...."  ;)  
 
 
import sys, itertools, types, math, curses, curses.ascii, string, os 
# Set the topmost and the leftmost boundaries for a cell.  
lbound = 7
tbound = 3                                     


class storage(): 
   def __init__(self):  
      # Create the dictionary to store data. 
      self.mydict = {}  
      
   def add(self, index, data):         
      # Index is the ABSOLUTE address of a cell. 
      self.index = index        
      self.data = data 
      # Store the data 
      self.mydict[index] = self.data  
            
   def show_all(self): 
      for k, v in self.mydict: 
         print k, v  
         
   def show_cell(self, index): 
      print index, self.mydict[index]       
         


# A highlight class. 
class highlight(object): 
   def __init__(self, scr, y, x, width):
      self.scr = scr 
      
      # An "update headings" tuple. 
      # This is used to find out if the headings need to be 
      # updated (when scrolling).                 
      # Gives the heading to update, and the increment to use.       
      self.hupdate = ("", 0) 
            
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
      
      # Width of the highlight.        
      self.width = width     
      # Show the highlight.     
      self.scr.chgat(self.y, self.x, self.width, curses.A_STANDOUT) 
      self.scr.refresh()   
      
   # Move the highlight   
   def move(self, direction):   
      # Find the position of the highlight 
      (self.y, self.x) = self.scr.getyx()           
      # Remove the highlight from the current cell. 
      self.scr.chgat(self.y, self.x, self.width, curses.A_NORMAL) 
      if direction == "U": 
         if self.y > 2: 
            self.y -= 1  
            self.absy -= 1         
         elif self.y == 2 and self.absy > 0: 
            self.scr.scroll(1)  
            # Update row headings 
            self.hupdate = ("R", -1)             
            self.scr.refresh()  
         elif self.y == 2 and self.absy == 0:     
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
         if self.x >= (7 + self.width):  
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
      self.scr.refresh()               
   

                                    
class sheet(highlight, storage): 
   def __init__(self, scr):       
      self.scr = scr  
      # TO DO: specify the range that the sheet shows 
      # when it is created. Also have a method that displays 
      # any data in that range. 
       
      curses.noecho() 
      curses.cbreak()
      stdscr.keypad(1)
      self.scr.scrollok(1)
      self.scr.idlok(1)      
      self.scr.leaveok(0)
      
      # The boundaries of the screen 
      (y, x) = self.scr.getmaxyx() 
      
      # These are the maximum values that self.y and self.x 
      # can have. However, self.absy and self.absx can be 
      # larger than these (due to scrolling). 
      self.maxrows = y  
      self.maxcols = x  
      
      # Set the scroll region. 
      # Setting the first parameter to 2 means that our column 
      # headings do not scroll off the screen. 
      self.scr.setscrreg(2, self.maxrows-1)               
       
      # Create the headings 
      # Simpler to do this in this class (rather than having a 
      # separate heading class). We will have an update method for 
      # the headings. 
       
      # First, we set our "displayed range" - this is the 
      # **absolute range** of cells that are shown on the screen.       
      self.rowrange = list(range(1, self.maxrows) )  
      self.colrange = list(range( 10, self.maxcols, 7) )    
      
      # The positions of the row headings       
      self.rowheadposlist = list((y,x) 
         for y in range(2, self.maxrows) 
            for x in range(2, 3) )  
      self.rowdata = self.rowrange 
      
      self.colheadposlist = list( (y,x) 
         for y in range(1, 2) 
            for x in range(10, self.maxcols, 7) )  
      self.coldata = list( chr(x) for x in range(65,78) )         
           
      # Show the headings 
      for x,y in zip(self.rowdata, self.rowheadposlist):
         self.scr.addstr(y[0], y[1], str(x) )              
      
      for x,y in zip(self.coldata, self.colheadposlist):
         self.scr.addstr(y[0], y[1], str(x) )   
                         
      # TO DO: Need an update method for the headings. 
      # This will be used when we scroll across the page or 
      # up and down the page.     
                                         
      # Create a highlight
      #self.h = highlight(self.scr, 3, 20, 7) 
      self.h = highlight(self.scr, 2, 7, 7) 
      # Create storage dict 
      self.d = storage() 
              
                 
   def add_data(self, abs_address, mydata): 
      self.index = (abs_address[0], abs_address[1]) 
      self.data = mydata 
      # Save the data in the dictionary 
      self.d[index] = self.data             
  
   # Update the headings. 
   def update_headings(self, htype, inc): 
      if htype == "R": 
         for x in self.rowdata: 
            x += inc 
         for x,y in zip(self.rowdata, self.rowheadposlist):
            self.scr.addstr(y[0], y[1], str(x) )      
            
      elif htype == "C": 
         for x in self.coldata: 
            x += inc 
         for x,y in zip(self.coldata, self.colheadposlist):
            self.scr.addstr(y[0], y[1], str(x) )   
      # Refresh the screen                
      self.scr.refresh()                  
       
               
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
          elif c==curses.KEY_UP:  
             curses.noecho()  
             if self.h.y == 2 and self.h.absy > 0: 
                self.update_headings("R", -1) 
             else: 
                pass 
                          
             self.h.move("U")             
             self.scr.refresh()
          elif c==curses.KEY_DOWN:
             curses.noecho()  
             if self.h.y == self.maxrows: 
                self.update_headings("R", 1) 
             else: 
                pass 
                          
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
     


