
# Matrix.py 
# Acknowledgement - this code was done by "bvdet" from bytes.com here - 
# http://bytes.com/topic/python/answers/594203-please-how-create-matrix-python
# Very many thanks to bvdet for doing this! 
# Note - I've rearranged the code slightly by changing the order of the 
# parameters so that row always comes first and column second. 

# A simple matrix
# This matrix is a list of lists
# Column and row numbers start with 1

import string, itertools    

class cell(object): 
   def __init__(self, data): 
      self.data = str(data) 
      
   def __repr__(self): 
      return self.data
      

class matrix(cell):
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
              
   def __iter__(self):
       for row in range(self.rows):
           for col in range(self.cols):
               yield (self.matrix, row, col)  
               
   def next(self): 
       pass             
           
   def setitem(self, row, col, v):
       self.matrix[row-1][col-1] = v
       
   def setrange(self, rows, cols, data):
       #while True:  
         try:  
            for x, y, z in itertools.izip(range(rows[0], rows[1]), 
               range(cols[0], cols[1]), data): 
                  self.setitem(x, y, z) 
                  #self.matrix[x-1][y-1] = z 
         except StopIteration: 
            pass       
                           
   def getitem(self, row, col):       
       return self.matrix[row-1][col-1]
       
   def getrange(self, rows, cols): 
       reslist = []
       for x in range(rows[0], rows[1]+1): 
          for y in range(cols[0], cols[1]+1):    
             reslist.append(self.matrix[x-1][y-1])
             #return list(self.matrix[x-1][y-1]) 
             return reslist 
                                        
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
  s = chr(x) 
  c.append(s.center(7))  

# Set the column headings 
for a in range(2, 12):  
  b.setitem(1, a, c[a-2]) 

# Set the row headings 
for e in range(2, 22): 
  b.setitem(e, 1, e-1) 
      
# Now, store the cell positions in the matrix 
for r in range(2, 22): 
  for c in range(2, 12): 
     b.setitem(r, c, (r, (c*7)-7))  
                                           
#print b  

'''b.setitem(2, 2, 17) 
b.setitem(2, 3, 25) 
a = b.getitem(2, 2) + b.getitem(2, 3) 
#b.setitem(2, 4, a) 
b.setitem(2, 4, (b.getitem(2, 2) + b.getitem(2, 3))) 
print b  ''' 


c = matrix(21, 11) 
l = []
colnums = range(65, 75)

for x in colnums: 
  s = chr(x) 
  l.append(s) 

c.setrange((1,2), (2,12), l)      

rownums = range(1, 22)
c.setrange((2,22), (1,2), rownums)      
                       
#d = c.getrange((1,2), (2,11))                      

print l

print c 








