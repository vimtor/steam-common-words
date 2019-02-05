import json
import pickle
import re
import nltk
import requests

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
        """
        Returns 100 times number of reviews for the specified appid.
        """
        reviews = []

        # TODO: get_name method won't be necessary when the name passed is correct.
        appid = self.get_appid(self.get_name(name))

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
            return next(game['appid'] for game in self.games if game['name'] == name)
        except StopIteration:
            # If not found, return None.
            return None


class Analyzer:

    def get_words(self, reviews, number=5):
        """ Returns the most common words found in 'reviews' until the 'number' paramater. """
        tokens = self.get_tokens(reviews)
        text = nltk.Text(tokens)

        fdist = nltk.FreqDist(text)
        return [word[0] for word in fdist.most_common()][:number]

    def get_tokens(self, reviews):
        """ Returns tokenized and cleaned reviews. """
        # Remove punctuation and special characters.
        cleaned_reviews = re.sub(r'[^\w\s]', '', reviews).lower()

        # Tokenize reviews into a list of words.
        word_list = nltk.tokenize.word_tokenize(cleaned_reviews)
        stopwords = json.load(open('static/data/stopwords.json', 'r'))

        return [word for word in word_list if word not in stopwords]


class SearchForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
