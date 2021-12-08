class SheetSource():
    def __init__(self, path: str = None, filename: str = None, extension: str = None) -> None:
        self.path = path
        self.filename = filename
        self.extension = extension

class Sheet():
    def __init__(self, headers: list = None, data: dict = None) -> None:
        self.headers = headers
        self.data = data