

#  pdspreadtest.py 

 
import sys, re, types, itertools, math, curses, curses.ascii, traceback, string, os 
# Set the topmost and the leftmost boundaries for a cell.  
lbound = 7
tbound = 3                                     


# Do a function to convert numeric references e.g. (10, 5) to 
# cell references e.g. J5. Also a function to do the reverse.  
# See here - http://en.wikipedia.org/wiki/Bijective_numeration 

# Each digit position represents a power of twenty-six, so for 
# example AB is "one 26**1, plus two units (26**0)" 
# since "A" is worth one, "B" is worth two, "C" is worth three,...
# Z is worth 26.   
# chr(65) is 'A'.  chr(90) is 'Z'.   

# Use divmod here.   
def numtoletter(num):  
   if num <= 0: 
      res = "Too small" 
   elif 1 <= num <= 26: 
      res = str( ' ' + chr(num + 64) ) 
   elif 26 < num <= 702: 
      a = divmod(num, 26) 
      if a[1] == 0: 
         res = str( chr( (a[0]-1) + 64) + 'Z' )       
      else: 
         res = str( chr( (a[0]) + 64) + chr( a[1] + 64) ) 
   else: 
      res = "Too large"  
   print res              
      

# Convert a column letter (e.g. "BD") to the corresponding 
# column number.   
def lettertonum(letter): 
   if len(letter) == 2: 
      num1 = ord(letter[0]) - 64 
      num2 = ord(letter[1]) - 64       
      res = (num1 * 26**1) + (num2 * 26**0) 
   elif len(letter) == 1: 
      num1 = ord(letter) - 64
      res = (num1 * 26**0) 
   print res    


# Split the address of a cell into column and row 
def splitaddress(cell): 
   col = "" 
   row = 0
   index = 0
   
   for x in cell: 
      if x.isalpha():  
         col = col + x
         index += 1
      else: 
         row = int(cell[index:]) 
   splitaddress = [col, row]
   return splitaddress


   
# Expand this to be a sheet class.  
# Use a dict to store data     
class data(object): 
   def __init__(self):  
      self.mydict = {} 
   
   #  Store data in a cell. 
   #  TODO - do a range version of this. 
   def set(self, y, x, data): 
      self.y = y
      self.x = x 
      self.data = data 
      self.mydict.update({(self.y, self.x) : self.data})  
      
   # Get the data in a cell.  
   #  TODO - do a range version of this. 
   def get(self, y, x):  
      print self.mydict[y,x] 
   
   # Get all data in the dict.    
   def getall(self): 
      for key in self.mydict:
         print key[0], key[1], self.mydict[key] 
          
         
# Need code to draw a cell highlight.  
# Sheet class can use data code to draw row, col headings. 
# For movement - cell.move(right) - increment the 
# current-location col by 1 and redraw the cell. 

# It can store current position of highlight.  
# It will also have code to move the highlight.  
# Cell class. Have address. 
# Store currently-visible cells and if they have data, 
# display it.  

# Scrolling code. May do a separate class for this.  
# Could have a display class. It would have movement 
# (including scrolling) in it.  
# Move(cell) , move(sheet). 
# If we move the highlight past edge of screen, move the 
# sheet too (by updating the row/col headings and showing the 
# relevant stored data).     
   
   
   
# Test the code 
a = data() 

# Store some data 
a.set(3, 5, "foo bar baz") 
a.set(1, 1, "This is a test....")  
a.set(2, 7, 42805)  

# Retrieve data 
a.get(3,5)
a.get(1,1) 
a.get(2,7) 
a.getall()  


numtoletter(25)
numtoletter(26)
numtoletter(27)
numtoletter(28)
numtoletter(51)
numtoletter(52)
numtoletter(53)
numtoletter(54)
numtoletter(702)

lettertonum('Y') 
lettertonum('Z') 
lettertonum('AA') 
lettertonum('AB') 
lettertonum('AY') 
lettertonum('AZ') 
lettertonum('BA') 
lettertonum('BB') 
lettertonum('ZY') 
lettertonum('ZZ') 

print splitaddress("AB123") 
print splitaddress("C18") 
print splitaddress("EF7") 


