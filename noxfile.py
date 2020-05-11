import nox

FILE_PATHS = ["utils", "main.py"]

@nox.session
def format(session):
    session.install("black")
    session.run("black", *FILE_PATHS)
