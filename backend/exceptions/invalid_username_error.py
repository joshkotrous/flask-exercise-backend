class InvalidUsernameError(Exception):
    def __init__(self, message="Username not found."):
        self.message = message
        super().__init__(self.message)
