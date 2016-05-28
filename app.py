import re
from flask import Flask
#from gosvg import board_svg, board_png, gen_board
import subprocess as sp

application = Flask(__name__)

def make_board(board_size, history, fmt):
#     moves = re.findall('(PASS)|([A-Z]+[0-9]+)', history.upper())
#     moves = map(lambda (a,b): a if b == '' else b, moves)
#     w, h, svg = gen_board(moves, int(board_size))
# 
#     if fmt == 'png':
#         ratio = float(h)/float(w)
#         board_png(w, h, svg, "static/board.png")
#         return application.send_static_file('board.png')
# 
#     if fmt == 'gif':
#         sp.call('rm static/board*', shell=True)
#         N = len(moves)
# 
#         w, h, svg = gen_board(moves, int(board_size))
#         board_png(w, h, svg, "static/board_{:04}.png".format(N))
#         
#         for n in xrange(N):
#             w, h, svg = gen_board(moves[:n], int(board_size))
#             board_png(w, h, svg, "static/board_{:04}.png".format(n))
# 
#         sp.call('convert -delay 70 -loop 0 static/board_*.png static/board.gif', shell=True)
#         return application.send_static_file('board.gif')
# 
#         
#     if fmt == 'svg':
#         return str(svg)
# 
    return "Que?"

application.add_url_rule('/<board_size>/<history>.<fmt>', 'hello', make_board)

if __name__ == "__main__":
    application.debug = True
    application.run()

