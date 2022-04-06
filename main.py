from flask import Flask, render_template, request


app = Flask(__name__)

with open('words.txt') as f:
    data = f.read().split()


def valid_5_letter(s) -> bool:
    if all([c.isalnum() for c in s]):
        if len(s) == 5:
            return True
    return False


def valid_5_letter_satisfying(s, pos_d, no_chars) -> bool:
    if valid_5_letter(s):
        s = s.lower()
        for i, c in enumerate(s):
            if i in pos_d:
                if pos_d[i] != c:
                    return False
            else:
                if c in no_chars:
                    return False
        return True
    return False


def no_chars_valid(no_chars):
    return all([
        c in 'abcdefghijklmnopqrstuvwxyz'
        for c in no_chars
    ])


def pos_d_valid(pos_d):
    return all([
        (v in 'abcdefghijklmnopqrstuvwxyz') and (len(v) == 1)
        for v in pos_d.values()
    ])


@app.route('/', methods=['GET', 'POST'])
def index():
    hit_words = []
    if request.method == 'POST':
        no_chars = request.form['nocharacters'].lower()
        pos_d = {
            k - 1: request.form[f'pos{k}']
            for k in [1, 2, 3, 4, 5]
        }
        pos_d = {k: v for k, v in pos_d.items() if len(v) > 0}

        if pos_d_valid(pos_d) and no_chars_valid(no_chars):
            hit_words = list({
                s.lower()
                for s in data
                if valid_5_letter_satisfying(s, pos_d=pos_d, no_chars=no_chars)
            })
        else:
            hit_words = []
            if not pos_d_valid(pos_d):
                hit_words.append(f'Invalid pos_d: {pos_d}')
            if not no_chars_valid(no_chars):
                hit_words.append(f'Invalid no_chars: {no_chars}')

    res = {**request.form, 'hit_words': hit_words}
    return render_template('index.html', res=res)
