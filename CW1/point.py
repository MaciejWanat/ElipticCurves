#! /usr/bin/env python3

import numbertheory

class CurveFp(object):
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

  def contains_point(self, x, y):
    return (y * y - (x * x * x + self.__a * x + self.__b)) % self.__p == 0

  def __str__(self):
    return "CurveFp(p=%d, a=%d, b=%d)" % (self.__p, self.__a, self.__b)

class Point(object):
  def __init__(self, curve, x, y, order=None):
    self.__curve = curve
    self.__x = x
    self.__y = y
    self.__order = order

    if self.__curve:
      assert self.__curve.contains_point(x, y)
    if order:
      assert self * order == INFINITY

  def __add__(self, other):
    if other == INFINITY:
      return self
    if self == INFINITY:
      return other
    assert self.__curve == other.__curve
    if self.__x == other.__x:
      if (self.__y + other.__y) % self.__curve.p() == 0:
        return INFINITY
      else:
        return self.double()

    p = self.__curve.p()

    l = ((other.__y - self.__y) * \
         numbertheory.inverse_mod(other.__x - self.__x, p)) % p

    x3 = (l * l - self.__x - other.__x) % p
    y3 = (l * (self.__x - x3) - self.__y) % p

    return Point(self.__curve, x3, y3)

  def __mul__(self, other):
    def leftmost_bit(x):
      assert x > 0
      result = 1
      while result <= x:
        result = 2 * result
      return result // 2

    e = other
    if self.__order:
      e = e % self.__order
    if e == 0:
      return INFINITY
    if self == INFINITY:
      return INFINITY
    assert e > 0

    e3 = 3 * e
    negative_self = Point(self.__curve, self.__x, -self.__y, self.__order)
    i = leftmost_bit(e3) // 2
    result = self
    while i > 1:
      result = result.double()
      if (e3 & i) != 0 and (e & i) == 0:
        result = result + self
      if (e3 & i) == 0 and (e & i) != 0:
        result = result + negative_self
      i = i // 2

    return result

  def __rmul__(self, other):
    return self * other

  def __str__(self):
    if self == INFINITY:
      return "infinity"
    return "(%d,%d)" % (self.__x, self.__y)

  def double(self):
    if self == INFINITY:
      return INFINITY

    p = self.__curve.p()
    a = self.__curve.a()

    l = ((3 * self.__x * self.__x + a) * \
         numbertheory.inverse_mod(2 * self.__y, p)) % p

    x3 = (l * l - 2 * self.__x) % p
    y3 = (l * (self.__x - x3) - self.__y) % p

    return Point(self.__curve, x3, y3)

  def x(self):
    return self.__x

  def y(self):
    return self.__y

  def curve(self):
    return self.__curve

  def order(self):
    return self.__order

INFINITY = Point(None, None, None)