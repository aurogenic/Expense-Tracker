import math
from numerize.numerize import numerize
def format (n, i=4):
    i -= 1 if n < 0 else 0
    sign = '-' if n<0 else ''
    n = abs(n)
    digits = int(math.log10(n)) + 1
    if digits <= i or i < 3:
        i -= digits
        st = str( round(n, i) + 1 / 10**(i+1))[:i+1+digits]
        st = st if i > 0 else st[:-1]
        return  sign + st
    suffices = ['', 'k', 'M', 'B', 'T']
    mg = min((digits - 1) // 3, len(suffices) -1)
    n = n / 10**(mg * 3)
    return  sign + format(n, i-1) + suffices[mg]

    



print(format(123456789,7 ))
# print(format(12345, 4))

# print(numerize(12345 + 1 / 10**3, 5))