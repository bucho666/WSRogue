# -*- coding: utf-8 -*-
import random
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
    to = (x + dx, y + dy)
    if not self.is_open(to): return
    del self._character[(x, y)]
    self._character[to] = character

  def coordinate_of_character(self, target):
    for coord, character in self._character.items():
      if target == character: return coord
    return None

  def is_open(self, coordinate):
    return not coordinate in self._character

  def random_open_coordinate(self):
    opens = []
    for y in range(12):
      for x in range(32):
        if self.is_open((x, y)): opens.append((x, y))
    return random.choice(opens)

class Character(object):
  def __init__(self, glyph, color):
    self._glyph = glyph
    self._color = color

  def render(self, screen, coordinate):
    screen.put(self._glyph, coordinate, self._color)
