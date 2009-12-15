

# Find the multiples of a number in a given base     
def newdivmod(num, base):     
    power = 0
    ans = 0 
    baselist = [] 
    anslist = [] 
    ans3list = [] 
    
    while (ans < num): 
       ans = (26 ** power) 
       if ans < num: 
          power += 1 
          
    # Now, divide the number by the powers of the base 
    powrange = range(power, -1, -1) 
    for i in powrange: 
      baselist.append(base ** i)         
        
    baserange = range(0, base+1)     
        
    for a in baselist: 
       ans3 = divmod(num, a) 
       for x in ans3: 
          if ans3[0] <= base and ans3[1] <= base:         
             ans3list.append(x) 
          else: 
             ans3 = divmod(x, a)                            
                           
    print num, base, power, powrange, baselist, ans3list  
    

newdivmod(17, 26) 
newdivmod(55, 26) 
newdivmod(670, 26) 
newdivmod(705, 26) 




