
# Classtest.py 
# Some code to play around with Python classes 

# This could be an address class 
class foo(object): 
   def init(self):
      self.data = "foo" 
      print self.data 
      
   def foo_meth(self, stuff): 
      print stuff    
      
# This could be a cell class      
class bar(foo):
   def init2(self):
      self.data = "bar" 
      print self.data   
      
# This could be a sheet class       
class baz(bar):       
   def __init__(self): 
      self.init() 
      self.init2()        
      self.data = "baz" 
      print self.data       
      self.foo_meth("Just a test")       
a = baz() 


      



