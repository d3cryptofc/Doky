import tomllib
from pathlib import Path


# Getting the project root path.
PROJECT_ROOT_PATH = Path(__file__).parent.parent

# Parsing the toml setup file.
with open(PROJECT_ROOT_PATH / 'pyproject.toml', 'rb') as file:
    project_setup = tomllib.load(file)['tool']['poetry']

# Getting project version.
VERSION = project_setup['version']

# Getting project description.
DESCRIPTION = project_setup['description']

# Getting project authors.
AUTHORS = project_setup['authors']

# Getting project repository URL.
REPOSITORY_URL = project_setup['repository']

# Getting project repository issues URL.
REPOSITORY_ISSUE_URL = REPOSITORY_URL + '/issues'
