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
              
   def __iter__(self):
       for row in range(self.rows):
           for col in range(self.cols):
               yield (self.matrix, row, col)
                          
   def setitem(self, row, col, v):
       self.matrix[row-1][col-1] = v
       
   def setrange(self, rows, cols, data):
       cells = list(itertools.product(range(rows[0], rows[1]),
          range(cols[0], cols[1]) ) )
       mydata = list(data)
       mylist = zip(cells, mydata)       
       for x in mylist:
           self.setitem(x[0][0], x[0][1], x[1])
                                   
   def getitem(self, row, col):
       return self.matrix[row-1][col-1]
       
   def getrange(self, rows, cols):
       reslist = []
       for x in range(rows[0], rows[1]+1):
          for y in range(cols[0], cols[1]+1):
             reslist.append(self.matrix[x-1][y-1])
             #return list(self.matrix[x-1][y-1])
             return reslist
                 
   def getrange2(self, rows, cols): 
       cells = list(itertools.product(range(rows[0], rows[1]),
          range(cols[0], cols[1]) ) )              
       for x in cells:
           return self.matrix[x[0]:x[1] ] 
                                           
   def __repr__(self):
       outStr = ""
       for i in range(self.rows):
           outStr += 'Row %s = %s\n' % (i+1, self.matrix[i])
       return outStr
  
 
# Run the code
# First (left) parameter is the rows, and the second (right) parameter
# is the columns.
c = matrix(6, 6)
l = []
colnums = range(65, 70)
 
for x in colnums:
  s = chr(x)
  l.append(s)
 
c.setrange((1,2), (2,7), l)
 
rownums = range(1, 6)
c.setrange((2,7), (1,2), rownums)
        
stuff = ["The", "quick", "brown", "fox", "jumps", "over",
   "the", "lazy", "dog"]
c.setrange((3,6), (3,6), stuff)
                                  
#print l
#print rownums
print c 
 
 
