from flask import Flask, render_template, redirect, url_for, session, flash
from utils import get_words, create_form, check_game, download_games

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Albaricoque'


@app.route('/', methods=['POST', 'GET'])
def index():
    form = create_form()

    if form.validate_on_submit():
        # Store the the name of the game on session.
        if check_game(form.name.data):
            return redirect(url_for('words', name=form.name.data))
        else:
            form.name.data = 'No existe ese juego'

    return render_template('index.html', form=form)


@app.route('/game/<name>', methods=['POST', 'GET'])
def words(name):
    return render_template('words.html', name=name, words=get_words(name, number=10))


@app.route('/<pagename>')
def default(pagename):
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
