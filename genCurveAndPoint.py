 #!/usr/bin/python3

from Crypto.Util import number
from point import Point, CurveFp
import sys
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
    
def CalcNP(n, p, a, b, x, y):   
    # multiplying n * p
    print(f'n: {n}')
    curve = CurveFp(p, a, b)
    point = Point(curve, x, y)

    nP = point.__mul__(n)
    print(f'nP: {nP}')

    print('\nTest for correctness:')
    print(elipticCurve(a, b, nP.x(), p))
    print(pow(nP.y(), 2, p))
    print(pow(nP.y(), 2, p) == elipticCurve(a, b, nP.x(), p))

    return nP

def CalcSecret(nP, yourSecret):
    commonSecret = nP.__mul__(yourSecret)
    return commonSecret

def elipticCurve(a, b, x, p):
    return (pow(x, 3, p) + (a * x) + b) % p

def main():
    p = randomP()
    nAlice = number.getRandomRange(0, 250000000000)
    nBob = number.getRandomRange(0, 250000000000)

    if len(sys.argv) > 1:
        nAlice = int(sys.argv[1])        
        if len(sys.argv) > 2:
            nBob = int(sys.argv[2])

    print('\nGenerate curve and point: \n')
    print(f'p: {p}')

    a, b, x = createElipticCurve(p)    
    y = pow(elipticCurve(a, b, x, p), (p + 1) // 4, p)
    
    print(f'y: {y}')
    print(f'Point: ({x}, {y})')

    print('\nTest for correctness:')
    print(elipticCurve(a, b, x, p))
    print(pow(y, 2, p))
    print(pow(y, 2, p) == elipticCurve(a, b, x, p))
  
    print('---------------------------------------------')
    print('\nAlice nP:')
    AliceNP = CalcNP(nAlice, p, a, b, x, y)
    print('\nBob nP:')
    BobNP = CalcNP(nBob, p, a, b, x, y)    
  
    # Exchange points and calculate common secret
    AliceSecret = CalcSecret(BobNP, nAlice)
    BobSecret = CalcSecret(AliceNP, nBob)

    print('---------------------------------------------')
    print('Common secret calculation:')
    print(f'\nAlice secret: {AliceSecret}')
    print(f'Bob secret: {BobSecret}')
    print('\nTest for correctness:')
    print(BobSecret.x() == AliceSecret.x() and AliceSecret.y() == BobSecret.y())    

if __name__ == '__main__':
   main()