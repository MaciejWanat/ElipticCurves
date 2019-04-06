# wylosowanie krzywej + pkt
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

    delta = p
    while (delta % p == 0):
        a = getRandom(p)
        b = getRandom(p)
        x = getRandom(p)    
        delta = calcDelta(a, b)  
    else:
        return elipticCurve(a, b, x)

def main():
    p = randomP()
    print('p: ', p)

    elipticCurve = 0
    while(not quadrTest(elipticCurve, p)):
        elipticCurve = createElipticCurve(p)
        print(elipticCurve)

if __name__ == '__main__':
   main()