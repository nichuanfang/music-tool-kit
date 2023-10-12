from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = f.read()

setup(
    name='music-tool-kit', 
    version='0.3.9',
    description='A tool kit for music download and clip', 
    long_description_content_type='text/markdown', 
    long_description=readme,
    url='https://github.com/nichuanfang/music-tool-kit',   
    project_urls={
        'Source Code': 'https://github.com/nichuanfang/music-tool-kit',
        'Bug Tracker': 'https://github.com/nichuanfang/music-tool-kit/issues',
        'Documentation': 'https://github.com/nichuanfang/music-tool-kit#music-tool-kit-%E9%9F%B3%E4%B9%90%E5%B7%A5%E5%85%B7%E7%AE%B1',
    },
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
    require_python='>=3.11.0',
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
        'Programming Language :: Python :: 3.11',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Utilities',
    ],
    zip_safe=False
)
