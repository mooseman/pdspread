

# base26.py 
# convert a number to an alphabetical string 
import string 

# 0, 1, 2, = A, B, C 
# 25, 26, 27 = Z, AA, AB 
# 50, 51, 52 = AZ, BA, BB  
'''def num2str(n):
    h = []
    while True:
        n,r = divmod(n,26)
        h[0:0] = chr(65+r)
        if n == 0:
            return ''.join(h)  '''

def num2str(x): 
   if x<26: s=chr(65+x)
   else:
      x=x-26
      s=chr(65+ (x/26) ) + chr(65+ (x%26) )      
   return s

                      
# Test the code 
print num2str(0) 
print num2str(6)
print num2str(24)  
print num2str(25)  
print num2str(26) 
print num2str(27)
print num2str(28)  
print num2str(49)
print num2str(50)
print num2str(51)  
print num2str(52)
print num2str(53)        
#print num2str(678) 

   
      





