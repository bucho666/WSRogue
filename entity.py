# -*- coding: utf-8 -*-
class Entity(object):
  def __init__(self, glyph, color, name):
    self._graphic = Graphic(glyph, color)
    self._name = name

  def render(self, screen, coordinate):
    self._graphic.render(screen, coordinate)

  def name(self):
    return self._name

class Graphic(object):
  def __init__(self, glyph, color):
    self._glyph = glyph
    self._color = color

  def render(self, screen, coordinate):
    screen.put(self._glyph, coordinate, self._color)
