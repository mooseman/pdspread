

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
      
       
def num2str(x):       
   myval = x 
   i=0   
          
   #res[i] = (ord(65xxx)) * (26**i) + chr(65+(x%26))   
     
   if x<26: s=chr(65+myval)
   else:
      x=myval-26
      s=chr(65+ (x/26) ) + chr(65+ (x%26) )      
   print myval, x, s
          
                            
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
str2num("ZZ")  


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



