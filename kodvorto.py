#!/usr/bin/env python3

from gi.repository import Rsvg
from gi.repository import Pango
from gi.repository import PangoCairo
import cairo
import math
import re
import collections

POINTS_PER_MM = 2.8346457

PAGE_WIDTH = 210
PAGE_HEIGHT = 297

N_COLUMNS = 3
N_ROWS = 6
CARDS_PER_PAGE = N_COLUMNS * N_ROWS

CARD_WIDTH = PAGE_WIDTH / N_COLUMNS
CARD_HEIGHT = PAGE_HEIGHT / N_ROWS

CURVE_SIZE = 3
INSET = 5

PUNCH_SIZE = 2
PUNCH_Y = INSET + PUNCH_SIZE * 1.5

MAIN_WORD_SIZE = 7
SMALL_WORD_SIZE = 5
SMALL_WORD_Y = PUNCH_Y + PUNCH_SIZE + SMALL_WORD_SIZE * 1.1

FACE = Rsvg.Handle.new_from_file('face.svg')

FACE_WIDTH = 15
FACE_HEIGHT = FACE_WIDTH * 2
FACE_X = CARD_WIDTH - INSET * 1.5 - FACE_WIDTH
FACE_Y = INSET * 1.5

def fit_image(cr, image, x, y, width, height):
    dim = image.get_dimensions()

    if (dim.width / dim.height > width / height):
        # scale to fit the width
        scale = width / dim.width
    else:
        # scale to fit the height
        scale = height / dim.height

    cr.save()

    cr.translate(x + width / 2 - dim.width * scale / 2,
                 y + height / 2 - dim.height * scale / 2)
    cr.scale(scale, scale)
    image.render_cairo(cr)

    cr.restore()

def start_page(cr):
    for i in range(N_COLUMNS - 1):
        cr.move_to((i + 1) * PAGE_WIDTH / N_COLUMNS, 0)
        cr.rel_line_to(0, PAGE_HEIGHT)
    for i in range(N_ROWS - 1):
        cr.move_to(0, (i + 1) * PAGE_HEIGHT / N_ROWS)
        cr.rel_line_to(PAGE_WIDTH, 0)

    cr.stroke()

def draw_card(cr, x, y, word):
    cr.move_to(x + INSET + CURVE_SIZE, y + INSET)
    cr.rel_line_to(CARD_WIDTH - (INSET + CURVE_SIZE) * 2, 0)
    cr.arc(x + CARD_WIDTH - INSET - CURVE_SIZE,
           y + INSET + CURVE_SIZE,
           CURVE_SIZE,
           3 * math.pi / 2.0,
           2 * math.pi)
    cr.arc(x + CARD_WIDTH - INSET - CURVE_SIZE,
           y + CARD_HEIGHT - INSET - CURVE_SIZE,
           CURVE_SIZE,
           0,
           math.pi / 2.0)
    cr.arc(x + INSET + CURVE_SIZE,
           y + CARD_HEIGHT - INSET - CURVE_SIZE,
           CURVE_SIZE,
           math.pi / 2.0,
           math.pi)
    cr.arc(x + INSET + CURVE_SIZE,
           y + INSET + CURVE_SIZE,
           CURVE_SIZE,
           math.pi,
           3 * math.pi / 2.0)

    cr.new_sub_path()
    cr.arc(x + CARD_WIDTH / 2.0,
           y + PUNCH_Y,
           PUNCH_SIZE,
           0,
           2 * math.pi)

    cr.stroke()

    fit_image(cr, FACE, x + FACE_X, y + FACE_Y, FACE_WIDTH, FACE_HEIGHT)
    cr.move_to(x + INSET * 1.3, y + SMALL_WORD_Y + SMALL_WORD_SIZE * 1.1)
    cr.rel_line_to(FACE_X - INSET * 1.6, 0)
    cr.stroke()

    cr.save()

    cr.set_font_size(MAIN_WORD_SIZE)
    width = cr.text_extents(word)[2]
    cr.move_to(x + CARD_WIDTH / 2 - width / 2,
               y + CARD_HEIGHT - MAIN_WORD_SIZE * 1.1)
    cr.show_text(word)

    cr.set_font_size(SMALL_WORD_SIZE)
    width = cr.text_extents(word)[2]
    cr.move_to(x + (FACE_X - INSET) / 2.0 + INSET,
               y + SMALL_WORD_Y)

    cr.translate(width / 2.0, 0)
    cr.rotate(math.pi)
    cr.translate(-width / 2.0, 0)
    cr.rel_move_to(-width / 2.0, 0)
    cr.show_text(word)

    cr.restore()

surface = cairo.PDFSurface("kodvortoj.pdf",
                           PAGE_WIDTH * POINTS_PER_MM,
                           PAGE_HEIGHT * POINTS_PER_MM)

cr = cairo.Context(surface)

# Use mm for the units from now on
cr.scale(POINTS_PER_MM, POINTS_PER_MM)

# Use ½mm line width
cr.set_line_width(0.5)

for i, word in enumerate(open('vortoj.txt', 'r')):
    word = word.rstrip()

    if i % CARDS_PER_PAGE == 0:
        start_page(cr)

    in_page = i % CARDS_PER_PAGE
    x = in_page % N_COLUMNS * CARD_WIDTH
    y = in_page // N_COLUMNS * CARD_HEIGHT
    draw_card(cr, x, y, word)

    if (i + 1) % CARDS_PER_PAGE == 0:
        cr.show_page()
