#!/usr/bin/env python
# by: farsheed ashouri
# rodmena@me.com
#latest version: 
#git clone https://github.com/ourway/Maya_plugin_compiler.git
'''
Usage:
./mcompiler.py <myplugin.cpp>
'''
_version = '0.1.1'

import re
import os
from subprocess import Popen, PIPE, call  # everything nedded to handle external commands
import threading
import sys

compiler = 'g++'
CFLAGS   = '-m64 -O3 -pthread -pipe -D_BOOL -DLINUX_64 -DREQUIRE_IOSTREAM -fPIC -DLINUX -D_BOOL -DBits64_'
CPPFLAGS = '%s -Wno-deprecated -fno-gnu-keywords' % CFLAGS
LD = '%s %s -Wl,-Bsymbolic -shared' % (compiler, CPPFLAGS)
ml = os.getenv('MAYA_LOCATION')
INCLUDES  = '-I. -I%s/include' % ml
LIBS = '-L%s/lib' % ml


def quote_command(cmd):
    '''Fix windows commands'''
    if not (os.name == "nt" or os.name == "dos"):
        return cmd # the escaping is required only on Windows platforms, in fact it will break cmd line on others
    re_quoted_items = re.compile(r'" \s* [^"\s] [^"]* \"', re.VERBOSE)
    woqi = re_quoted_items.sub('', cmd)
    if len(cmd) == 0 or (len(woqi) > 0 and not (woqi[0] == '"' and woqi[-1] == '"')):
        return '"' + cmd + '"'   
    else:
        return cmd


def process(execfn):
    '''General external process'''
    cmd = quote_command(execfn)  #preventing windows base errors
    p = Popen(cmd, shell=True, env=os.environ, stderr=PIPE, stdout=PIPE,\
            universal_newlines=True)  # process
    (stdout, stderr) = p.communicate()
    return (stdout, stderr)

def compile(path):
    bname = os.path.basename(path)
    
    ext = bname.split('.')[-1]
    #print ext
    oname = bname.replace(ext, 'o')
    pname = bname.replace(ext, 'so')
    os.chdir(os.path.dirname(path))
    ocmd = '%s -c %s %s %s' % (compiler,INCLUDES, CPPFLAGS, path)
    (output, err) = process(ocmd)
    if err:
        print err
        return
    files = os.listdir('.')
    ofile = [i for i in files if bname.replace(ext, 'o') in i]
    if ofile:
        ofile = os.path.abspath(ofile[0])
    cmd = '%s -o %s %s %s -lOpenMaya -lOpenMayaUI -lOpenMayaAnim -lFoundation' % (LD, pname, ofile, LIBS)
    (output, err) = process(cmd)
    if not err:
        print '***********'
        print '*Compiled.*'
        print '***********'
        return
    else:
        print err
        return

    
    
    

if __name__ == '__main__':
    if len(sys.argv)<2:
        print ('Please give me an input cpp file')
    else:
        path = os.path.abspath(sys.argv[1])
        compile(path)
