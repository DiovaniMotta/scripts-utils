import os


class FileValidator:

    @staticmethod
    def allow_extension(path: str, extensions=None):
        if not os.path.isfile(path):
            raise Exception (f"File '{path}' does not exist.")
        if extensions:
            ext = os.path.splitext(path)[1].lower()
            if ext not in extensions:
                raise Exception (
                    f"Invalid extension '{ext}'. Extension allow: {', '.join(extensions)}"
                )
        return path