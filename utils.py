from models import Steam, Analyzer, SearchForm

steam = Steam()
analyzer = Analyzer()


def get_words(name, number=5):
    reviews = steam.get_reviews(name)
    return analyzer.get_words(reviews, number=number)


def download_games():
    steam.download_games()


def create_form():
    form = SearchForm()
    return form


def check_game(name):
    for game in steam.game_names:
        if name == game:
            return True

    return False
