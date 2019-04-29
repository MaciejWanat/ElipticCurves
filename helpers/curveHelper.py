from Crypto.Util import number
from models.point import Point
from models.curve import Curve

def getPointWithCurve(p):
    curve, x = getRandomCurveAndX(p)

    while (curve.delta() % p == 0 or not curve.quadrTest(x)):
        curve, x = getRandomCurveAndX(p)

    y = curve.calculateY(x)
    point = Point(curve, x, y)
    
    return point
    
def calcNP(point, n):   
    print(f'n: {n}')

    nP = point * n
    curve = point.curve()
    print(f'nP: {nP}')

    if not curve.containsPoint(nP.x(), nP.y()):
        print('\nError! Point not on the curve!')

    return nP

def calcSecret(nP, yourSecret):
    commonSecret = nP * yourSecret
    return commonSecret

def getRandomCurveAndX(p):
    a = getRandomNumber(p)
    b = getRandomNumber(p)
    x = getRandomNumber(p)

    curve = Curve(p, a, b)

    return curve, x

def getRandomNumber(max):
    return number.getRandomRange(0, max - 1)