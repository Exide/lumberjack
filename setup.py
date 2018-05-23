import setuptools

with open('README.md') as f:
    long_description = f.read()

setuptools.setup(
    name='lumberjack',
    version='0.0.1',
    author='Ryan Zander',
    author_email='exide@hotmail.com',
    description='A logging package for Python.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Exide/lumberjack',
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
