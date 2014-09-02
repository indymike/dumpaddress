from setuptools import setup

setup(
    name='getum',
    version='0.1',
    description='Command line tool for exctracting email addresses and urls from text files and links from html files.',
    author='Mike Seidle',
    author_email='mike@seidle.net',
    download_url='https://github.com/indymike/getum',
    py_modules=['getum'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        getum=getum:cli
    ''',
)
