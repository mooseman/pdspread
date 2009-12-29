

#  makecols.py 
#  Code to track the width of columns and fit as many as possible 
#  into a given screen width. 
#  Columns will have a default width. For this example, we make this 7.

import math, string, itertools  

# Helper function to convert a number to a column letter. 
def num2str(n):
    #assert isinstance(n,int) and n > 0
    digits = "-ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    res = []
    while True:
        n, r = divmod(n, 26)
        if r == 0:    # Adjust the quotient and remainder
            n, r = n-1, 26
        res[0:0] = digits[r]
        if n == 0:
            return "".join(res)


class page(object): 
  def __init__(self, scrwidth, defaultwidth): 
     self.collist = [] 
     self.colwidths = [] 
     self.scrwidth = scrwidth 
     self.defaultwidth = defaultwidth 
     self.numcols = int(math.floor(self.scrwidth / self.defaultwidth)) 
     # Populate the lists 
     for i in range(0, self.numcols):
        self.collist.append(chr(65+i)) 
        self.colwidths.append(self.defaultwidth) 
        
  # Add columns to the lists until we reach the screen width.       
  def add(self):       
     # The letter of the current rightmost column.  
     # Note - need to later update this to cater for multi-letter 
     # column names. 
     self.lastcol = self.collist[len(self.collist)-1] 
     self.newcol = num2str(len(self.collist)+1) 
     print self.lastcol, self.newcol   
     
  # Remove cols from the lists until the width is the screen width 
  # or less.    
  def remove(self):     
     pass 
          
  # A refresh method to recalculate the number of columns on the 
  # screen when a column has had its width changed.       
  def refresh(self):       
     pass 
  
  # A method to change the width of a column.    
  def setwidth(self, col, width): 
     if col in self.collist: 
        myindex = self.collist.index(col) 
        self.colwidths[myindex] = width     
     else: 
        pass    
                
  def display(self): 
     print self.collist, self.colwidths        


# Run the code 
a = page(80, 7)
a.setwidth('C', 4) 
a.setwidth('E', 11) 
a.add() 
a.display() 


