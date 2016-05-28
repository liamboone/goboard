import re
from flask import Flask, render_template
from gosvg import board_svg, gen_board
import subprocess as sp

application = Flask(__name__)

def make_board(board_size, history):
    moves = re.findall('(PASS)|([A-Z]+[0-9]+)', history.upper())
    moves = map(lambda (a,b): a if b == '' else b, moves)
    w, h, svg = gen_board(moves, int(board_size))

    return render_template('view.html', svg=svg)

application.add_url_rule('/<board_size>/<history>', 'hello', make_board)

if __name__ == "__main__":
    application.debug = True
    application.run()

