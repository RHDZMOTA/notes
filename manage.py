import os
import settings

from difflib import SequenceMatcher
from datetime import datetime


def now():
    return datetime.now()


def timeit(function):
    def wrapper(self, *args, **kwargs):
        result = function(self, *args, **kwargs)
        diff = f"[timeit] Duration: {now() - self.created_at}"
        print(f"{result}\n{diff}" if result else diff)

    return wrapper


def lazy_drive_wrapper(function):
    def wrapper(*args, **kwargs):
        from drive import gdrive_wrapper

        return function(drive_wrapper=gdrive_wrapper, *args, **kwargs)

    return wrapper


def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


def similar_enough(a, b, threshold=settings.SIMILARITY_THRESHOLD):
    return similarity(a, b) > threshold


def standardize(note_name):
    note_name = note_name.strip().split("/")[-1]
    return note_name if note_name.lower().endswith(".rmd") else f"{note_name}.rmd"


def standardize_note_name_arg(function):
    def wrapper(note_name, *args, **kwargs):
        return function(note_name=standardize(note_name), *args, **kwargs)

    return wrapper


def get_files(path, ending="*"):
    files = os.listdir(path)
    if ending == "*":
        return files
    return [file for file in files if file.endswith(ending)]


def get_notes():
    return get_files(settings.PATH_NOTES_SRC, ending=".rmd")


def get_resources():
    return get_files(settings.PATH_NOTES_RESOURCES, ending="*")


def get_pdfs():
    return get_files(settings.PATH_NOTES_PDF, ending=".pdf")


def missing_pdfs():
    notes = {note.replace(".rmd", "") for note in get_notes()}
    pdfs = {pdf.replace(".pdf", "") for pdf in get_pdfs()}
    return list(notes.difference(pdfs))


@standardize_note_name_arg
def render(note_name, title=None, author=settings.AUTHOR, bib_path=settings.PATH_NOTES_RESOURCES_BIB):
    note_path = add_abs_path(note_name)
    pdf_path = get_pdf_path(note_name)
    title = title if title else infer_title(note_name)
    return os.system(
        f"""
    printf "rmarkdown::render('{note_path}', 
        output_format='pdf_document', 
        output_file='{pdf_path}',
        output_options=list(pandoc_args=c(
            '--metadata=title:\\"{title}\\"',
            '--metadata=author:\\"{author}\\"',
            '--metadata=bibliography:\\"{bib_path}\\"',
            '--metadata=urlcolor:blue',
            '--metadata=link-citations:true'
    )))" | R --vanilla --quiet
    """
    )


def render_missing_pdfs():
    for name in missing_pdfs():
        render(name)


def render_all():
    for note_name in get_notes():
        render(note_name)


@standardize_note_name_arg
def add_abs_path(note_name):
    return os.path.join(settings.PATH_NOTES_SRC, note_name)


@standardize_note_name_arg
def get_pdf_path(note_name):
    note_name = note_name.replace(".rmd", "")
    note_name = note_name if note_name.endswith(".pdf") else f"{note_name}.pdf"
    return os.path.join(settings.PATH_NOTES_PDF, note_name)


@standardize_note_name_arg
def pretty_print_single(note_name):
    note_info = f"- {note_name}"
    print(note_info)


def pretty_print_many(notes):
    for note in notes:
        pretty_print_single(note)


def get_file_content(file_path):
    with open(file_path, "r") as file:
        content = file.read()
    return content


@standardize_note_name_arg
def get_note_content(note_name):
    note_path = add_abs_path(note_name)
    return get_file_content(note_path)


@standardize_note_name_arg
def show_note_length(note_name):
    note_path = add_abs_path(note_name)
    return os.system(f"wc -l {note_path}")


@standardize_note_name_arg
def show_note_size(note_name):
    note_path = add_abs_path(note_name)
    return os.system(f"du -sh {note_path}")


def infer_abs_path(file_name):
    # TODO: change for 'if file in files'
    if file_name.lower().endswith(".rmd"):
        return os.path.join(settings.PATH_NOTES_SRC, file_name)
    elif file_name.lower().endswith(".pdf"):
        return os.path.join(settings.PATH_NOTES_PDF, file_name)
    else:
        return os.path.join(settings.PATH_NOTES_RESOURCES, file_name)


def get_file_content_and_infer_path(file_name):
    file_path = infer_abs_path(file_name)
    return get_file_content(file_path)


@standardize_note_name_arg
def set_note_content(note_name, content):
    note_path = add_abs_path(note_name)
    with open(note_path, "w") as file:
        file.write(content)


@standardize_note_name_arg
def infer_title(note_name, fallback=settings.DEFAULT_TITLE):
    content = get_note_content(note_name)
    for line in content.split("\n"):
        if line.startswith("#"):
            return line.replace("#", "").strip()
    return fallback


@standardize_note_name_arg
def get_words_in_name(note_name):
    return [
        word
        for word_by_underscore in note_name.replace(".rmd", "").split("_")
        for word_by_hyphen in word_by_underscore.split("-")
        for word in word_by_hyphen.split(" ")
    ]


def open_ranger(path):
    if not path:
        return os.system("ranger")
    return os.system(f"ranger {settings.PATH_NOTES_SRC}")


@standardize_note_name_arg
def open_vim(note_name, raise_error=False):
    note_path = add_abs_path(note_name)
    if note_name in get_notes():
        return os.system(f"vim {note_path}")
    elif raise_error:
        raise ValueError("Note not found: run 'notes ls' to see all the notes.")
    return os.system(f"vim {note_path}")


@standardize_note_name_arg
def open_vim_all(note_name=""):
    notes = get_notes()
    if note_name not in notes:
        return os.system(f"vim {os.path.join(settings.PATH_NOTES_SRC, '*')}")
    notes.remove(note_name)
    notes = [note_name] + notes
    return os.system(f"vim {' '.join([add_abs_path(note) for note in notes])}")


@standardize_note_name_arg
def touch(note_name):
    if note_name in get_notes():
        raise ValueError("Note already exists.")
    return os.system(f"touch {add_abs_path(note_name)}")


def get_last_modified_file(file_name, file_base_path, files=None, raise_error=False):
    files = os.listdir(file_base_path) if not files else files
    if file_name not in files:
        if raise_error:
            raise Exception(f"File {file_name} not found in {file_base_path}.")
        return -1
    file_path = os.path.join(file_base_path, file_name)
    last_modified = os.stat(file_path).st_mtime
    return last_modified


def get_last_modified_pdf(pdf_name, raise_error=False):
    return get_last_modified_file(pdf_name, settings.PATH_NOTES_PDF, get_pdfs(), raise_error)


def get_last_modified_resource(resource_name, raise_error=False):
    return get_last_modified_file(resource_name, settings.PATH_NOTES_RESOURCES, get_resources(), raise_error)


def get_last_modified_note(note_name, raise_error=False):
    return get_last_modified_file(note_name, settings.PATH_NOTES_SRC, get_notes(), raise_error)


def get_last_modified(name, raise_error=False):
    last_mod_all = [
        get_last_modified_note(name, raise_error),
        get_last_modified_pdf(name, raise_error),
        get_last_modified_resource(name, raise_error),
    ]
    for last_mod in last_mod_all:
        if last_mod > 0:
            return last_mod
    return -1


@standardize_note_name_arg
def open_pdf(note_name, pdf_open_command=settings.PDF_OPEN_COMMAND, compile=False):
    pdf_path = get_pdf_path(note_name)
    try:
        if compile:
            render(note_name=note_name)
        os.system(f"{pdf_open_command} {pdf_path}")
    except:
        render(note_name=note_name)
        open_pdf(note_name, pdf_open_comman=pdf_open_command)


@standardize_note_name_arg
def show(note_name, show_command=settings.SHOW_COMMAND):
    note_path = add_abs_path(note_name)
    os.system(f"{show_command} {note_path}")


def list_notes(prefix=""):
    pretty_print_many([note for note in get_notes() if note.startswith(prefix)])


def find(pattern, similar=False):
    notes = get_notes()
    if not similar:
        return pretty_print_many([note for note in notes if pattern in note])
    if " " not in pattern:
        return pretty_print_many([note for note in notes if similar_enough(note, pattern)])
    for note in notes:
        relevant_words = [
            word
            for word in get_words_in_name(note)
            for pattern_word in pattern.split(" ")
            if similar_enough(word, pattern_word)
        ]
        if relevant_words:
            pretty_print_single(note)
