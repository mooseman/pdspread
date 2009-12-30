

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
     self.total_colwidths = sum(self.colwidths)          
     self.newcol = num2str(len(self.collist)+1) 
     # If the totsl column width is less than the screen width, add 
     # as many columns as will fit in the screen width. 
     while (self.total_colwidths + self.defaultwidth) < self.scrwidth:        
           self.newcol = num2str(len(self.collist)+1)          
           # Add the new columns to the lists
           self.collist.append(self.newcol) 
           self.colwidths.append(self.defaultwidth) 
           self.total_colwidths = sum(self.colwidths)
                        
  # Remove cols from the lists until the width is the screen width 
  # or less. This method actually "removes" columns by iterating over 
  # the columns from left to right, keeping them while the total column 
  # width is less than the screen width.            
  def remove(self):                  
     self.newcolwidths = [] 
     
     for i, v in enumerate(self.colwidths): 
        if sum(self.colwidths[0:i]) + v < self.scrwidth:         
           self.newcolwidths.append(v)            
        else:
           break
     # Set the values of our lists to the newly-created ones.
     self.collist = self.collist[0:i]
     self.colwidths = self.newcolwidths 
                                  
  # A refresh method to test the total column widths and recalculate 
  # how many columns to display on the screen.    
  def refresh(self):       
     self.total_colwidths = sum(self.colwidths)             
     if self.total_colwidths < self.scrwidth: 
        self.add() 
     else: 
        self.remove()    
     
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
a.setwidth('A', 20) 
a.setwidth('B', 15) 
a.setwidth('C', 15)
a.setwidth('D', 20)
a.refresh() 
a.display() 
#a.refresh() 
#a.display() 


