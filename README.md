# biggestContributor
Who are the biggest contributers on your reddit sub? Check it out [here](
https://bigcontrib.torrtle.co/).

### Description
This is a Flask app that uses the PRAW library in order to get information about subreddits.

### Contributing
How to run this app.

1. Clone the repository.
2. CD into the repository.
3. Using your Python3 installation, create a virtual environment and activate it.
```Bash
$ python3 -m venv env
$ source env/bin/activate
```
4. Create a `.env` file in the repo folder and add the following environment variables.
```Bash
CLIENT_ID=<reddit web app client id>
CLIENT_SECRET=<reddit web app client secret>
```
5. Install the dependencies.
```Bash
$ pip install -r requirements.txt
```
6. Run `main.py`
```Bash
$ python main.py
```
