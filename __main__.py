import fire
import settings
import manage
import os


class Notes(object):
    class References(object):
        def __init__(self, created_at=None):
            self.created_at = created_at if created_at else manage.now()

        @manage.timeit
        def edit(self):
            return os.system(f"vim {settings.PATH_NOTES_RESOURCES_BIB}")

        @manage.timeit
        def show(self, list_format=False):
            pass

        @manage.timeit
        def add_book(self, alias, title, author, year, publisher):
            pass

        @manage.timeit
        def add_article(self, alias, title, author, journal, volume, year):
            pass

        @manage.timeit
        def add_online(self, alias, title, year, organization, author, url):
            pass

        def add_youtube(self, alias, title, year, organization, author, url):
            return self.add_online(alias, title, year, organization, author, url)

    class Drive(object):
        class Worker(object):
            def __init__(self, created_at=None):
                self.created_at = created_at if created_at else manage.now()
                self.started = False

            def status(self):
                pass

            def start(self):
                # TODO: Async drive worker
                return "GDrive worker started!"

        def __init__(self, created_at=None):
            self.created_at = created_at if created_at else manage.now()
            self.worker = self.Worker(self.created_at)

        @manage.timeit
        @manage.lazy_drive_wrapper
        def ls(self, drive_wrapper, prefix=""):
            notes = drive_wrapper.ls(settings.GDRIVE_SRC, lambda elem: elem["title"].startswith(prefix))
            return [note["title"] for note in notes if note["title"] != "resources"]

        @manage.timeit
        @manage.lazy_drive_wrapper
        def download(self, name, drive_wrapper, folder_id=settings.GDRIVE_SRC):
            title = manage.standardize(name)
            print(f"[INFO] Downloading content for: {title}")
            content = drive_wrapper.get_content_string(title, folder_id=folder_id)
            print(f"[INFO] Writing into local disk...")
            manage.set_note_content(note_name=title, content=content)
            print("[INFO] Done.")

        @manage.timeit
        @manage.lazy_drive_wrapper
        def upload_note(self, name, drive_wrapper, folder_id=settings.GDRIVE_SRC):
            content = manage.get_note_content(name)
            title = manage.standardize(name)
            drive_wrapper.update_or_create(title=title, content=content, parent_id=folder_id)
            print(f"[INFO] Uploaded note: {title}")

        @manage.timeit
        @manage.lazy_drive_wrapper
        def sync(self, name, drive_wrapper, folder_id=settings.GDRIVE_SRC):
            print(f"[INFO][{name}] Sync request.")
            last_mod_drive = drive_wrapper.get_last_modified(title=name, folder_id=folder_id)
            last_mod_local = manage.get_last_modified(name, raise_error=False)
            drive_diff = last_mod_drive - last_mod_local
            if drive_diff > 0:
                print(f"[INFO][{name}] Overwriting from Google Drive.")
                content = drive_wrapper.get_content_string(name, folder_id=folder_id)
                manage.set_note_content(note_name=name, content=content)
            elif drive_diff < 0:
                print(f"[INFO][{name}] Uploading and replacing in Google Drive.")
                file_path = manage.infer_abs_path(name)
                drive_wrapper.update_or_create_content_file(file_path, folder_id)
                # content = manage.get_file_content_and_infer_path(name)
                # drive_wrapper.update_or_create(title=name, content=content, parent_id=folder_id)

            else:
                print(f"[WARN][{name}] Ignoring: File not found in local not drive.")

        @manage.timeit
        def syncall(self, exclude_dirs="", exclude_files=""):
            def inner(pattern, elements, drive_folder):
                if pattern in exclude_dirs:
                    return None
                [self.sync(name=elem, folder_id=drive_folder) for elem in elements if elem not in exclude_files]

            inner("note", manage.get_notes(), settings.GDRIVE_SRC)
            inner("pdf", manage.get_pdfs(), settings.GDRIVE_PDF)
            inner("resources", manage.get_resources(), settings.GDRIVE_RESOURCES)

    class Services(object):
        def __init__(self, created_at=None):
            self.created_at = created_at if created_at else manage.now()

        def start(self, detached=True):
            # TODO: docker-compose up
            pass

        def down(self):
            # TODO: docker-compose down
            pass

        def ps(self):
            return os.system("docker ps")

    def __init__(self):
        now = manage.now()
        self.created_at = now
        self.name = settings.AUTHOR
        self.refs = self.References(created_at=now)
        self.drive = self.Drive(created_at=now)
        self.services = self.Services(created_at=now)

    @manage.timeit
    def hello(self):
        return f"Hello, {self.name}!"

    @manage.timeit
    def run(self, command):
        return os.system(command)

    @manage.timeit
    def length(self, name):
        return manage.show_note_length(name)

    @manage.timeit
    def size(self, name):
        return manage.show_note_size(name)

    @manage.timeit
    def shell(self):
        ipython_command = f"{os.path.join(settings.PATH_PROJECT, settings.VIRTUALENV_NAME, 'bin/ipython')}"
        shell_script = f"{os.path.join(settings.PATH_PROJECT, 'shell.py')}"
        return os.system(f"{ipython_command} -i {shell_script}")

    def alias(self):
        python_path = f"{os.path.join(settings.PATH_PROJECT, settings.VIRTUALENV_NAME, 'bin/python')}"
        return f"""alias notes="{python_path} {settings.PATH_PROJECT}" """

    @manage.timeit
    def ls(self, prefix=""):
        return manage.list_notes(prefix)

    @manage.timeit
    def touch(self, name):
        return manage.touch(note_name=name)

    @manage.timeit
    def ranger(self):
        return manage.open_ranger(path=settings.PATH_NOTES_SRC)

    @manage.timeit
    def vim(self, name, raise_error=False):
        return manage.open_vim(note_name=name, raise_error=raise_error)

    @manage.timeit
    def vimall(self, name=""):
        return manage.open_vim_all(name)

    def edit(self, name):
        self.vim(name=name, raise_error=True)

    @manage.timeit
    def view(self, name, command="gio open", compile=False):
        return manage.open_pdf(note_name=name, pdf_open_command=command, compile=compile)

    @manage.timeit
    def show(self, name, command="less"):
        return manage.show(note_name=name, show_command=command)

    @manage.timeit
    def last_modified(self, name, format=""):
        last_mod = manage.get_last_modified(name)
        if not format:
            return last_mod
        # TODO: format epoch
        last_mod_formatted = last_mod
        return last_mod_formatted

    @manage.timeit
    def find(self, pattern, similar=False):
        return manage.find(pattern=pattern, similar=similar)

    @manage.timeit
    def render(self, note, title=None, author=None):
        return manage.render(note_name=note, title=title, author=author if author else self.name)

    @manage.timeit
    def renderall(self, missing=False):
        if missing:
            return manage.render_missing_pdfs()
        return manage.render_all()


if __name__ == "__main__":
    fire.Fire(Notes)
