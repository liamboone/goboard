import re
from flask import Flask, render_template, send_file
from gosvg import board_svg, gen_board
from cStringIO import StringIO

application = Flask(__name__)

def make_board(board_size, history):
    moves = re.findall('(PASS)|([A-Z]+[0-9]+)', history.upper())
    moves = map(lambda (a,b): a if b == '' else b, moves)
    w, h, svg = gen_board(moves, int(board_size))

    svg_io = StringIO()
    svg_io.write(str(svg))
    svg_io.seek(0)

    return send_file(svg_io, mimetype="image/svg+xml")

def index():
    return render_template('index.html')

application.add_url_rule('/<board_size>/<history>', 'board', make_board)
application.add_url_rule('/', 'index', index)

if __name__ == "__main__":
    application.debug = True
    application.run()

