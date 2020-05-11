import nox

FILE_PATHS = ["utils", "main.py"]

@nox.session
def lint(session):
    session.run("pip", "install", "-r", "requirements.txt")
    session.install("black")
    session.install("flake8")
    session.run("black", "--check", *FILE_PATHS)
    session.run("flake8", *FILE_PATHS)

@nox.session
def format(session):
    session.install("black")
    session.run("black", *FILE_PATHS)
