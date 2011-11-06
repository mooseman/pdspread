

#  pdspreadtest.py 

 
import sys, re, types, itertools, math, curses, curses.ascii, traceback, string, os 

   
# Expand this to be a sheet class.  
# Use a dict to store data?     
class cell(object): 
   def __init__(self, y, x):  
      self.y = y 
      self.x = x       
      self.data = None 
   
   #  Store data. This can be done with a dict.  
   def set(self, data): 
      self.data = data 

   # Get data in a cell.  
   def get(self): 
      print self.data  

   def address(self): 
      print "(" + str(self.y) + "," + str(self.x) + ")"   


a = cell(3, 5) 

a.set("foo bar baz") 
a.get() 
a.address() 










