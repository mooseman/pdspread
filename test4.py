

# Convert a string of letters to a number
# NOTE! MAKE SURE THE STRING IS IN UPPER CASE!!!
def str2num(str): 
   num = []
   str2 = str.upper()
   l = len(str2)
      
   r = range(l-1, -1, -1) 

   for a,b in zip(str2, r):       
      res = (ord(a)-64) * (26**b)       
      num.append(res)  
      val = sum(num)
   print str, val 
                  

# Find the maximum power of 26 to go to when calculating a 
# string.             
def findmaxpower(x): 
    power = 0 
    mult = 0 
    ans = 0 
    mylist = [] 
    
# If we get to 26, then increment the power by 1. 
# Also reset mylist[0] to 0 
    
    while (ans < x):   
       ans = mult * (26 ** power)   
       if ans < x:      
          mult += 1             
       if mult == 26: 
          mult = 0 
          power += 1 
                       
    print x, mult, power           
          
            
            
            
def test(x): 
   multlist = [0]
   alist = [26] 
   powlist = [0] 
   
   mysum = 0 
   pow = 0    
   ans = 0
   
   # Need to get x in here.                   
   for a in range(0, 3):            
      quot, rem = divmod(x, (26**pow)) 
            
      if quot == 0: 
         ans = rem
      else: 
         pass 
            
                      
         '''if a == 26: 
            pow += 1                         
            multlist.append(quot)
            alist.append(a) 
            powlist.append(pow) '''
                                                      
   print quot, ans, rem, pow 
            
            
            
def num2str(x): 
    if x<26: s=chr(65+x)
    else:
	x=x-26
	s=chr(65+ (x//26) ) + chr(65+ (x%26) )    
    #return s  
    print x, s               
             
                            
str2num("A") 
str2num("B") 
str2num("C") 
str2num("X") 
str2num("Y") 
str2num("Z") 
str2num("AA") 
str2num("AB")        
str2num("AC")  
str2num("AY")  
str2num("AZ")  
str2num("BA")  
str2num("BB")  
str2num("BC")  
str2num("IV")
str2num("ZX")
str2num("ZY")
str2num("ZZ")
str2num("AAA")  
str2num("AAB")  
str2num("AAC")  


num2str(0)
num2str(1)
num2str(2)
num2str(3)
num2str(24)
num2str(25)
num2str(26) 
num2str(27)
num2str(28)
num2str(29) 
num2str(256)

#test(5) 
#test(34) 
findmaxpower(5) 
findmaxpower(34) 
findmaxpower(55) 
findmaxpower(83) 
findmaxpower(670) 
findmaxpower(690) 


