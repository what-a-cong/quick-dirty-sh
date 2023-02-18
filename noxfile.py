import nox


@nox.session
def flake8(session):
    session.install("flake8")
    session.run("flake8", "qdsh.py")


@nox.session
def lit(session):
    session.install("lit")
    session.install("filecheck")
    session.run("lit", "test", "-v")


@nox.session(tags=["debug", "manual"])
def lit_debug(session):
    session.install("lit")
    session.install("filecheck")
    session.run("lit", "test", "-vv", "-a")
