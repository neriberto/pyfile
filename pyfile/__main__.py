from __future__ import absolute_import

import os
import sys

if __package__ == '':
    path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, path)

import pyfile

if __name__ == '__main__':
    sys.exit(pyfile.main())