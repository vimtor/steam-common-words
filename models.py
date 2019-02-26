import json
import pickle
import re
import requests
import random

from collections import Counter

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class Steam:
    """
    Main class that will make all the requests to the Steam API
    and parse its responses into meaningful information (Words).

    """

    def __init__(self):
        """ Initializes all the parameters and loads the files into variables. """
        self.failed = False

        # API endpoints for further usage.
        self.url = 'http://store.steampowered.com/appreviews/{}?json=1'
        self.all_games_url = 'http://api.steampowered.com/ISteamApps/GetAppList/v0002/'
        self.parameters = {'filter': 'all', 'pucharse_type': 'steam', 'num_per_page': 100, 'start_offset': 0}

        # Directories for the fetched data.
        self.games_dir = 'static/data/game_list.data'
        self.game_names_dir = 'static/data/game_names.json'

        # Initialize the games list with the file content.
        self.games = pickle.load(open(self.games_dir, 'rb'))
        self.game_names = json.load(open(self.game_names_dir, 'r'))

    def download_games(self):
        """ Downloads all the steam games data and dumps it to files. """
        downloaded_games = requests.get(self.all_games_url).json()['applist']['apps']

        pickle.dump(downloaded_games, open(self.games_dir, 'wb'))
        json.dump([game['name'] for game in downloaded_games], open(self.game_names_dir, 'w'))

    def get_reviews(self, name, number=1):
        """
        Returns the reviews of the specified game.

        Attributes
            name (str): Name of the game to get reviews from.
            number (int): Number of reviews to request. (Each request is 100 times the number requested).

        Returns
            str: A whole string with all the reviews concatenated.

        Raises
            ValueError: If the reviews for the specified game cannot be reached.
        """
        reviews = []

        appid = next(game['appid'] for game in self.games if game['name'].lower() == name.lower())

        for i in range(number):
            # Get the reviews.
            file = requests.get(self.url.format(appid), params=self.parameters)
            file_json = file.json()

            # Check if the reviews can be access.
            if file_json['success'] != 1:
                raise ValueError('Cannot access this game.')

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

    def get_words(self, name, number, ranges=3):
        """
        Returns the most common words found.

        Parameters
            name (str): Name of the game to get reviews from.
            number (int):  How many words the function should return.
            ranges (int): How many different types of popularity a word could be.

        Returns
            list(Word): List of Word objects which have the text and the popularity as class attributes.

        Raises
            ValueError: If the reviews for the specified game cannot be reached.

        """
        reviews = self.get_reviews(name, 5)

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

    def check_game(self, name):
        """
        Checks if the inputted game exists.

        Parameters
            name(str): The name to find.

        Returns
            The name of the found game or None if it was not found.

        """
        for game in self.game_names:
            if name.lower() == game.lower():
                return game

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


class SearchForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
