class TodoError(Exception):
    pass

class InvalidTaskError(TodoError):
    pass

class StorageError(TodoError):
    pass
