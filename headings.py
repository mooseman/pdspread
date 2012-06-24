


#  pdspread.py 
#  The beginnings of a Python spreadsheet. 
#  This code is released to the public domain. 
#  "Share and enjoy...."  ;)  
 
 
import sys, itertools, types, math, curses, curses.ascii, string, os 
         

class heading(object): 
   def __init__(self, posrange, datalist):      
      self.posrange = posrange
      self.datalist = datalist 
           
   def update(self, inc): 
      for x in self.datalist: 
         x += inc 
     

class thing(object): 
  def __init__(self, scr, ypos, xpos, val): 
     self.scr = scr
     self.ypos = ypos
     self.xpos = xpos     
     self.val = val 
     self.scr.refresh()
  
  def update(self, inc): 
     self.val += inc    
     self.scr.addstr(self.ypos, self.xpos, str(self.val) ) 
     self.scr.refresh() 


                                    
class sheet(heading): 
   def __init__(self, scr):       
      self.scr = scr  
      # TO DO: specify the range that the sheet shows 
      # when it is created. Also have a method that displays 
      # any data in that range. 
       
      # A number to use as a "dummy row or column heading" 
      self.mynum = 0 
       
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
      self.rh = heading(self.rowheadposlist, self.rowdata)  
      self.ch = heading(self.colheadposlist, self.coldata)   
      
      for x,y in zip(self.rowdata, self.rowheadposlist):
         self.scr.addstr(y[0], y[1], str(x) )  
         
      for x,y in zip(self.coldata, self.colheadposlist):
         self.scr.addstr(y[0], y[1], str(x) )   
      
      self.thing = thing(self.scr, 10, 55, 42)              
                                    
      self.scr.refresh()          
                         
      # TO DO: Need an update method for the headings. 
      # This will be used when we scroll across the page or 
      # up and down the page.     
                                         
      # Create a highlight
      #self.h = highlight(self.scr, 3, 20, 7) 
      #self.h = highlight(self.scr, 2, 7, 7) 
      # Create storage dict 
      #self.d = storage() 
              
                  
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
             self.thing.update(-1)                                                                                          
             self.scr.addstr(5, 20, "self.thing is " + str(self.thing.val) )              
             self.scr.refresh()
          elif c==curses.KEY_DOWN:
             curses.noecho()  
             self.thing.update(1)                                                                                                                                                                   
             self.scr.addstr(5, 20, "self.thing is " + str(self.thing.val) )               
             self.scr.refresh()   
          elif c==curses.KEY_LEFT: 
             curses.noecho()    
             (self.y, self.x) = self.scr.getyx()  
             self.scr.move(self.y, self.x-1)             
             self.scr.addstr(7, 20, "self.x is " + str(self.x) )                           
             self.scr.refresh()
          elif c==curses.KEY_RIGHT: 
             curses.noecho()              
             (self.y, self.x) = self.scr.getyx() 
             self.scr.move(self.y, self.x+1)              
             self.scr.addstr(7, 20, "self.x is " + str(self.x) )              
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
     

