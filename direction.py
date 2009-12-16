
#  direction.py 
#  Gives the cell which is in a given direction 
#  from the supplied cell. 

# Get the letter or numeric part of a cell address (so that we can 
# manipulate it). 
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
def num2str(number): 
    result = []
    letters = ""
    while number > 0:
       result.append(number % 26)
       number /= 26
    # Convert the digits to letters   
    for x in result: 
       letters = letters + chr(64+x)    
    return letters[::-1] # reverse the string 


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



