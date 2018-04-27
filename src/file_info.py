class FileInfo():
    """This class saves the creation and expiration date of a file."""

    def __init__(self, file, creation_date, expiration_date):
        self.file = file
        self.creation_date = creation_date
        self.expiration_date = expiration_date
