from flask import Flask, render_template, request

app = Flask(__name__)


with open('words.txt') as f:
    data = sorted(f.read().split())


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


@app.route('/', methods=['GET', 'POST'])
def index():
    A2Z = 'abcdefghijklmnopqrstuvwxyz'
    hit_words = []
    if request.method == 'POST':
        no_chars = [
            c for c in request.form['nocharacters'].lower()
            if c in A2Z
        ]
        pos_d = {}
        for k in [1, 2, 3, 4, 5]:
            v = request.form[f'pos{k}'].lower()
            if len(v) > 0 and v[0] in A2Z:
                pos_d[k - 1] = v[0]
        if len(no_chars) > 0 or len(pos_d) > 0:
            hit_words = sorted(list({
                s.lower()
                for s in data
                if valid_5_letter_satisfying(s, pos_d=pos_d, no_chars=no_chars)
            }))
        else:
            hit_words = ['You need to fill out something.']

    res = {**request.form, 'hit_words': hit_words}
    return render_template('index.html', res=res)
