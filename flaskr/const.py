import platform

LINUX = 'Linux'


def in_linux():
    if platform.system() == LINUX:
        return True
    else:
        return False
