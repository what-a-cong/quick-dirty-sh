import nox


@nox.session
def lint(session):
    session.install("flake8")
    session.run("flake8", "qdsh.py")


@nox.session
def type(session):
    session.install("mypy")
    session.run("mypy", "qdsh.py")


@nox.session
def lit(session):
    session.install("lit")
    session.install("filecheck")
    session.run("lit", "test", "-v")


@nox.session(tags=["debug"])
def lit_debug(session):
    session.install("lit")
    session.install("filecheck")
    session.run("lit", "test", "-vv", "-a")
