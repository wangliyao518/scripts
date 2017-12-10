# -*- coding utf-8 -*-
"""
author: leo
"""
from random import choice
import time
import sys, os
import copy
import curses


class cell(object):

    def __init__(self, x_pos, y_pos):
        self.x, self.y, self.is_alive = x_pos, y_pos, False

    def __str__(self):
        return self.status

    def setStatus(self, status="."):
        if status == "*":
            self.is_alive = True
        elif status == ".":
            self.is_alive = False
        else:
            raise Exception("set status is invalid!")

    @property
    def status(self):
        if self.is_alive:
            return "*"
        else:
            return "."


class chessboard(object):
    def __init__(self, x_pos, y_pos):
        self._x_pos = x_pos
        self._y_pos = y_pos
        self._elements = [["." for y in range(self._y_pos)] for x in range(self._x_pos)]
        self._show_img = ""
        self._pad = curses.initscr()
        #self._pad = curses.newpad(x_pos, y_pos)

    def reset_elements_data(self, new_data):
        self._elements = new_data

    def draw_old(self):
        self._show_img = ""
        for x in xrange(self._x_pos):
            self._show_img += " -" * self._y_pos + "\n"
            for y in xrange(self._y_pos):
                self._show_img += "|" + "%s" % self._elements[x][y]
            self._show_img += "|\n"
        self._show_img += " -" * self._y_pos
        print (self._show_img)

    def draw(self):
        self._show_img = ""
        for x in xrange(self._x_pos):
            self._show_img += " -" * self._y_pos + "\n"
            for y in xrange(self._y_pos):
                self._show_img += "|" + "%s" % self._elements[x][y]
            self._show_img += "|\n"
        self._show_img += " -" * self._y_pos
        self._pad.addstr(0, 0, self._show_img)
        self._pad.refresh()


class Game(object):

    def __init__(self, x_pos, y_pos):
        self._row = x_pos
        self._column = y_pos
        self.chessboarder = chessboard(x_pos, y_pos)
        self.celler = [[cell(x, y) for y in range(self._column)] for x in range(self._row)]
        self._initial_chessboard()

    def _initial_chessboard(self):
        for x in range(self._row):
            for y in range(self._column):
                self.celler[x][y].setStatus(choice(('*', ".")))
        self.chessboarder.reset_elements_data(self.celler)
        pass

    def get_alive_neighbours(self, cell_obj, celler):
        alive_count = 0
        for x_offset in xrange(-1, 2):
            for y_offset in xrange(-1, 2):
                c_x, c_y = cell_obj.x + x_offset, cell_obj.y + y_offset
                if (c_x, c_y) == (cell_obj.x, cell_obj.y) or \
                        (c_x < 0 or c_x >= self._row) or \
                        (c_y < 0 or c_y >= self._column):
                    continue
                if celler[c_x][c_y].is_alive:
                    alive_count += 1
                #else:
                #    print '###',c_x, c_y, self.celler[c_x][c_y]
        return alive_count

    def specify_rule(self):
        celler_tmp = copy.deepcopy(self.celler)
        for x in range(self._row):
            for y in range(self._column):
                alive_neighbours_num = self.get_alive_neighbours(celler_tmp[x][y], celler_tmp)
                #print '##########', alive_neighbours_num, celler_tmp[x][y]
                if celler_tmp[x][y].status == "*" and alive_neighbours_num < 2:
                    self.celler[x][y].setStatus(".")
                if celler_tmp[x][y].status == "*" and alive_neighbours_num > 3:
                    self.celler[x][y].setStatus(".")
                if celler_tmp[x][y].status == "." and alive_neighbours_num == 3:
                    self.celler[x][y].setStatus("*")


    def start(self):
        for i in range(100):
            self.chessboarder.draw()
            self.specify_rule()
            time.sleep(0.1)

    def stop(self):
        pass


if __name__ == '__main__':
    gamer = Game(7, 8)
    gamer.start()
