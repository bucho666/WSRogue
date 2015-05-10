# -*- coding: utf-8 -*-
import random
from entity import Entity

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


class View(object):
  def __init__(self, character, on_map):
    self._character = character
    self._map = on_map
    self._size = (15, 9)

  def render(self, screen):
    (cx, cy) = self._map.coordinate_of_character(self._character)
    w, h = self._size
    ox, oy = cx - (w/2), cy - (h/2)
    for px, py in [(x + ox, y + oy) for y in range(h) for x in range(w)]:
      self._map.render_at((px, py), screen, (px - ox, py - oy))

class Map(object):
  dark = Terrain(' ', 'black')
  def __init__(self, (w, h)):
    self._character = dict()
    self._cell = [[Terrain('.', 'silver') for x in range(w)] for y in range(h)]

  def render(self, screen):
    for x, y in self.coordinates():
      self._cell[y][x].render(screen, (x, y))
    for coord, character in self._character.items():
      character.render(screen, coord)

  def render_at(self, coord, screen, to):
    (x, y) = coord
    if x < 0 or y < 0:
      self.dark.render(screen, to)
    else:
      try:
        self._cell[y][x].render(screen, to)
      except IndexError:
        self.dark.render(screen, to)
    if coord in self._character:
      self._character[coord].render(screen, to)

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
    opens = [c for c in self.coordinates() if self.is_open(c)]
    return random.choice(opens)

  def coordinates(self):
    w, h = self.size()
    return [(x, y) for y in range(h) for x in range(w)]

  def size(self):
    return len(self._cell[0]), len(self._cell)

class MapFile(object):
  _terrain = {
    '.': Terrain('.', 'silver', '床'),
    '=': Terrain('=', 'olive' , '橋'),
    '#': Wall('#', 'silver', '壁'),
    'T': Wall('T', 'green',  '木'),
    '~': Wall('~', 'blue' ,  '湖'),
  }

  @classmethod
  def load(cls, f):
    symbol_map = [line.rstrip() for line in f]
    (h, w) = len(symbol_map), len(symbol_map[0])
    m = Map((w, h))
    for (x, y) in m.coordinates():
      s = symbol_map[y][x]
      m.put_terrain(cls._terrain[s], (x, y))
    return m
