

# Acknowledgement - Very many thanks to Bill from 
# python-forum.org for doing this code.  

def num2str(n):
    assert isinstance(n,int) and n > 0
    digits = "-ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    res = []
    while True:
        n, r = divmod(n, 26)
        if r == 0:    # Adjust the quotient and remainder
            n, r = n-1, 26
        res[0:0] = digits[r]
        if n == 0:
            return "".join(res)
            
# Test the code 
for n in [1,2,3,25,26,27,675,676,677,701,702,703]:
   print "%4d ==> %s" % (n, num2str(n))
   

   
   

            
            
