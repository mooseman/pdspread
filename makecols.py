

#  makecols.py 
#  Code to track the width of columns and fit as many as possible 
#  into a given screen width. 
#  Columns will have a default width. For this example, we make this 7.

import math, string, itertools  

class page(object): 
  def __init__(self, scrwidth, defaultwidth): 
     self.collist = [] 
     self.colwidths = [] 
     self.scrwidth = scrwidth 
     self.defaultwidth = defaultwidth 
     self.numcols = math.floor(self.scrwidth / self.defaultwidth) 
     # Populate the lists 
     for i in range(0, self.numcols):
        self.collist.append(chr(65+i)) 
        self.colwidths.append(self.defaultwidth) 
        
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
a.display() 


