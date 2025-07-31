from setuptools import setup, find_packages

setup(
    name='Crypto Price Tracker',
    version='0.1.0',
    packages=find_packages(),
    install_requires=["requests"],
    entry_points={
        'console_scripts': [
            'crypto_price_tracker=cryptotracker.cli:main'
        ]
    },
    author='Oyebamiji Israel',
    author_email='israelbmj@gmail.com',
    description='CLI tool to fetch and analyze crypto prices',
    url='https://github.com/yourusername/crypto-price-tracker',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)