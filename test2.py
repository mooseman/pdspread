

# Convert a string of letters to a number
# NOTE! MAKE SURE THE STRING IS IN UPPER CASE!!!
def test(str): 
   num = []
   str2 = str.upper()
   l = len(str2)
      
   r = range(l-1, -1, -1) 

   for a,b in zip(str2, r):       
      c = ord(a) 
      d = c-64  #* (26**b)     
      res = d*(26**b)   
      num.append(res)  
      val = sum(num)
      print a, b, c, d, num, res, val 
      
test("A") 
test("B") 
test("C") 
test("X") 
test("Y") 
test("Z") 
test("AA") 
test("AB")        
test("AC")  
