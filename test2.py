


#  test.py 

def test(num): 
  
  a = divmod(num, 26) 
  
  #if a[0] == 0: 
  #   pass 
  
  if a[1] == 0: 
     num1 = a[0]-1 
     num2 = 26
  else: 
     num1 = a[0]
     num2 = a[1] 
     
  l1 = chr(num1 + 64)
  l2 = chr(num2 + 64)       

  print str(l1 + l2) 
  
  
test(25) 
test(26)
test(27) 
test(51)
test(52)
test(53)
test(700)
test(701)
test(702) 


  
