# -*- coding: utf-8 -*-
class Map(object):
  def __init__(self):
    self._character = dict()

  def render(self, screen):
    screen.fill('.')
    for coord, character in self._character.items():
      character.render(screen, coord)

  def put_character(self, character, pos):
    self._character[pos] = character

  def move_character(self, character, direction):
    (x, y) = self.coordinate_of_character(character)
    (dx, dy) = direction
    del self._character[(x, y)]
    self._character[(x + dx, y + dy)] = character

  def coordinate_of_character(self, target):
    for coord, character in self._character.items():
      if target == character: return coord
    return None

class Character(object):
  def __init__(self, glyph, color):
    self._glyph = glyph
    self._color = color

  def render(self, screen, coordinate):
    screen.put(self._glyph, coordinate, self._color)
