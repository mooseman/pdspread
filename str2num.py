

#  str2num.py 
#  Convert a column string to a number 

def str2num(str): 
    num = 0 
    mylen = len(str) 
    # A list of the powers of 26 that we need for the calculations
    powerlist = range(mylen-1, -1, -1) 
    for a,b in zip(str.upper(), powerlist):
       num += (ord(a)-64) * (26**b)       
    return num    
    
# Test the code 
print str2num("G") 
print str2num("Z") 
print str2num("AA") 
print str2num("BE") 
print str2num("AAC") 

    
