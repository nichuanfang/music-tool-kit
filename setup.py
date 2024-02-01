from setuptools import setup, find_packages
with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = f.read()

setup(
    name='music-tool-kit',
    version='1.3.4',
    description='A tool kit for music download and clip',
    long_description_content_type='text/markdown',
    long_description=readme,
    url='https://github.com/nichuanfang/music-tool-kit',

    project_urls={
        'Source Code': 'https://github.com/nichuanfang/music-tool-kit',
        'Bug Tracker': 'https://github.com/nichuanfang/music-tool-kit/issues',
        'Documentation': 'https://blog.jaychou.site/2023/12/02/music-tool-kit%E5%B7%A5%E5%85%B7/',
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
    python_requires='>=3.11',
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
