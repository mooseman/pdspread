

# align.py  
# Align a sequence of charcters depending on whether 
# it is a string or a number.  

import types, math, string, os, re  


def align(thing): 
   if 'int' in str(type(thing)): 
      retval = "right" 
   elif 'str' in str(type(thing)): 
      retval = "left"  
   elif 'list' in str(type(thing)): 
      retval = "list" 
   elif 'tuple' in str(type(thing)): 
      retval = "tuple"                    
   print retval             

# Test the code 
a = align(123) 
b = align("123") 
c = align([4,5,6]) 
d = align((42, "foo", 3.1415926) )





 
