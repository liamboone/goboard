import re
from functools import partial
from itertools import product

import goboard


class XMLElement (object):
    def __init__(self, obj_name, **attrs):
        attrs_text = ' '.join('{k}="{v}"'.format(k=k,v=v) for k,v in attrs.items())
        self.start_text = '<{obj} {attrs}>'.format(obj=obj_name,
                                                   attrs=attrs_text)
        self.end_text = '</{obj}>'.format(obj=obj_name)
        self.children = []

    def __str__(self):
        rep = (self.start_text +
               ''.join(map(str, self.children)) +
               self.end_text)
        return rep

    def add_children(self, children):
        self.children.extend(children)

    def add_child(self, child):
        self.children.append(child)

Circle = partial(XMLElement, 'circle')
Stone = partial(Circle, style='stroke-width:1;stroke:black')
Rect = partial(XMLElement, 'rect')
Text = partial(XMLElement, 'text')
Line = partial(XMLElement, 'line', style='stroke-width:1;stroke:black')
ThickLine = partial(XMLElement, 'line', style='stroke-width:3;stroke:black')
SVG = partial(XMLElement, 'svg', xmlns="http://www.w3.org/2000/svg")

def coord_to_tuple(coord):
    x = ord(coord[0])
    if x > ord('I'):
        x -= 1
    return (x-ord('A')+1, int(coord[1:]))

def gen_board(history, board_width):
    board = goboard.Board(board_width)

    for i, move in enumerate(history):
        if move.upper() != 'PASS':
            row, col = coord_to_tuple(move)
            board.play_move(i%2 + 1, row-1, col-1)
    
    if len(history) == 0 or move.upper() == 'PASS':
        last_move = None
    else:
        last_move = (i%2, coord_to_tuple(move.upper()))

    blacks = [(r+1, c+1) for r, c in board.get_player_stones(1)]
    whites = [(r+1, c+1) for r, c in board.get_player_stones(2)]

    black_captures = board.get_player_captures(1)
    white_captures = board.get_player_captures(2)
    
    extra_text = "Captures: Black {} | White {}".format(black_captures,
                                                        white_captures)

    return board_svg(board_width, 30, whites, blacks, last_move, extra_text)

def rank_to_file(rank):
    to_char = lambda x: 'ABCDEFGHJKLMNOPQRSTUVWXYZ'[x]
    d, m = divmod(rank, 25)
    if d > 0:
        return rank_to_file(d-1) + to_char(m)
    return to_char(m)

def board_svg(board_width, stone_width, white_stones, black_stones, last_move, extra_text):
    board_size = (board_width+1)*stone_width
    Hoshi = lambda x,y,**attrs: Circle(cx=stone_width*(x-1),
                                       cy=stone_width*(y-1),
                                       r=stone_width/8, fill='black', **attrs)
    Marker = lambda x,y,**attrs: Circle(cx=stone_width*(x-1),
                                        cy=stone_width*(y-1),
                                        r=stone_width/5, **attrs)
    Halo = lambda x,y,**attrs: Circle(cx=stone_width*(x-1),
                                      cy=stone_width*(y-1),
                                      r=stone_width/2, fill='white', 
                                      style='stroke-width:2;stroke:white', **attrs)
    BlackStone = lambda x,y,**attrs: Stone(cx=stone_width*(x-1),
                                           cy=stone_width*(y-1),
                                           r=stone_width/2-1, fill='black', **attrs)
    WhiteStone = lambda x,y,**attrs: Stone(cx=stone_width*(x-1),
                                           cy=stone_width*(y-1),
                                           r=stone_width/2-1, fill='white', **attrs)

    svg = SVG(width=board_size+20, height=board_size+50)
    board = Rect(width=board_size+20, height=board_size+50, 
                 style='fill:white')
    stones = SVG(x=stone_width/2+10, y=stone_width/2+10, overflow='visible',
                 viewBox="{0} {0} {1} {2}".format(-stone_width/2-1, board_size+20, board_size+50))
    grid = SVG(
               x=stone_width/2+10, y=stone_width/2+10, overflow='visible',
               viewBox="{0} {0} {1} {2}".format(-stone_width/2-1, board_size+20, board_size+50))
    
    letters = []
    lines = []
    for x in xrange(board_width):
        lines.append(Line(x1=0,                           y1=stone_width*x,
                          x2=stone_width*(board_width-1), y2=stone_width*x))
        lines.append(Line(y1=0,                           x1=stone_width*x,
                          y2=stone_width*(board_width-1), x2=stone_width*x))
        text = Text(x=5, y=stone_width*(x+1)+15)
        text.add_child(board_width-x)
        letters.append(text)
        text = Text(x=stone_width*(board_width+1), y=stone_width*(x+1)+15)
        text.add_child(board_width-x)
        letters.append(text)
        text = Text(x=stone_width*(x+1)+7, y=15)
        text.add_child(rank_to_file(x))
        letters.append(text)
        text = Text(x=stone_width*(x+1)+7, y=stone_width*(board_width+1)+15)
        text.add_child(rank_to_file(x))
        letters.append(text)

    lines.append(ThickLine(x1=-1,                            y1=0,
                           x2=stone_width*(board_width-1)+1, y2=0))
    lines.append(ThickLine(y1=-1,                            x1=0,
                           y2=stone_width*(board_width-1)+1, x2=0))
    lines.append(ThickLine(x1=-1,                            y1=stone_width*(board_width-1),
                           x2=stone_width*(board_width-1)+1, y2=stone_width*(board_width-1)))
    lines.append(ThickLine(y1=-1,                            x1=stone_width*(board_width-1),
                           y2=stone_width*(board_width-1)+1, x2=stone_width*(board_width-1)))

    grid.add_children(lines)

    hoshi = []
    if board_width >= 15:
        four = 4
        ten = (board_width+1)/2
        sixteen = board_width-3
        if board_width % 2 == 1:
            hoshi = product([four, ten, sixteen], [four, ten, sixteen])
        else:
            hoshi = product([four, sixteen], [four, sixteen])
    elif board_width >= 13:
        four = 4
        ten = (board_width+1)/2
        sixteen = board_width-3
        hoshi = list(product([four, sixteen], [four, sixteen]))
        if board_width % 2 == 1:
            hoshi.append((ten,ten))
    elif board_width >= 9:
        four = 3
        ten = (board_width+1)/2
        sixteen = board_width-2
        hoshi = list(product([four, sixteen], [four, sixteen]))
        if board_width % 2 == 1:
            hoshi.append((ten,ten))
    elif board_width % 2 == 1:
        ten = (board_width+1)/2
        hoshi = [(ten,ten)]
        
    hoshi = (Hoshi(x,y) for x,y in hoshi)
    grid.add_children(hoshi)

    halos = (Halo(x,board_width-y+1) for x,y in black_stones)
    stones.add_children(halos)
    halos = (Halo(x,board_width-y+1) for x,y in white_stones)
    stones.add_children(halos)

    black_stones = (BlackStone(x,board_width-y+1) for x,y in black_stones)
    white_stones = (WhiteStone(x,board_width-y+1) for x,y in white_stones)

    stones.add_children(black_stones)
    stones.add_children(white_stones)

    if last_move is not None:
        stones.add_child(Marker(last_move[1][0], board_width-last_move[1][1]+1, 
                                fill={0:'white', 1:'black'}[last_move[0]]))

    extra = Text(x=5, y=board_size+35)
    extra.add_child(extra_text)

    svg.add_children([board, grid, stones])
    svg.add_children(letters)
    svg.add_child(extra)
    return (board_size+20, board_size+50, svg)


if __name__ == '__main__':
    sample_hist = """
 C4    D16
 Q4    Q16
 R14   O17
 S16   R17
 R11   C10
 F3    C7
 B6    B7
 C6    D8
 L4    R8
 R7    Q7
 Q8    S7
 R6    S6
 Q6    S10
 R9    S8
xP7    S9
 T8    S11
 S12   R4
 S4    S5
 R5    T4
 S3    R10
 Q10  xQ9
 P9    Q11
 P10  xR12
xR9    S13
 Q13   Q12
 R3
"""

    sample_hist = sample_hist.replace('x', ' ')
    moves = re.findall('([A-Z]+[0-9]+)|(PASS)', sample_hist.upper())
    moves = map(lambda (a,b): a if b == '' else b, moves)
    w, h, svg = gen_board(moves, 19)
    print svg
    ratio = float(h)/float(w)
