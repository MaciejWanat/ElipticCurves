#! /usr/bin/env python3

from models import curve
from helpers.mathHelper import inverse_mod

class Point(object):
  def __init__(self, curve, x, y):
    self.__curve = curve
    self.__x = x
    self.__y = y

    if self.__curve:
      assert self.__curve.contains_point(x, y)

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
        inverse_mod(other.__x - self.__x, p)) % p

    x3 = (l * l - self.__x - other.__x) % p
    y3 = (l * (self.__x - x3) - self.__y) % p

    return Point(self.__curve, x3, y3)

  def __mul__(self, n, accumulator = False):
    if not accumulator:
      accumulator = self

    if n == 0:
        return INFINITY
    if n == 1:
        return accumulator
    if n % 2 == 1:
      return self.__mul__(n - 1, self.__add__(accumulator)) # addition when n is odd

    return self.__mul__(n/2, accumulator.double())          # doubling when n is even

  def __str__(self):
    if self == INFINITY:
      return "infinity"
    return "(%d, %d)" % (self.__x, self.__y)

  def __eq__(self, other):
    if self.x() == other.x() and self.y() == other.y():
      return True
    return False

  def double(self):
    if self == INFINITY:
      return INFINITY

    p = self.__curve.p()
    a = self.__curve.a()

    l = ((3 * self.__x * self.__x + a) * \
        inverse_mod(2 * self.__y, p)) % p

    x3 = (l * l - 2 * self.__x) % p
    y3 = (l * (self.__x - x3) - self.__y) % p

    return Point(self.__curve, x3, y3)

  def x(self):
    return self.__x

  def y(self):
    return self.__y

  def curve(self):
    return self.__curve

INFINITY = Point(None, None, None)