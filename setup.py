from setuptools import setup

setup(
    name='getum',
    version='0.1',
    py_modules=['getum'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        getum=getum:cli
    ''',
)
