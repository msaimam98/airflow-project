import sys
CHOOSE = ['divide', 'multiply', 'subtract', 'add']

def divide(num, denom):
    # num = kwargs['templates_dict']['a3']
    # denom = kwargs['templates_dict']['b3']
    # if isinstance(num1, int):
    #     num = num1
    # if isinstance(denom1, int):
    #     denom = denom1
    return float(num)/float(denom)

def multiply(num, denom):

    return float(num) * float(denom)

def subtract(num, denom):

    return float(num) - float(denom)

def add(num, denom):

    return float(num) + float(denom)

if __name__ == "__main__":
    newnew = []
    for item in sys.argv:
        newnew.append(item)
    if newnew[1] == CHOOSE[0]:
        to_print = divide(newnew[2], newnew[3])
    elif newnew[1] == CHOOSE[1]:
        to_print = multiply(newnew[2], newnew[3])
    elif newnew[1] == CHOOSE[2]:
        to_print = subtract(newnew[2], newnew[3])
    else:
        to_print = add(newnew[2], newnew[3])
    print(to_print)








