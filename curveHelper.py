from Crypto.Util import number
from point import Point
from curve import Curve

def quadrTest(f, p):
    if f == 0:
        return False

    if(pow(f,((p-1)//2), p) == 1):
        return True
    return False

def getPointWithCurve(p):
    getRandom = lambda p: number.getRandomRange(0, p - 1)
    calcDelta = lambda a, b: (4 * pow(a, 3)) + (27 * pow(b, 2))

    a = 0
    b = 0
    x = 0
    delta = p
    while (delta % p == 0 or not quadrTest(elipticCurve(a,b,x,p), p)):
        a = getRandom(p)
        b = getRandom(p)
        x = getRandom(p)    
        delta = calcDelta(a, b)  
    else:
        curve = Curve(p, a, b)
        y = pow(elipticCurve(a, b, x, p), (p + 1) // 4, p)
        point = Point(curve, x, y)
        return point
    
def calcNP(point, n):   
    print(f'n: {n}')

    nP = point * n
    curve = point.curve()
    print(f'nP: {nP}')

    if not curve.contains_point(nP.x(), nP.y()):
        print('\nError! Point not on the curve!')

    return nP

def calcSecret(nP, yourSecret):
    commonSecret = nP * yourSecret
    return commonSecret

def elipticCurve(a, b, x, p):
    return (pow(x, 3, p) + (a * x) + b) % p