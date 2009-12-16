



def num2str(number): 
    result = []
    letters = ""
    while number > 0:
       result.append(number % 26)
       number /= 26
    # Convert the digits to letters   
    for x in result: 
       letters = letters + chr(64+x)
    #return result[::-1]  # reverse it 
    return letters[::-1] 

print num2str(10)
print num2str(33)
print num2str(55)
print num2str(705)
