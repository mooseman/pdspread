

#  test.py 

def x2str(x, width): 
    myval = int(x/width) 
    s=chr(66+myval)    
    return s     
    
width = 15 

for x in range(20, 75, 15): 
   print x2str(x, width) 
   
    





