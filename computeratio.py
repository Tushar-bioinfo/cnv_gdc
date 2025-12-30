#from decimal import *
#import sys
### Used inside main code to compute ratio of tumor to normal counts with 2 decimal precision
#def computeratio(tumor_count:int,normal_count:int)-> Decimal:
#    getcontext().prec = 2
#    return ( Decimal(tumor_count) / Decimal(normal_count))


from decimal import Decimal, InvalidOperation, DivisionByZero

def computeratio(tumor_count, normal_count):
    try:
        tumor = Decimal(int(tumor_count))
        normal = Decimal(int(normal_count))
        if normal == 0:
            return None   # or Decimal("0"), or "NA"
        return tumor / normal
    except (InvalidOperation, ValueError, TypeError, DivisionByZero):
        return None
