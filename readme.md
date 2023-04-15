## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation
Before installing the project your system must have python and pip installed.

To install the project, run the following command:
1. Make virtual environment using `py3 -m venv venv`
2. Activate virtual environment using `Source venv/Scripts/activate`
3. Install the project dependencies using `pip install -r requirements.txt`


## Usage
1. Run imdb_movies_scrapping updating the database schemas and so your database is created
2. Now run the app using `uvicorn main:app --reload`