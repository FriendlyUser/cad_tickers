# content of conftest.py
import os

def pytest_configure(config):
    """
    Allows plugins and conftest files to perform initial configuration.
    This hook is called for every plugin and initial conftest
    file after command line options have been parsed.
    """


def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """


def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """


def try_and_delete(filePath):
    if os.path.exists(filePath):
        os.remove(filePath)

def pytest_unconfigure(config):
    """
    called before test process is exited.
    """
    try_and_delete('All.xlsx')
    try_and_delete('TSXV.xlsx')
    try_and_delete('All.xlsx')
    try_and_delete('cse.xlsx')
    try_and_delete('cse.pdf')