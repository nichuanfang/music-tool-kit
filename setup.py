from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = f.read()

setup(
    name='music-tool-kit', 
    version='0.2.9',
    description='A tool kit for music download and clip', 
    long_description_content_type='text/markdown', 
    long_description=readme,
    url='https://github.com/nichuanfang/music-tool-kit',   
    author='Nichuan Fang',
    author_email='f18326186224@gmail.com',
    license='MIT',
    platforms='any',
    keywords=[
        'mk'
        'mtk'
        'music',
        'musictool',
        'musicdownload',
        'musicclip',
        'musickit',
        'musictoolkit',
    ],
    packages=find_packages(exclude=['tests']),
    package_data={
        'mk': ['*.txt'],
    },
    require_python='>=3.8',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'mk = mk.__main__:main',
        ]
    },
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: Chinese (Simplified)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Utilities',
    ],
    zip_safe=False
)
