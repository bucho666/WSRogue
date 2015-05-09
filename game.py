# -*- coding: utf-8 -*-
import random
from entity import Entity

class Map(object):
  def __init__(self, (w, h)):
    self._character = dict()
    self._cell = [[Terrain('.', 'silver') for x in range(w)] for y in range(h)]

  def render(self, screen):
    for y in range(len(self._cell)):
      for x, cell in enumerate(self._cell[y]):
        try:
          cell.render(screen, (x, y))
        except IndexError:
          pass
    for coord, character in self._character.items():
      character.render(screen, coord)

  def put_character(self, character, pos):
    self._character[pos] = character

  def put_terrain(self, terrain, (x, y)):
    self._cell[y][x] = terrain

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
    if coordinate in self._character: return False
    return self.walkable(coordinate)

  def walkable(self, (x, y)):
    return self._cell[y][x].walkable()

  def random_open_coordinate(self):
    opens = []
    w, h = self.size()
    for y in range(h):
      for x in range(w):
        if self.is_open((x, y)): opens.append((x, y))
    return random.choice(opens)

  def size(self):
    return len(self._cell[0]), len(self._cell)

class Character(Entity):
  def __init__(self, glyph, color, name='player'):
    Entity.__init__(self, glyph, color, name)

class Terrain(Character):
  def __init__(self, glyph, color, name='地形'):
    Entity.__init__(self, glyph, color, name)

  def walkable(self):
    return True

class Wall(Character):
  def __init__(self, glyph, color, name='壁'):
    Entity.__init__(self, glyph, color, name)

  def walkable(self):
    return False

class MapFile(object):
  _terrain = {
    '.': Terrain('.', 'silver', '床'),
    '#': Wall('#', 'silver', '壁'),
    'T': Wall('T', 'green',  '木'),
    '~': Wall('~', 'blue' ,  '湖'),
    '=': Terrain('=', 'olive' , '橋'),
  }

  @classmethod
  def load(cls, f):
    symbol_map = [line.rstrip() for line in f]
    (h, w) = len(symbol_map), len(symbol_map[0])
    m = Map((w, h))
    for y in range(h):
      for x, s in enumerate(symbol_map[y]):
        m.put_terrain(cls._terrain[s], (x, y))
    return m
