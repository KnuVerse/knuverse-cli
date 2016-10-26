from setuptools import setup, find_packages

setup(
    name='knuverse-cli',
    version='1.0.4',
    description='Demo of the Knuverse SDK that lets you verify with AudioPIN and AudioPass',
    long_description=open('README.md').read(),
    url='https://github.com/KnuVerse/knuverse-cli',
    author='KnuVerse',
    author_email='support@knuverse.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='api sdk knuverse cloud voice authentication audiopin audiopass demo',

    install_requires=['knuverse==1.0.4', 'colorama', 'pyaudio'],
    packages=find_packages(exclude=['examples']),
    entry_points={
        'console_scripts': [
            'knuverse = cli.__main__:main'
        ]
    },
)