


#  update.py 
#  Playing around with updating things in a curses window. 
#  This is aimed at getting row and column heading updates to 
#  work for pdspread. 

#  This code is released to the public domain. 
#  "Share and enjoy...."  ;)  
 
 
import sys, itertools, types, math, curses, curses.ascii, string, os 
         

class heading(object): 
   def __init__(self, posrange, datalist):      
      self.posrange = posrange
      self.datalist = datalist 
           
     
# An object to play around with. 
# Stores a value and has an update method. 
class thing(object): 
  def __init__(self, scr, ypos, xpos, val): 
     self.scr = scr
     self.ypos = ypos
     self.xpos = xpos     
     self.val = val 
     self.scr.addstr(self.ypos, self.xpos, "My value: " 
        + str(self.val) ) 
     self.scr.refresh()
  
  # Increment method. Update val by a set number
  def inc(self, inc): 
     self.val += inc          
     # Write new value 
     # The spaces after the value are so that we 
     # properly overwrite what was there before. 
     self.scr.addstr(self.ypos, self.xpos, "New value: " 
        + str(self.val) + "     " ) 
     self.scr.refresh() 
     
  # Set value to a particular value    
  def set(self, val): 
     self.val = val      
     # Write new value 
     # The spaces after the value are so that we 
     # properly overwrite what was there before. 
     self.scr.addstr(self.ypos, self.xpos, "New value: " 
        + str(self.val) + "     " ) 
     self.scr.refresh()    


# An "array thing" to play with and to update.  
class arrthing(object): 
   def __init__(self, scr, posarr, dataarr): 
      self.scr = scr 
      self.posarr = posarr 
      self.dataarr = dataarr 
      for x,y in zip(self.dataarr, self.posarr):
         self.scr.addstr(y[0], y[1], str(x) ) 
      self.scr.refresh()    
      
   def inc(self, myint): 
      for index, item in enumerate(self.dataarr):  
        self.dataarr[index] += myint
               
      # Write new value 
      # The spaces after the value are so that we 
      # properly overwrite what was there before. 
      for x,y in zip(self.dataarr, self.posarr):
         self.scr.addstr(y[0], y[1], str(x) + "     " )      
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
      
      (self.y, self.x) = self.scr.getyx()    
      
      # Create a few "thing" objects. 
      self.thing1 = thing(self.scr, 5, 10, 42)    
      self.thing2 = thing(self.scr, 7, 10, self.y) 
      self.thing3 = thing(self.scr, 9, 10, self.x) 
      self.thing4 = arrthing(self.scr, [ (11,10), (11,15), (11,20), 
         (11,25) ], [1, 2, 3, 4] )        
      # Move away       
      
      self.scr.move(10, 30)     
      #self.scr.addstr(self.y, self.x, str(self.thing4) )
                                             
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
             # Update our thing. This could be made conditional on 
             # being at the edge of a screen - exactly what is 
             # needed for heading updates.              
             self.thing1.inc(-5)               
             self.thing2.set(self.y-1)   
             self.thing3.set(self.x)   
             self.scr.move(self.y-1, self.x)                                                                                                                                                       
             self.scr.refresh()
          elif c==curses.KEY_DOWN:
             curses.noecho() 
             # Update our thing. This could be made conditional on 
             # being at the edge of a screen - exactly what is 
             # needed for heading updates.               
             self.thing1.inc(5)                      
             self.thing2.set(self.y+1)     
             self.thing3.set(self.x)   
             self.scr.move(self.y+1, self.x)                                                                                                                                                                                                          
             self.scr.refresh()   
          elif c==curses.KEY_LEFT: 
             curses.noecho()                
             self.thing2.set(self.y)     
             self.thing3.set(self.x-1)  
             self.thing4.inc(-1)  
             self.scr.move(self.y, self.x-1)                                                                        
             self.scr.refresh()
          elif c==curses.KEY_RIGHT: 
             curses.noecho()                
             self.thing2.set(self.y)     
             self.thing3.set(self.x+1)  
             self.thing4.inc(1) 
             self.scr.move(self.y, self.x+1)                                                                     
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
     

