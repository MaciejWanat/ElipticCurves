 #!/usr/bin/python3

from mathHelper import randomP
from curveHelper import getPointWithCurve, calcNP, calcSecret, elipticCurve
from point import Point
from curve import Curve
from Crypto.Util import number
import sys

def main():
    p = randomP()
    nAlice = number.getRandomRange(0, 250000000000)
    nBob = number.getRandomRange(0, 250000000000)

    if len(sys.argv) > 1:
        nAlice = int(sys.argv[1])        
        if len(sys.argv) > 2:
            nBob = int(sys.argv[2])

    print('\n> Generate curve and point:')

    point = getPointWithCurve(p) 
    curve = point.curve()

    print(f'Curve:', curve)
    print(f'Point: ({point.x()}, {point.y()})')
    
    if not curve.contains_point(point.x(), point.y()):
        print('\nError! Point not on the curve!')
  
    print('\n> Alice nP:')
    aliceNP = calcNP(point, nAlice)
    print('\n> Bob nP:')
    bobNP = calcNP(point, nBob)    
  
    # Exchange points and calculate common secret
    aliceSecret = calcSecret(bobNP, nAlice)
    bobSecret = calcSecret(aliceNP, nBob)

    print('\n> Common secret calculation:')
    print(f'Alice secret: {aliceSecret}')
    print(f'Bob secret: {bobSecret}')
    print('\nSecrets equal:', bobSecret == aliceSecret)

if __name__ == '__main__':
   main()