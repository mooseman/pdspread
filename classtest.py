
# Classtest.py 
# Some code to play around with Python classes 

# A possible class hierarchy could look like this -  
# Address -> cell 
# Window -> sheet(window, cell)  




# This could be an address class 
class foo(object): 
   def init(self):
      self.data = "foo" 
      print self.data 
      # This is equivalent to self.agate = 123
      setattr(self, "agate", 123)
      
      
# This could be a cell class      
class bar(foo):
   def init2(self):
      self.data = "bar" 
      print self.data  
      # This is equivalent to self.jade = "foo bar baz" 
      setattr(self, "jade", "foo bar baz") 
      
# This could be a sheet class       
class baz(bar):       
   def __init__(self): 
      self.init() 
      self.init2()        
      self.data = "baz" 
      print self.data    
      # This is equivalent to self.quartz = [789, "test", 42]    
      setattr(self, "quartz", [789, "test", 42])      
            
a = baz() 

print dir(a) 
      



