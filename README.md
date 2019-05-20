# Notes

**Disclaimer** 

This is just a "toy project" that pretends to be a commandline note manager. Of course, you can do all of this with just vim... so feel free to disregard this repository!

--

This app facilitates the management of r-markdown notes by automating the compiling process, search, and sync with Google Drive. See the [usage section](## Usage) for more. 

## Setup

**Note**: This instructions assume you are using a debian-based OS. 

Clone this repository and run the following in the project base directory:

* Install dependencies and requirements:
    * `bash setup.sh`
    * `./venv/bin/python -m pip install -r requirements.txt`    
* Create your custom config by editing the `.env` file:
    * `vim .env`
* Create an alias in your shell-config.
    * Show the alias: `./venv/bin/python . alias`

## Usage

This is an opinionated note manage. This means that all the notes are required to be r-markdown compatible and will be "compiled" to PDF.

All note-related stuff are stored in a `.note` directory following: 

* `.note/pdf`: contains the pdf-version of the notes.
* `.note/src`: flatspace where all your notes live. 
* `.note/src/resources`: contains resources for your notes (e.g. png, jpg).
* `.note/src/resources/references.bib`: file containing all references. 

### Simple search

* `notes ls`

Lists all the available notes. 

* `notes find {pattern} [--similar]`

The `find` command lists all the notes that contains the `{pattern}` in their base-name. If the `--similar` flag is present, will perform a "similarity string search" using the default threshold of `0.5`. You can modify this default by defining `SIMILARITY_THRESHOLD` in the `.env`. 


### Editing/Creating notes

* `notes touch {name}`

You can create an empty note by using the `touch` command. Example: by running `notes touch example` a now note `example.rmd` will be created. 

* `notes vim {name}`

You can also create new notes or edit existing ones by running the `vim` command. If you want to open a specific note and raise an error if not exists, use `notes edit {name}`

* `notes vimall {name}`

This command opens `vim` with all notes in the buffer. The `name` parameter is optional. 

* `notes ranger`

You can explore the notes via the `ranger` commandline application. 

### View notes 

* `notes show {name}`

The `show` commands allows a quick view of a particular notes with `--command` default as `less`. 

* `notes view {name}`

The `view` command allows a pdf-view of the note using `--command` default as `gio open`. Note that the note will be compiled if the pdf does not exists. To manually re-compile a note use: `notes render {name} {title} {autor}` where the `{title}` arg can be inferred from the first line of the note and the `{author}` from the `.env` file. You can re-compile all notes in one step with this command: `notes renderall`


### Google Drive integration

to be defined. 

### Automatic Drive sync

to be defined. 

### Advanced search

to be defined. 

## Contriburing

to be defined. 

Consider using `black` for automated code-formatting:
* `pip install black`
* `black . --line-length 120 --exclude venv`

