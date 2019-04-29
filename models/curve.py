class Curve(object):
  def __init__(self, p, a, b):
    self.__p = p
    self.__a = a
    self.__b = b

  def p(self):
    return self.__p

  def a(self):
    return self.__a

  def b(self):
    return self.__b

  def containsPoint(self, x, y):
    return (y * y - (x * x * x + self.__a * x + self.__b)) % self.__p == 0

  def calculateY(self, x):
    return pow(self.getCurveValue(x), (self.__p + 1) // 4, self.__p)

  def getCurveValue(self, x):
    return (pow(x, 3, self.__p) + (self.__a * x) + self.__b) % self.__p

  def __str__(self):
    return "(p = %d, a = %d, b = %d)" % (self.__p, self.__a, self.__b)

  def quadrTest(self, x):
    if self.getCurveValue(x) == 0:
        return False

    if pow(self.getCurveValue(x), ((self.__p - 1) // 2), self.__p) == 1:
        return True
    return False
  
  def delta(self):
    return (4 * pow(self.__a, 3)) + (27 * pow(self.__b, 2))
