class Error(Exception):
    """
    Base class for exceptions in this module.
    """
    def __init__(self, message):
        """
        Constructor
        """
        self.message = message

    def to_dict(self):
        """
        Convert the error to a dictionary
        """
        return {"error": self.message}