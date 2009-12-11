



import curses.ascii, re, string   

coord_pat = re.compile('^(?P<x>[a-zA-Z]{1,2})(?P<y>\d+)$')

def x2str(x):
    "Convert a column number number like 26 to AA2"
    if x<26: s=chr(65+x)
    else:
	x=x-26
	s=chr(65+ (x/26) ) + chr(65+ (x%26) )    
    return s

# Look at doing a version of this which takes into account the 
# screen width and the default column width. This will let you 
# easily calculate the actual position of a column on the screen. 
# Notes on doing this - (let's use an example column - S
# Find the number of columns which will fit across the screen. Need to 
# use max_x and width for this. 
# Create a function which "counts" using letters, like this - 
# A, b, c, ... x, y, z, aa, ab, ac, ad, ... 
# Using the above function, find how many "screen widths" you need 
# before you get to a given column. For example, if we can fit 8 columns
# on the screen, and we look at col S, we need 2 "screens" plus 3 columns 
# to get to S (the 19th letter).   

def str2yx(s):    
    "Convert a string like A1 to a coordinate pair like 0,0"
    match = coord_pat.match(s)
    if not match: return None
    y,x = match.group('y', 'x')
    x = string.upper(x)
    if x == "A": width = 0
    else: width = 7    
    if len(x)==1: x=ord(x)-56 + ( (ord(x)-65) * width) 
    else:
	x= (ord(x[0])-56+width)*26 + ord(x[1])-56+width + 26
    return string.atoi(y)+1, x
        
                
print str2yx("a1")
print str2yx("b1")
print str2yx("c1") 
print str2yx("a2")
print str2yx("a3")
print str2yx("e7") 
print str2yx("h15") 
#print str2yx("ad5") 

print x2str(0)  
print x2str(1)
print x2str(2) 
print x2str(25)
print x2str(26)
print x2str(27)
print x2str(51)
print x2str(52)
print x2str(53)
      
         
        
