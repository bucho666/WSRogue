# -*- coding: utf-8 -*-
class Entity(object):
  def __init__(self, glyph, color, name):
    self._glyph = glyph
    self._color = color
    self._name = name

  def render(self, screen, coordinate):
    screen.put(self._glyph, coordinate, self._color)

  def name(self):
    return self._name
