


class safe_open:
    """Context manager for safely opening files.

    This context manager ensures that the directory containing the file exists

    Args:
        file_path (str): The path to the file to open.
        mode (str): The mode to open the file in. Default is 'r'.
        encoding (str): The encoding to use when opening the file. Default is 'utf-8'.
    """
    def __init__(self, file_path: str, mode: str = 'r', **kwargs):
        self.file_path = file_path
        self.mode = mode
        self.kwargs = kwargs or {}
        self.file = None

    def __enter__(self):
        import os
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        self.file = open(self.file_path, self.mode, **self.kwargs)
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()
        return False


class FileWriter:

    def __init__(self, file_path: str, mode: str = 'w', **kwargs):
        self.file_path = file_path
        self.mode = mode
        self.kwargs = kwargs or {}
        self.file = None

    def write(self, content: str|bytes):
        with safe_open(
            self.file_path,
            self.mode,
            **self.kwargs
        ) as f:
            f.write(content)