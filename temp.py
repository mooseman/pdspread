

#  temp.py 

import itertools 

l = [1, 2, 3, 4, 5, 6, 7, 8]

def test(num): 
   return list(itertools.takewhile(lambda x: x+x < num, l)) 
   
#  run the code 
#print test(10) 

def test2(num): 
   return [ l[0:x] for x in range(0, len(l)-1) if sum(l[0:x]) <= num]           
#  Run the code 
print test2(10) 
         
         



