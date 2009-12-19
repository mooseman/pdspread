
# Matrix.py 
# Acknowledgement - this code was done by "bvdet" from bytes.com here - 
# http://bytes.com/topic/python/answers/594203-please-how-create-matrix-python
# Very many thanks to bvdet for doing this! 
# Note - I've rearranged the code slightly by changing the order of the 
# parameters so that row always comes first and column second. 

# A simple matrix
# This matrix is a list of lists
# Column and row numbers start with 1
  
class matrix(object):
   def __init__(self, rows, cols):
       self.rows = rows
       self.cols = cols
       
       # initialize matrix and fill with zeroes
       self.matrix = []
       for i in range(rows):
           ea_row = []
           for j in range(cols):
               ea_row.append(0)
           self.matrix.append(ea_row)
  
   def setitem(self, row, col, v):
       self.matrix[row-1][col-1] = v
  
   def getitem(self, row, col):       
       return self.matrix[row-1][col-1]
       
   def __repr__(self):
       outStr = ""
       for i in range(self.rows):
           outStr += 'Row %s = %s\n' % (i+1, self.matrix[i])
       return outStr
  

# Run the code  
# First (left) parameter is the rows, and the second (right) parameter 
# is the columns.   
a = matrix(4,4)
print a
a.setitem(3,4,'55.75')
print a
a.setitem(2,3,'19.1')
print a
print a.getitem(3,4)


b = matrix(21, 11) 
c = [] 

colnums = range(65, 75)
for x in colnums: 
  c.append(chr(x))    

# Set the column headings 
for a in range(2, 12):  
  b.setitem(1, a, c[a-2]) 

# Set the row headings 
for e in range(2, 22): 
  b.setitem(e, 1, e-1) 
      
print b  

b.setitem(2, 2, 17) 
b.setitem(2, 3, 25) 
a = b.getitem(2, 2) + b.getitem(2, 3) 
#b.setitem(2, 4, a) 
b.setitem(2, 4, (b.getitem(2, 2) + b.getitem(2, 3))) 
print b 





