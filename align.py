

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


# Use divmod(a, b)  
def colhead(num):  
  if 0 <= num <= 26: 
     colhead = chr(num+64) 
  elif num > 26: 
     colheadpair = divmod(num, 26) 
     colhead = str(chr(colheadpair[0]+64) + chr(colheadpair[1]+64+1))      
  print colhead        
       
            
# Test the code 
colhead(10) 
colhead(26) 
colhead(27)
colhead(28) 
colhead(29) 
colhead(52)
colhead(53) 
colhead(54) 
colhead(78) 
colhead(79) 
colhead(80) 


def test(num): 
   res = divmod(num, 26) 
   print res 
   
test(10) 
test(26) 
test(27)
test(28) 
test(29) 
test(52)
test(53) 
test(54) 
test(78) 
test(79) 
test(80) 
   

def yx2str(y,x):
    "Convert a coordinate pair like 1,26 to AA2"
    if x<26: 
       s=chr(65+x)
    else:
       x=x-26
       s=chr(65+ (x/26) ) + chr(65+ (x%26) )
    s=s+str(y+1)
    return s
    
def x2str(x, width):
    myval = int(x/width)
    s=chr(65+myval)
    return s
    
coord_pat = re.compile('^(?P<x>[a-zA-Z]{1,2})(?P<y>\d+)$')

def str2yx(s):
    "Convert a string like A1 to a coordinate pair like 0,0"
    match = coord_pat.match(s)
    if not match: return None
    y,x = match.group('y', 'x')
    x = string.upper(x)
    if len(x)==1: 
       x=ord(x)-65
    else:
       x= (ord(x[0])-65)*26 + ord(x[1])-65 + 26
    return string.atoi(y)-1, x

print yx2str(0,0)     # 'A1'
print yx2str(0,25)    # 'Z1'
print yx2str(0,26)    # 'AA1'
print str2yx('A1')    # (0,0)
print str2yx('Z1')    # (0,1)
print str2yx('AA1')   # (0,26)




 
