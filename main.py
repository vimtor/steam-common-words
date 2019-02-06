from flask import Flask, render_template, redirect, url_for, request
from utils import get_words, create_form, check_game

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Albaricoque'


@app.route('/', methods=['POST', 'GET'])
def index():
    form = create_form()

    if form.validate_on_submit():
        real_name = check_game(form.name.data)
        if real_name is not None:
            return redirect(url_for('words', name=real_name),
                            code=307)  # POST request to check if the name comes from form.
        else:
            form.name.data = ''
            return render_template('search-error.html', form=form)

    return render_template('search.html', form=form)


@app.route('/<name>', methods=['POST', 'GET'])
def words(name):
    if request.method == 'GET':
        name = check_game(name)
        if name is None:
            return redirect(url_for('index'))

    return render_template('words.html', name=name, words=get_words(name, number=10, ranges=3))


@app.errorhandler(500)
def server_error():
    return redirect(url_for('index'))


@app.errorhandler(404)
def not_found(error):
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
