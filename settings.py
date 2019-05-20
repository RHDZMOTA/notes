import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)


# Read .env variables
AUTHOR = os.environ.get("AUTHOR", "default-author")
DEFAULT_TITLE = os.environ.get("DEFAULT_TITLE", "default-title")
VIRTUALENV_NAME = os.environ.get("VIRUTALENV_NAME", "venv")
PDF_OPEN_COMMAND = os.environ.get("PDF_OPEN_COMMAND", "gio open")
SHOW_COMMAND = os.environ.get("SHOW_COMMAND", "less")
GDRIVE_AUTO_RELOAD = os.environ.get("GDRIVE_AUTO_RELOAD", 100)
GDRIVE_BASE = os.environ.get("GDRIVE_BASE", "root")
GDRIVE_PDF = os.environ.get("GDRIVE_PDF", "root")
GDRIVE_SRC = os.environ.get("GDRIVE_SRC", "root")
GDRIVE_RESOURCES = os.environ.get("GDRIVE_RESOURCES", "root")
SIMILARITY_THRESHOLD = float(os.environ.get("SIMILARITY_THRESHOLD", "0.5"))

# Project environment variables
PATH_PROJECT = os.path.abspath(os.path.dirname(__file__))
PATH_NOTES = os.path.join(PATH_PROJECT, ".notes")
PATH_NOTES_SRC = os.path.join(PATH_NOTES, "src")
PATH_NOTES_PDF = os.path.join(PATH_NOTES, "pdf")
PATH_NOTES_RESOURCES = os.path.join(PATH_NOTES_SRC, "resources")
PATH_NOTES_RESOURCES_BIB = os.path.join(PATH_NOTES_RESOURCES, "references.bib")

GDRIVE_CLIENT_CONFIG = os.path.join(PATH_PROJECT, "client_secrets.json")
