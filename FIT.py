__author__ = 'laurynaskarazija'
import argparse
import os
import subprocess
import sys
import datetime
import imp


def translateLog(log, target):
    def writetonewlogwithlocations(translate, funclog, f):
        atr = None
        if sys.platform == "darwin":
            atr = subprocess.Popen('gaddr2line -Cpifse {}'.format(target).split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        else:
            atr = subprocess.Popen('addr2line -Cpifse {}'.format(target).split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        translated = atr.communicate(translate)[0]
        trls =  translated.strip().split('\n')
        # print trls
        for i, g in enumerate(funclog):
            j = 2*i
            if "Interpos.cpp" in trls[j]:
                j=j+1
            line = "{}: {}\n".format(funclog[i], trls[j])
            # print line[:-1]
            f.write(line)
    print "Translating"
    with open(log+'new', 'w') as newfile:
        startline = None
        newlog =[]
        translate = ''
        bufferlimit = 500
        curr = 0
        with open(log, 'r') as f:
            startline = f.readline()
            newfile.write(startline)
            line = f.readline()
            while line!='':
                words = line.strip().split()
                if len(words) == 3 and words[1].startswith('0x') and words[2].startswith('0x'):
                    newlog.append(words[0])
                    translate+=words[1]+'\n'+words[2]+'\n'
                    curr+=1
                    if curr>=bufferlimit:
                        writetonewlogwithlocations(translate, newlog, newfile)
                        translate = ''
                        newlog = []
                        curr = 0
                line = f.readline()
            writetonewlogwithlocations(translate, newlog, newfile)
    os.remove(log)
    os.rename(log+'new', log)


class InjectionTarget:
    def __init__(self, path):
        if path.startswith('/'):
            self.type = 'absolute'
            self.path = path
        elif path.startswith('.'):
            self.type = 'relative'
            self.path = path
        else:
            self.path = './' + path
            self.type = 'relative'

    def getpath(self):
        return self.path

    def getstring(self):
        return self.path

    def __str__(self):
        return self.path


class Run(object):
    def __init__(self, lib, exe, args, configfile,debugmode=False, recovery_mode=False):
        self.env = os.environ.copy()
        self.lib = lib
        self.exe = exe
        self.args = args
        self.configFile = configfile
        self.forceInj = False
        self.debugmode = debugmode
        self.recovery_mode=recovery_mode

    def get_unique_names(self, seed):
        pfi = (str(self.exe) + "_activationlog_{}.dat".format(str(seed))).split('/')[-1]
        mfi = (str(self.exe) + "_log_{}.dat".format(str(seed))).split('/')[-1]
        ofi = (str(self.exe) + "_outlog_{}.dat".format(str(seed))).split('/')[-1]
        efi = (str(self.exe) + "_errlog_{}.dat".format(str(seed))).split('/')[-1]
        ifi = (str(self.exe) + "_inlog_{}.dat".format(str(seed))).split('/')[-1]
        return pfi, mfi, ofi, efi, ifi

    def prep_control(self, injmode, forcelog=False, seed=0, filename='fit.control'):
        self.env["FIT_ENV_READ_TEST"] = "TEST"
        if sys.platform == "darwin":
            print "Darwin detected: using DYLD_INSERT_LIBRARIES"
            self.env["DYLD_INSERT_LIBRARIES"] = os.path.abspath(self.lib)
            self.env["DYLD_FORCE_FLAT_NAMESPACE"] = '1'
        else:
            self.env["LD_PRELOAD"] = os.path.abspath(self.lib)
        pfi, mfi, ofi, efi, ifi = self.get_unique_names(seed)
        options, mfile, ofile, efile, ifile, logging = parse_config_file(self.configFile, mfi, ofi, efi, ifi)
        self.logs_get_collected = (logging or forcelog)
        print "Injection enable: {}".format(injmode)
        print "Logging enable: {}".format(self.logs_get_collected)
        if self.logs_get_collected:
            print "Main logfile: {}".format(mfile)
            print "StdOut logfile: {}".format(ofile)
            print "StdErr logfile: {}".format(efile)
            print "Input logfile: {}".format(ifile)
            print "FIT logs : {}".format(pfi)
            if self.debugmode:
                print "FIT log will be transtaleted to contain source locations"
        if self.recovery_mode:
            print "Recover detection enabled - will attempt to detect recovery calls"
        self.env["FIT_CONTROL_FILE"] = create_control_file(options, mfile, ofile, efile, ifile, pfi, injmode,
                                                         (logging or forcelog), filename, self.debugmode, self.recovery_mode)
        return pfi, mfile, ofile, efile, ifile


class TestRun(Run):
    def __init__(self, lib, exe, args, configfile, log=True, debugmode=False, recovery_mode=False):
        super(TestRun, self).__init__(lib, exe, args, configfile, debugmode, recovery_mode)
        self.logging = log

    def execute_test(self):
        md = True
        if self.forceInj:
            md = False
        pfi = self.prep_control(md, self.logging)[0]
        call_line = [str(self.exe)]
        if self.args is not None:
            if isinstance(self.args, list):
                call_line += self.args
            else:
                call_line += [self.args]
        print call_line
        t = subprocess.Popen(call_line, env=self.env)
        t.wait()
        if self.debugmode and self.logs_get_collected:
            translateLog(pfi, str(self.exe))
        return 'RT: {}'.format(t.returncode)


class VerificationRun(Run):
    def __init__(self, lib, exe, args, configFile, verifier, debugmode=False,recovery_mode=False):
        super(VerificationRun, self).__init__(lib, exe, args, configFile, debugmode, recovery_mode)
        self.logging = True
        self.verify = verifier

    def execute_test(self):
        self.cpfi, self.cmfi, self.cofi, self.cefi, self.cifi = self.prep_control(False, True,
                                                                                 str(datetime.datetime.now())[11:])
        callLine = [str(self.exe)]
        if self.args != None:
            if isinstance(self.args, list):
                callLine += self.args
            else:
                callLine += [self.args]
        print str(callLine) + "  Clean run"
        sys.stdout.flush()
        cleanProc = subprocess.Popen(callLine, env=self.env)
        cleanProc.wait()
        if self.debugmode:
            translateLog(self.cpfi, str(self.exe))
        self.crt = cleanProc.returncode
        print str(callLine) + "  Dirty run"
        sys.stdout.flush()
        self.dpfi, self.dmfi, self.dofi, self.defi, self.difi = self.prep_control(True, True,
                                                                                 str(datetime.datetime.now())[11:])
        dirtyProc = subprocess.Popen(callLine, env=self.env)
        dirtyProc.wait()
        if self.debugmode:
            translateLog(self.dpfi, str(self.exe))
        self.drt = dirtyProc.returncode
        return self.verify(self.crt, self.cifi, self.cofi, self.cefi, self.cmfi,
                           self.drt, self.difi, self.dofi, self.defi, self.dmfi)


def parse_config_file(config, mfi, ofi, efi, ifi):
    mfile = mfi
    ofile = ofi
    efile = efi
    ifile = ifi
    logging = True
    options = []
    with open(config, 'r') as f:
        while True:
            line = f.readline()
            if len(line) is 0:
                break
            elif not line.startswith('FIT'):
                continue
            else:
                words = line.strip().split()[0].split('=')
                if words[0] == 'FIT_input_log':
                    ifile = words[1]
                elif words[0] == 'FIT_main_log':
                    mfile = words[1]
                elif words[0] == 'FIT_stdout_log':
                    ofile = words[1]
                elif words[0] == 'FIT_stderr_log':
                    efile = words[1]
                elif words[0] == 'FIT_LOGGING_ENABLE':
                    logging = (words[1] == '1')
                else:
                    options.append('{}\n'.format(words[1]))
    return options, mfile, ofile, efile, ifile, logging


def create_control_file(options, mFile, oFile, eFile, iFile, pFile, injCtln, logging, fl='control.fit', debugmode=False, recovery=False):
    with open(fl, 'wt') as out:
        if injCtln:
            out.write('1\n')
        else:
            out.write('0\n')
        if logging:
            out.write('1\n')
        else:
            out.write('0\n')
        if debugmode:
            out.write('1\n')
        else:
            out.write('0\n')
        if recovery:
            out.write('1\n')
        else:
            out.write('0\n')
        for opt in options:
            out.write(opt)
        out.write(pFile + '\n')
        out.write(mFile + '\n')
        out.write(oFile + '\n')
        out.write(eFile + '\n')
        out.write(iFile + '\n')
    return os.getcwd() + '/' + fl

def fit(interposition_lib, config_file, target, args, force_inj_enable=False, force_log_disable=False, verifier=None, debugmode = False, recovery=False):
    print target
    injtarget = InjectionTarget(target)
    if verifier is not None:
        run = VerificationRun(interposition_lib, injtarget, args, config_file, verifier, debugmode, recovery)
        if force_inj_enable:
            run.forceInj = True
        return run.execute_test()
    else:
        run = TestRun(interposition_lib, injtarget, args, config_file, not force_log_disable, debugmode, recovery)
        rt = run.execute_test()
        sys.stdout.flush()
        print rt
        return rt

def main():
    interposition_lib = 'libfit.so'
    parser = argparse.ArgumentParser(description="A Library injection program", prefix_chars='+')
    parser.add_argument('+a', '++verify', dest='verify',
                        help="Use the following module for verification, must contain verify()", default=None)
    parser.add_argument('+p', '++log-disable', dest='log', action='store_false', help="logging?", default=True)
    parser.add_argument('+d', '++disable', dest='disable', help='Force injection off', action='store_true',
                        default=False)
    parser.add_argument('+g', '++debug', dest='debugmode', help='Attempt to track call location from debug symbols', action='store_true',
                        default=False)
    parser.add_argument('+r', '++recovery', dest='recovery_mode', help='Attempt to track call location from debug symbols', action='store_true',
                        default=False)
    parser.add_argument('+l', '++lib', dest='lib', help="Interposition library", default=interposition_lib)
    parser.add_argument('config', help="config file")
    parser.add_argument('target', help="target binary")
    parser.add_argument('args', help="arguments to be passsed to a binary", nargs='*')
    args = parser.parse_args()
    ver = None
    if args.verify is not None:
        try:
            path= os.path.abspath(args.verify)
            verify = imp.load_source('ver', path)
        except Exception:
            raise Exception("Importing verifyer failed")
        if verify.verify is None:
            raise Exception("Wrong verifier")
        ver = verify.verify
    if args.debugmode:
        if sys.platform == "darwin":
            check = subprocess.check_output(['which', 'gaddr2line'])
            if check=='':
                print "No gaddr2line found; please install binutils"
                return -1
        else:
            check = subprocess.check_output(['which', 'addr2line'])
            if check=='':
                print "No addr2line found; please install binutils"
                return -1
    return fit(args.lib,args.config, args.target, args.args, args.disable, args.log, ver, args.debugmode, args.recovery_mode)

if __name__ == "__main__":
    main()
