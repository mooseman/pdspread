


#  cellclass.py 


# A test class to manipulate cell references 
# Look up the cell address (e.g. "C7"), get the screen 
# position, and do something with it. 

# NOTE - it is necessary to store this stuff in a separate dict 
# because "moving" (changing a cell reference) sometimes involves 
# deleting an existing dict entry and then replacing it with a modified 
# one. For example, if you are at the right edge of the screen and you are 
# scrolling right, the "position" entries will remain the same (e.g. (10, 25) ), 
# but the cell which is AT that position will change ( e.g. D, E, F, G, H..... ).  

import sys, types, math, curses, curses.ascii, string, os 


class test(object): 
   def __init__(self): 
      self.tdict = {} 
      
   # Proplist has the following - 
   # width, ypos, xpos    
   def add(self, cell, proplist): 
      if not self.tdict.has_key(cell): 
         self.tdict.update({cell: proplist})  
      else: 
         print "Key is already in dict"      
   
   def remove(self, cell): 
      if self.tdict.has_key(cell): 
         del self.tdict[cell] 
      else: 
         print "Key is not in dict"       
   
   def move(self, cell, direction): 
      if self.tdict.has_key(cell): 
         if direction == "U": 
            self.tdict[cell][1] -= 1 
         elif direction == "D":     
            self.tdict[cell][1] += 1 
         elif direction == "L": 
            self.tdict[cell][2] -= self.tdict[cell][0] 
         elif direction == "R": 
            self.tdict[cell][2] += self.tdict[cell][0]  
      else: 
            print "Key is not in dict"          
   
   def show(self, cell): 
      if self.tdict.has_key(cell): 
         print cell, self.tdict[cell]            
      else: 
         print "Key is not in dict"    


# Test the code 
a = test() 

a.add("A1", [7, 7, 3]) 
a.add("E7", [7, 13, 55]) 
a.show("E7") 
a.add("A1", [7, 23, 42]) 
a.move("E7", "R") 
a.show("E7") 
a.move("E7", "D")  
a.show("E7") 
a.remove("A1") 
a.show("A1")   
a.move("A1", "D") 


