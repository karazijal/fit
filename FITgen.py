#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
'''
Script to generate boiler plate code for function interposition based on a file
containing definitions of functions to interpose and a pair of templates for
the files to be genreated based on this gathered information.
'''
__author__ = 'laurynaskarazija'

import sys
import os
import argparse
from subprocess import call

try:
    import yaml
except ImportError:
    print("Yaml module is not present")
    print("Please install the PyYaml module")
    sys.exit(1)
try:
    import jinja2
except ImportError:
    print("Jinja2 module is not present!")
    print("Please install the Jinja2 module.")
    sys.exit(1)


def get_testing_arguments(f):
    return_list = []
    if 'errinj' not in f['flags'] or f['name'].startswith('__'):
        return ['SKIP']
    for arg in f['args']:
        if isinstance(arg, str):
            return ['SKIP']
        if arg['type'] in ['int', 'size_t', 'ssize_t', 'uid_t', 'pid_t', 'gid_t', 'mode_t', 'off_t', 'off64_t',
                           'pos64_t', 'long']:
            return_list.append('4')
        elif '*' in arg['type']:
            return_list.append('NULL')
        else:
            print arg
    return return_list

def declare_static_variables_string(args):
    if isinstance(args, str):
        lst = args.replace('(', '').replace(')', '').replace('.', '').strip().split(',')
        lst = filter(lambda x: x!='' ,map(lambda x: x.strip(), lst))
        text =''
        for arg in lst:
            text+= 'static '+arg+"_rec="+(arg.split()[-1].replace('*',''))+';\n'
        return "/*00AA00:*/ {}".format(text)
    else:
        return "//Something else: 00EE00"

def assign_variables_string(args):
    if isinstance(args, str):
        lst = args.replace('(', '').replace(')', '').replace('.', '').strip().split(',')
        lst = filter(lambda x: x!='' ,map(lambda x: x.strip(), lst))
        text =''
        for arg in lst:
            text+= (arg.split()[-1].replace('*',''))+"_rec="+(arg.split()[-1].replace('*',''))+';\n'
        return "/*00AA00:*/ {}".format(text)
    else:
        return "//Something else: 00EE00"

def compare_variables_string(args):
    if isinstance(args, str):
        lst = args.replace('(', '').replace(')', '').replace('.', '').strip().split(',')
        lst = filter(lambda x: x!='' ,map(lambda x: x.strip(), lst))
        text =''
        for arg in lst:
            text+= (arg.split()[-1].replace('*',''))+"_rec=="+(arg.split()[-1].replace('*',''))+'&&\n'
        return "/*00AA00:*/ {}".format(text)
    else:
        return "//Something else: 00EE00"

def is_buffer(arg):
    return '*' in arg['type'] and 'ptr'==arg['name']

def with_size(func):
    for arg in func['args']:
        if arg['name']=='size' and arg['type']=='size_t':
            return True
    return False


def rebuild_func(funcs, skip=False, skipList=[], verbose=False, errPickMode=False):
    nfuncs = []
    topfuncs = []
    for func in funcs:
        if skip:
            if 'nogen' in func['flags']:
                if verbose:
                    print "SKIPPING " + str(func)
                continue
            elif 'void' == func['ret']:
                continue
            elif func['name'] in skipList:
                continue

        f = dict()
        f['name'] = func['name']
        f['ret'] = func['ret']

        f['flags'] = []
        for flg in func['flags']:
            # if flg=='nogen' or flg=='errinj' or flg=='nonauto' or flg=='log' or flg=='fdprotect' or flg=='shorted' or flg=='vararg':
            if flg in ['nogen', 'errinj', 'nonauto', 'log', 'fdprotect', 'shorted', 'vararg', 'placeontop', 'dir',
                       'open']:
                f['flags'].append(flg)
            if 'input' in flg or 'output' in flg:
                f['flags'].append(flg)
        f['args'] = []
        FILE_based = False
        if isinstance(func['args'], str):
            f['args'] = func['args']
        else:
            for arg in func['args']:
                newarg = {}
                newarg['name'] = arg['name']
                newarg['type'] = arg['type']
                if 'dims' in arg:
                    newarg['type'] = newarg['type'] + ' *'
                f['args'].append(newarg)
                if newarg['type'] == 'FILE *':
                    FILE_based = True
        if 'log' in f['flags'] and FILE_based:
            f['flags'].append('file')

        if 'fdprotect' in func['flags']:
            f['fd_protect'] = func['fd_protect']

        if 'vararg' in func['flags']:
            f['real_func'] = func['real_func']
        elif 'shorted' in func['flags']:
            f['real_call'] = func['real_call']

        if 'err_ret' in func:
            f['err_ret'] = func['err_ret']
        else:
            if '*' in func['ret']:
                f['err_ret'] = 'NULL'
            else:
                f['err_ret'] = '-1'
        if 'errs' in func:
            s = set(func['errs'])
            f['errs'] = list(s)
        else:
            f['errs'] = []
        f['errline'] = pickErrno(f['errs'], errPickMode, verbose)
        f['test_call_args'] = get_testing_arguments(f)
        if errPickMode and f['errline'] is None and 'errinj' in f['flags']:
            continue

        # print f
        if 'placeontop' in func["flags"]:
            topfuncs.append(f)
        else:
            nfuncs.append(f)
    nfuncs = topfuncs + nfuncs
    return nfuncs


def pp_yaml(funcs, file):
    for func in funcs:
        file.write('- name: {}\n'.format(func['name']))
        file.write('  ret: "{}"\n'.format(func['ret']))
        file.write('  flags: {}\n'.format(str(func['flags'])))

        if 'vararg' in func['flags']:
            file.write('  real_func: "{}"\n'.format(func['real_func']))
        if 'shorted' in func['flags']:
            file.write('  real_call: "{}"\n'.format(func['real_call']))
        if 'fdprotect' in func['flags']:
            file.write('  fd_protect:\n')
            file.write('    arg: "{}"\n'.format(func['fd_protect']['arg']))
            file.write('    errno: "{}"\n'.format(func['fd_protect']['errno']))
        file.write('  args:')
        if isinstance(func['args'], str):
            file.write(' "{}"\n'.format(func['args']))
        else:
            file.write('\n')
            for arg in func['args']:
                file.write('    - name: {}\n'.format(arg['name']))
                file.write('      type: "{}"\n'.format(arg['type']))
        file.write('  errs: {}\n'.format(str(func['errs'])))
        file.write('  err_ret: "{}"\n'.format(str(func['err_ret'])))
        file.write('  errline: "{}"\n'.format(str(func['errline'])))
        file.write('  testline: "{}"\n'.format(str(func['test_call_args'])))
        file.write('\n')


def exclusive_fgets(name):
    return str(name) == "fgets_unlocked"


def is_unlocked(name):
    return '_unlocked' in str(name)


def is_nb(name):
    return str(name) == 'nb'


def pickErrno(errList, errPickMode, verbose=False):
    if len(errList) is 0:
        if errPickMode:
            return None
        return "//This function does not cause errors: Issue Code: 00FF03"
    elif 'EAGAIN' in errList:
        return 'errno = EAGAIN;'
    elif 'EINTR' in errList:
        return 'errno = EINTR;'
    elif 'EIO' in errList:
        return 'errno = EIO;'
    elif 'EWOULDBLOCK' in errList:
        return 'errno = EWOULDBLOCK;'
    elif 'ENOMEM' in errList:
        if errPickMode:
            return None
        return 'errno = ENOMEM;'
    else:
        if errPickMode:
            return None
        errLine = 'int errList[] = {'
        for errno in errList:
            errLine += '{},'.format(errno)
        errLine = errLine[:-1] + "};"
        lengthLine = 'int errlen = {};'.format(len(errList))
        pickLine = "errno = errList[rand() % errlen]; //pick uniform random error"
        line = errLine + lengthLine + pickLine
        if verbose:
            print line
        return line


def CompileSharedLib(filenames, tp, verbose=False):
    if sys.platform == "darwin":
        gcc = ['g++']
        gcc.append('-Wall')
        target = tp + 'libfit.dylib'
    else:
        gcc = ['g++']
        target = tp + 'libfit.so'
        gcc.append('-Wall')
        gcc.append('-shared')
        gcc.append('-Og')
        gcc.append('-std=gnu++0x')
    gcc.append('-fPIC')
    gcc.append('-ggdb')
    gcc.append('-o')
    gcc.append(target)
    if sys.platform == "darwin":
        gcc.append('-dynamiclib')
    # Files that should be compiled
    # Should be interposition folder
    for filename in filenames:
        gcc.append(filename)
    gcc.append('-ldl')
    if verbose:
        print gcc
    call(gcc)
    return target

def CompileTest(filenames, tp, verbose=False):
    gcc = ['g++']
    target = tp + 'selftest'
    gcc.append('-w')
    gcc.append('-g')
    gcc.append('-o')
    gcc.append(target)
    # Files that should be compiled
    # Should be interposition folder
    for filename in filenames:
        gcc.append(filename)
    if verbose:
        print gcc
    call(gcc)
    return target

def main():
    parser = argparse.ArgumentParser(description="Script to generate a interposition library")
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help="Verbose output", default=False)
    parser.add_argument('-e', '--errors', dest='errors', action='store_true',
                        help="Non-random non-critical errors only", default=False)
    parser.add_argument('-t', '--test', dest='test', help="Prepare, compile and execute selftests", action='store_true',
                        default=False)
    parser.add_argument('-b', '--basic', dest='basic', action='store_true', default=False)
    parser.add_argument('-c', '--recompile', dest='recompile', action='store_true',
                        help="Just recompile, without generation", default=False)
    parser.add_argument('-d', '--output-dir', dest='dir', help='Output Path', default='')
    # parser.add_argument('folderpath', help='Path to a folder containing function-def file and src subfolder for source code')
    args = parser.parse_args()
    print "Looking for files at {}".format(os.path.abspath(args.dir))
    interposc = args.dir + "Interposition/src/Interpos.cpp"
    originalh = args.dir + "Interposition/src/Orig.hpp"
    originalc = args.dir + "Interposition/src/Orig.cpp"
    testc = args.dir + "Interposition/src/Test.cpp"
    if not args.recompile:
        print "Refactoring the code"
        with open("Interposition/func-def.yaml", 'rt') as funcDefFile:
            oldfuncs = yaml.safe_load(funcDefFile)
        rm = ['utime', '__isoc99_scanf', '__isoc99_vscanf', '__isoc99_fscanf',
              '__isoc99_vfscanf', '__wprintf_chk', '__vwprintf_chk', '__fwprintf_chk', '__vfwprintf_chk', 'socketpair',
              'calloc', 'malloc', 'realloc']
        funcs = rebuild_func(oldfuncs, True, rm, args.verbose, args.errors)

        # This is for the formatting for the disseration
        # Feel free to remove this
        # def c(a, b):
        #     x = a["name"]
        #     while x.startswith('_') or x.startswith('I') or x.startswith('O'):
        #         x=x[1:]
        #     y = b["name"]
        #     while y.startswith('_')or y.startswith('I') or y.startswith('O'):
        #         y=y[1:]
        #     if x>y:
        #         return 1
        #     elif y>x:
        #         return -1
        #     else:
        #         return 1
        #
        # fn = sorted(funcs, cmp=c)
        # # fn = funcs
        # l = 31
        # for i in range(l):
        #     print "{:23s}{:15s}{:23s}{}".format(fn[4*i]["name"], fn[4*i+1]["name"],fn[4*i+2]["name"],fn[4*i+3]["name"])
        # print "{:23s}{:15s}{}".format(fn[-3]["name"], fn[-2]["name"],fn[-1]["name"])
        # return True


        if args.basic:
            nl = []
            for fn in funcs:
                if 'read' in fn['name'] or 'write' in fn['name'] or 'open' in fn['name'] or 'close' in fn[
                    'name'] or 'getline' in fn['name'] or 'fputs' in fn['name']:
                    nl.append(fn)
            funcs = nl

        # Debugging on a smaller list
        leave_list = ['fread', 'fclose', 'fwrite', 'fopen', 'getline', 'malloc', 'mkdir', 'read']
        flist = []
        for func in funcs:
            if func["name"] in leave_list:
                flist.append(func)
        if args.verbose:
            for func in funcs:
                print func['name'] + str(func['errs'])

        # Uncomment for funcs.yaml being made
        # with open(args.dir + 'funcs.yaml', "wt") as newFile:
        #     pp_yaml(funcs, newFile)

        env = jinja2.Environment(loader=jinja2.FileSystemLoader("."))
        env.tests['exclusive_fgets'] = exclusive_fgets
        env.tests['is_unlocked'] = is_unlocked
        env.tests['is_nb'] = is_nb
        env.tests['buffer'] = is_buffer
        env.tests['with_size'] = with_size
        env.filters['declare_static_variables_string'] = declare_static_variables_string
        env.filters['assign_variables_string'] = assign_variables_string
        env.filters['compare_variables_string'] = compare_variables_string

        print "Making Interpos.cpp"
        with open(interposc, "wt") as fl:
            tmpl = env.get_template('Interposition/Interpos.cpp.tmpl')
            fl.write(tmpl.render(fn_list=funcs))
        print "Making Orig.cpp"
        with open(originalc, "wt") as fl:
            tmpl = env.get_template('Interposition/Orig.cpp.tmpl')
            fl.write(tmpl.render(fn_list=funcs))
        print "Making Orig.hpp"
        with open(originalh, "wt") as fl:
            tmpl = env.get_template('Interposition/Orig.hpp.tmpl')
            fl.write(tmpl.render(fn_list=funcs))
        print "Making fit.config example"
        with open(args.dir + "example_fit.config", "wt") as fl:
            tmpl = env.get_template('Interposition/config.tmpl')
            fl.write(tmpl.render(fn_list=funcs))
        if args.test:
            print "Making tests"
            with open(testc, "wt") as fl:
                tmpl = env.get_template('Interposition/Test.cpp.tmpl')
                fl.write(tmpl.render(fn_list=funcs))
            with open(args.dir + "test.config", "wt") as fl:
                tmpl = env.get_template('Interposition/test.config.tmpl')
                fl.write(tmpl.render(fn_list=funcs))

    files = [interposc,
             originalc,
             'Interposition/src/Logfile.cpp',
             'Interposition/src/main.c']
    if sys.platform == "darwin":
        files = files[:-1]
    print "Compiling the interposition library"
    lbl = CompileSharedLib(files, args.dir, args.verbose)
    # print "Cleaning up"
    # os.remove(interposc)
    # os.remove(originalc)
    # os.remove(originalh)
    if args.test:
        trt = CompileTest([testc], args.dir, args.verbose)
        testconf = args.dir + "test.config"
        import FIT
        FIT.fit(lbl, testconf, trt, None, force_inj_enable=True, force_log_disable=False, verifier=None, debugmode = True)

if __name__ == "__main__":
    main()
