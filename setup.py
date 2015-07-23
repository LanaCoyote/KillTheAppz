try:
    from setuptools import setup
except ImportError :
    from distutils.core import setup

config = {
    'description': 'Simple Twitter spambot blocker',
    'author': 'Lancey',
    'url': 'http://lancey.space',
    'download_url': 'http://lancey.space',
    'author_email': 'lancey@lancey.space',
    'version': '1.0',
    'install_requires': ['tweepy'],
    'packages': ['KillTheAppz'],
    'scripts': [],
    'name': 'KillTheAppz',
}

setup(**config)
