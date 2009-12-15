
def to_base_26(number):
   result = []
   while number > 0:
      result.append(number % 26)
      number /= 26
   return result[::-1] # reverse it

num = 55
digits = to_base_26(num)
print "Base 26 digits are (MSB first):",digits
print num," = "," + ".join(["%d*26^%d"  % (x,i) for i,x in enumerate(reversed(digits))])


num = 705 
digits = to_base_26(num)
print "Base 26 digits are (MSB first):",digits
print num," = "," + ".join(["%d*26^%d"  % (x,i) for i,x in enumerate(reversed(digits))])


