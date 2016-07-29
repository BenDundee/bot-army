import os

def get_path(f, ext=''):
    """ Get the full path given the extension.

    :param f: Filename. You may pass the variable __file__ in here, to get the location of the associated file.
    :type f: str
    :param ext: (relative) extension
    :type ext: str
    """
    loc = os.path.abspath(os.path.dirname(f))
    return os.path.join(loc, ext)
