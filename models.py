import json
import pickle
import re
from collections import Counter
import requests
import random

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class Steam:
    games = []
    game_names = []

    url = 'http://store.steampowered.com/appreviews/{}?json=1'
    parameters = {'filter': 'all', 'pucharse_type': 'steam',
                  'num_per_page': 100, 'start_offset': 0}

    all_games_url = 'http://api.steampowered.com/ISteamApps/GetAppList/v0002/'
    games_directory = 'static/data/gameslist.data'

    def __init__(self):
        # Initialize the games list with the file content.
        with open(self.games_directory, 'rb') as file:
            self.games = pickle.load(file)

        with open('static/data/gamenames.data', 'rb') as file:
            self.game_names = pickle.load(file)

    def download_games(self):
        downloaded_games = requests.get(self.all_games_url).json()['applist']['apps']

        with open(self.games_directory, 'wb') as file:
            pickle.dump(downloaded_games, file)

    def get_reviews(self, name, number=1):
        """ Returns 100 times number of reviews for the specified appid. """
        reviews = []

        # TODO: get_name method won't be necessary when the name passed is correct.
        appid = self.get_appid(name)

        for i in range(number):
            # Get the reviews.
            file = requests.get(self.url.format(appid), params=self.parameters)

            # Add the requested reviews.
            reviews += [review_properties['review'] for review_properties in file.json()['reviews']]

            # Offset start for the next iteration.
            self.parameters['start_offset'] = 100 * i

            # Check if there is not more reviews to get.
            if len(reviews) < self.parameters['start_offset']:
                break

        # Reset the offset for further requests.
        self.parameters['start_offset'] = 0

        return str(reviews)

    def get_name(self, name):
        """
        Returns a the first match of the game whose name matches the name parameter.
        """
        # For optimization in the list comprehension.
        name = name.lower()

        return next(game for game in self.game_names if name in game.lower())

    def get_appid(self, name):
        """ Returns the appid of the game whose names is equal to the name parameter. """
        # TODO: Try and catch won't be necessary because the name parameter will be validated.
        try:
            # Return the first match.
            return next(game['appid'] for game in self.games if game['name'].lower() == name.lower())
        except StopIteration:
            # If not found, return None.
            return None


class Word:
    """
    Container for popular words.

    Attributes
        text (str): Written word (in lowercase).
        popularity (int): Score of the word among the other ones analyzed.

    """

    def __init__(self, text, popularity):
        self.text = text
        self.popularity = popularity

    def __str__(self):
        return f"({self.text}, {self.popularity})"

    def __repr__(self):
        return self.__str__()


class Analyzer:

    def get_words(self, reviews, number, ranges=3):
        """
        Returns the most common words found.

        Parameters
            reviews (str): All the concatenated reviews in one single string.
            number (int):  How many words the function should return.
            ranges (int): How many different types of popularity a word could be.


        Returns
            list(Word): List of Word objects which have the text and the popularity as class attributes.

        """

        # Tokenize and remove punctuation.
        tokens = re.split(r'\W+', reviews)
        tokens = [token.lower() for token in tokens]

        # Remove stopwords.
        stopwords = json.load(open('static/data/stopwords.json', 'r'))
        tokens = [token for token in tokens if token not in stopwords]

        # Get the most common words and the intervals of popularity.
        words = Counter(tokens).most_common(number)
        _, max_score = words[0]
        step = max_score / ranges

        # Shuffle words to make the displaying less boring.
        random.shuffle(words)

        common_words = []
        for word, score in words:
            if score > step * 2:
                common_words.append(Word(word, 2))
            elif score > step * 1.35:
                common_words.append(Word(word, 1))
            else:
                common_words.append(Word(word, 0))

        return common_words


class SearchForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
