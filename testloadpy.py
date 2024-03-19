import time
import threading
from ctypes import *
from contextlib import contextmanager
import io
import os
import sys
import tempfile


lib = CDLL("./libopenBrf.so")
c_stderr = c_void_p.in_dll(lib, 'stderr')


@contextmanager
def stderr_redirector(stream):
    # The original fd stderr points to. Usually 1 on POSIX systems.
    original_stderr_fd = sys.stderr.fileno()

    def _redirect_stderr(to_fd):
        """Redirect stderr to the given file descriptor."""
        # Flush the C-level buffer stderr
        lib.fflush(c_stderr)
        # Flush and close sys.stderr - also closes the file descriptor (fd)
        sys.stderr.close()
        # Make original_stderr_fd point to the same file as to_fd
        os.dup2(to_fd, original_stderr_fd)
        # Create a new sys.stderr that points to the redirected fd
        sys.stderr = io.TextIOWrapper(os.fdopen(original_stderr_fd, 'wb'))

    # Save a copy of the original stderr fd in saved_stderr_fd
    saved_stderr_fd = os.dup(original_stderr_fd)
    try:
        # Create a temporary file and redirect stderr to it
        tfile = tempfile.TemporaryFile(mode='w+b')
        _redirect_stderr(tfile.fileno())
        # Yield to caller, then redirect stderr back to the saved fd
        yield
        _redirect_stderr(saved_stderr_fd)
        # Copy contents of temporary file to the given stream
        tfile.flush()
        tfile.seek(0, io.SEEK_SET)
        stream.write(tfile.read())
    finally:
        tfile.close()
        os.close(saved_stderr_fd)


def main():
    f = io.BytesIO()
    with stderr_redirector(f):
        x = threading.Thread(target=start_lib, args=(lib,))
        x.start()

        modiferCode(lib)

    errorMessages = f.getvalue().decode('utf-8')
    #print('Got stderr: "{0}"'.format(errorMessages))


def start_lib(lib):
    args = (c_char_p * 1)()
    args[0] = b""
    lib.StartExternal(len(args), args)


def modiferCode(lib):
    time.sleep(5)

    lib.SetModPath(b"/home/djaessel/.steam/debian-installation/steamapps/common/MountBlade Warband/Modules/Native/")

    print("GET READY")

    time.sleep(5)
    res = lib.SelectItemByNameAndKind(b"club", 0)
    #print("RESULT:", res)

    time.sleep(5)
    res = lib.SelectItemByNameAndKind(b"sledgehammer", 0)
    #print("RESULT:", res)

    time.sleep(5)
    res = lib.SelectItemByNameAndKind(b"military_hammer", 0)
    #print("RESULT:", res)

    time.sleep(5)
    lib.CloseApp()

main()

