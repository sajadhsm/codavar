import os
import shutil
import stat

def _rmtree_handleError(func, path, exc_info):
    print('Handling Error for file ' , path)
    print(exc_info)
    # Check if file access issue
    if not os.access(path, os.W_OK):
       # Try to change the permision of file
       os.chmod(path, stat.S_IWUSR)
       # call the calling function again
       func(path)

def remove_dir(path):
    shutil.rmtree(path, onerror=_rmtree_handleError)