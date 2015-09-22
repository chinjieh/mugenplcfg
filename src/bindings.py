#   Copyright (C) 2015 Chen Chin Jieh <chinjieh@gmail.com>
#   Copyright (C) 2015 Reto Buerki <reet@codelabs.ch>
#   Copyright (C) 2015 Adrian-Ken Rueegsegger <ken@codelabs.ch>
#
#   This file is part of mugenplcfg.
#
#   mugenplcfg is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   mugenplcfg is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with mugenplcfg.  If not, see <http://www.gnu.org/licenses/>.


# Module to handle generation of PyXB binding file
import os
import subprocess
import shutil
import customExceptions
import paths
import sys
sys.path.append(paths.PYXB)


def init(schemapath, bindingspath):
    # Create platformconfig.py PyXB binding module if it doesn't exist
    print "Checking for PyXB binding file..."
    BINDINGS_FOLDER = os.path.dirname(bindingspath)
    BINDINGS_NAME = os.path.splitext(os.path.basename(bindingspath))[0]

    if not bindingsExist(bindingspath):
        print "Bindings not found, generating binding file..."
        createBindings(schemapath,
                       BINDINGS_FOLDER,
                       BINDINGS_NAME,
                       paths.PYXB_GEN)
    else:
        print "Bindings found at: %s" % bindingspath


def copyEnvWithPythonPath():
    """
    Returns copy of current environment to use in subprocess, so that pyxbgen
    subprocess will inherit PYTHONPATH"""
    myenv = os.environ.copy()
    pathstr = ""
    for dir in sys.path:
        pathstr = pathstr + dir + ":"
    myenv["PYTHONPATH"] = pathstr
    return myenv


def bindingsExist(bindingfile):
    "Checks if PyXB bindings exist"
    if os.path.isfile(bindingfile):
        return True
    else:
        return False


def createBindings(schemafilepath, outpath, outname, pyxbgenpath):
    "Produces binding file from schema"
    with open(schemafilepath) as f:
        infile = f.name

    # Copy current environments including PYTHONPATH
    myenv = copyEnvWithPythonPath()
    success = False

    # Make output dir
    if not os.path.isdir(outpath):
        os.mkdir(outpath)

    print "Running PyXB 'pyxbgen' command..."
    try:
        proc = subprocess.check_call(
            [pyxbgenpath, "-u", infile, "-m",
             os.path.join(outpath, outname)], env=myenv)
    except subprocess.CalledProcessError:
        # Bad schema chosen.
        raise customExceptions.PyxbgenInvalidSchema(
            "Failed to generate bindings from file: %s" % infile)

    except OSError as e:
        if e.errno == os.errno.ENOENT:  # pyxb does not exist
            raise OSError(
                "'pyxbgen' script could not be found at: %s\n" % pyxbgenpath +
                "Failed to generate bindings.")
    else:
        print "Generated binding file to: %s" % os.path.join(outpath,
                                                             outname + ".py")

        # Set owner to user, not root (if run as root)
        parentdir = os.path.dirname(os.path.dirname(outpath))
        uid = os.stat(parentdir).st_uid  # Get user id of parent dir
        gid = os.stat(parentdir).st_gid  # Get group id of parent dir
        os.chown(os.path.join(outpath, outname + ".py"), uid, gid)
        os.chown(outpath, uid, gid)
        success = True

    return success
