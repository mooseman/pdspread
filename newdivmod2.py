

# Find the multiples of a number in a given base   

import string, itertools 
  
def newdivmod(num, base):     
    power = 0
    ans = 0 
    baselist = [] 
    anslist = [] 
    anslist2 = []  
   
    while (ans < num): 
       ans = (26 ** power) 
       if ans < num: 
          power += 1 
       else: 
          pass    
          
    # Now, divide the number by the powers of the base 
    # powrange is the range of the powers of the base (the powers of 26 
    # in this case) 
    powrange = range(power, -1, -1) 
    for i in powrange: 
      baselist.append(base ** i)         
    
    # The "base range (from 0 to 26 in this case)     
    baserange = range(0, base+1)     
    
    # Get all possible combinations of the powers and coefficients     
    for a in itertools.product(baselist, baserange):  
       if (a[0] * a[1]) <= num: 
          anslist.append(a) 
    
    for b, c in itertools.product(anslist, anslist): 
       if b[0]*b[1] + c[0]*c[1] == num: 
         anslist2.append([b])                       
                           
    print num, base, power, powrange, baselist, anslist2  
    

#newdivmod(17, 26) 
newdivmod(55, 26) 
#newdivmod(670, 26) 
#newdivmod(705, 26) 




