from models import Steam, Analyzer, SearchForm

steam = Steam()
analyzer = Analyzer()


def get_words(name, number, ranges):
    reviews = steam.get_reviews(name)
    return analyzer.get_words(reviews, number, ranges)


def download_games():
    steam.download_games()


def create_form():
    form = SearchForm()
    return form


def check_game(name):
    for game in steam.game_names:
        if name.lower() == game.lower():
            return True

    return False
