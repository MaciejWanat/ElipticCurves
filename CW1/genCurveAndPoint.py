 #!/usr/bin/python3

from Crypto.Util import number
INIT_PRIME_SIZE = 256

def randomP():
    p = number.getPrime(INIT_PRIME_SIZE)

    while(p % 4 != 3):
        p = number.getPrime(INIT_PRIME_SIZE)
    return p

def quadrTest(f, p):
    if f == 0:
        return False

    if(pow(f,((p-1)//2), p) == 1):
        return True
    return False

def createElipticCurve(p):
    getRandom = lambda p: number.getRandomRange(0, p - 1)

    calcDelta = lambda a, b: (4 * pow(a, 3)) + (27 * pow(b, 2))
    elipticCurve = lambda a, b, x: (pow(x, 3, p) + (a * x) + b) % p

    a = 0
    b = 0
    x = 0
    delta = p
    while (delta % p == 0 or not quadrTest(elipticCurve(a,b,x), p)):
        a = getRandom(p)
        b = getRandom(p)
        x = getRandom(p)    
        delta = calcDelta(a, b)  
    else:
        return a, b, x

def main():
    p = randomP()
    print(f'p: {p}')

    a, b, x = createElipticCurve(p)
    elipticCurve = lambda a, b, x: (pow(x, 3, p) + (a * x) + b) % p
    
    y = pow(elipticCurve(a, b, x), (p + 1) // 4, p)

    print(f'y: {y}')

    print(f'Point: ({x}, {y})')

    print('\nTest for correctness:')
    print(elipticCurve(a, b, x))
    print(pow(y, 2, p))
    print(pow(y, 2, p) == elipticCurve(a, b, x))

if __name__ == '__main__':
   main()