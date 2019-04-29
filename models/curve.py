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

  def __str__(self):
    return "(p = %d, a = %d, b = %d)" % (self.__p, self.__a, self.__b)