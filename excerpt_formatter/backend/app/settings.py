import os
from distutils.util import strtobool
from pathlib import Path

PACKAGE_NAME = "excerpt-formatter"

try:
    IS_PRODUCTION = bool(strtobool(os.getenv("IS_PRODUCTION")))
except (ValueError, AttributeError):
    IS_PRODUCTION = True

# Find project root path
if IS_PRODUCTION:
    PROJECT_ROOT = Path("/app")
    APP_DIR = PROJECT_ROOT
    FRONTEND_DIR = PROJECT_ROOT.joinpath("frontend")
else:
    path = Path.cwd()
    while path.name != PACKAGE_NAME:
        path = path.parent
    PROJECT_ROOT = path
    PY_PACKAGE_NAME = PACKAGE_NAME.replace("-", "_")
    APP_DIR = PROJECT_ROOT.joinpath(f"{PY_PACKAGE_NAME}/backend/app")
    FRONTEND_DIR = PROJECT_ROOT.joinpath(f"{PY_PACKAGE_NAME}/frontend")
