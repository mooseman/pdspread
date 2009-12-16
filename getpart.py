

# getpart.py 

# Get the string or numeric part of a cell address 

import string 

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
     
# Test the code
print getpart("FH15", "A")
print getpart("G57", "A")
print getpart("ES15", "N")
print getpart("G57", "N")
         
         
