
#  direction.py 
#  Gives the cell which is in a given direction 
#  from the supplied cell. 
# Acknowledgement: Very many thanks to those in pythonforum.org who 
# have helped me with my questions there. In particular, Bill there 
# supplied the code used in the num2str function here.

# This code is released to the public domain. 

def getpart(cell, part): 
  letters = "" 
  numbers = "" 
        
  for x in cell: 
     if x.isalpha(): 
        letters += x 
     elif x.isdigit(): 
        numbers += x 
     else: 
        pass    
        
  numbers = int(numbers)         
     
  if part.upper() == "A": 
     return letters
  elif part.upper() == "N":
     return numbers 


# Convert a "column number" to the column letter(s) 
# See if this can be restricted to the range 1-26 inclusive.
def num2str(n):
    assert isinstance(n,int) and n > 0
    digits = "-ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    res = []
    while True:
        n, r = divmod(n, 26)
        if r == 0:    # Adjust the quotient and remainder
            n, r = n-1, 26
        res[0:0] = digits[r]
        if n == 0:
            return "".join(res)


# Convert "column letter(s)" to the column number   
def str2num(str): 
    num = 0 
    mylen = len(str) 
    # A list of the powers of 26 that we need for the calculations
    powerlist = range(mylen-1, -1, -1) 
    for a,b in zip(str.upper(), powerlist):
       num += (ord(a)-64) * (26**b)       
    return num    


def dir(cell, dir):   
   letters = getpart(cell, "A") 
   numbers = getpart(cell, "N")   
   # Convert the letter part of the address to a number 
   colnum = str2num(letters) 
   
   if dir.upper() == "L": 
      if colnum > 1: 
         colnum -= 1 
         result = str(num2str(colnum) + str(numbers)) 
      else: 
         result = None  
   elif dir.upper() == "R": 
      colnum += 1 
      result = str(num2str(colnum) + str(numbers)) 
   elif dir.upper() == "U": 
      if numbers > 1: 
         numbers -= 1 
         result = str(num2str(colnum) + str(numbers))             
      else: 
         result = None 
   elif dir.upper() == "D": 
      numbers += 1 
      result = str(num2str(colnum) + str(numbers))             
      
   return result    
   
#  Test the code 
print dir("C5", "L") 
print dir("C5", "R") 
print dir("C5", "U") 
print dir("C5", "D")    
print dir("A1", "L")    
print dir("A1", "U")    
print dir("A1", "R")    
print dir("A1", "D")    
print dir("Z1", "R")    
print dir("AA1", "L")    
#print str2num("Z") 
#print str2num("AA") 
print num2str(27)
print num2str(26) 
print num2str(25) 
print num2str(1) 


