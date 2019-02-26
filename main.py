from flask import Flask, render_template, redirect, url_for, request
from models import Steam, SearchForm

from settings import secret_key

app = Flask(__name__)
steam = Steam()

app.config['SECRET_KEY'] = secret_key


@app.route('/', methods=['POST', 'GET'])
def index():
    form = SearchForm()

    if form.validate_on_submit():
        real_name = steam.check_game(form.name.data)
        if real_name is not None:
            return redirect(url_for('words', name=real_name),
                            code=307)  # POST request to check if the name comes from form.
        else:
            form.name.data = ''
            return render_template('search-error.html', form=form)

    if steam.failed:
        steam.failed = False
        form.name.data = ''
        return render_template('search-warning.html', form=form)
    else:
        return render_template('search.html', form=form)


@app.route('/<name>', methods=['POST', 'GET'])
def words(name):
    if request.method == 'GET':
        name = steam.check_game(name)
        if name is None:
            return redirect(url_for('index'))

    # The game reviews can be private depending of the game.
    try:
        return render_template('words.html', name=name, words=steam.get_words(name, number=18, ranges=3))
    except ValueError:
        steam.failed = True
        return redirect(url_for('index'))  # POST request to indicate that the request was unsuccessful.


@app.errorhandler(500)
def server_error():
    return redirect(url_for('index'))


@app.errorhandler(404)
def not_found(error):
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
