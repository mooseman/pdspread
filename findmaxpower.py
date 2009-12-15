


# findmaxpower.py 
# Find the highest power to use when calculating a string 
def findmaxpower(x):
    power = 0
    mult = 0
    ans = 0
    
    while (ans < x):
       ans = (26 ** power) 
       ans2 = divmod(x, 26) 
       if ans2[0] > 26: 
          ans3 = divmod(ans2[0], 26)    
       else:    
          ans3 = 0                
       if ans < x:
          power += 1
                           
    print x, ans, ans2, ans3, power 
    
    
# Test the code 
findmaxpower(5) 
findmaxpower(34) 
findmaxpower(77) 
findmaxpower(670) 
findmaxpower(705)     


