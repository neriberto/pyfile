from __future__ import print_function
import binascii
import hashlib
from mmap import mmap, PROT_READ
import os
import sys

try:
    import magic
except ImportError:
    pass

try:
    import pydeep
    HAVE_SSDEEP = True
except ImportError:
    HAVE_SSDEEP = False


class PyFile(object):

    def __init__(self, file_path=None, file_data=None):
        """ Construtor da classe
        @param file_path: Caminho completo do arquivo
        @param file_data: Buffer of a file
        """
        self.file_path = file_path

        if file_path:
            with open(self.file_path, 'rb') as f:
                data = mmap(f.fileno(), 0, prot=PROT_READ)
                self.file_data = str()
                while True:
                    line = data.readline()
                    if line == "":
                        break
                    self.file_data = self.file_data + line
                data.close()
        else:
            self.file_data = file_data

    def get_name(self):
        """ Obtem o nome do arquivo """
        if self.file_path is None:
            return "Noname"

        file_name = os.path.basename(self.file_path)
        return file_name

    def get_data(self):
        """
        Retorna o conteudo do arquivo
        :return: retorna uma string com o conteudo do arquivo
        """
        return self.file_data

    def get_size(self):
        """ Obtem o tamanho do arquivo """
        if self.file_path is None:
            return 0
        return os.path.getsize(self.file_path)

    def get_crc32(self):
        """ Obtem o CRC32 do arquivo """
        if self.file_data is None:
            return ''

        res = ''
        crc = binascii.crc32(self.file_data)
        for i in range(4):
            t = crc & 0xFF
            crc >>= 8
            res = '%02X%s' % (t, res)
        return res

    def get_hashes(self):
        """ Obtem os hashes MD5, SHA1, SHA256 e SHA512 do arquivo """
        if self.file_data is None:
            return ''
        md5 = hashlib.md5(self.file_data).hexdigest()
        sha1 = hashlib.sha1(self.file_data).hexdigest()
        sha256 = hashlib.sha256(self.file_data).hexdigest()
        sha512 = hashlib.sha512(self.file_data).hexdigest()
        return md5, sha1, sha256, sha512

    def get_ssdeep(self):
        """ Obtem o hash SSDEEP do arquivo """
        if not HAVE_SSDEEP:
            return ''
        if self.file_data is None:
            return ''
        try:
            return pydeep.hash_file(self.file_path)
        except Exception:
            return ''

    def get_type(self):
        """ Obtem o tipo real do arquivo """
        if self.file_data is None and self.file_path is None:
            return ''

        file_type = self.__get_type_method1()
        if len(file_type) == 0:
            file_type = self.__get_type_method2()

        if len(file_type) == 0:
            file_type = self.__get_type_method3()

        return file_type

    def __get_type_method1(self):
        """ Obtem o tipo real do arquivo """
        try:
            ms = magic.open(magic.MAGIC_NONE)
            ms.load()
            return ms.buffer(self.file_data)
        except:
            return ''

    def __get_type_method2(self):
        """ Obtem o tipo real do arquivo """
        try:
            return magic.from_buffer(self.file_data)
        except:
            return ''

    def __get_type_method3(self):
        """ Obtem o tipo real do arquivo """
        try:
            import subprocess
            file_process = subprocess.Popen(
                    ['file', '-b', self.file_path],
                    stdout=subprocess.PIPE)
            return file_process.stdout.read().strip()
        except:
            return ''


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    if len(sys.argv) > 1:
        my_file = PyFile(file_path=sys.argv[1])
        print("True Type: {}".format(my_file.get_type()))
        print("CRC32: {}".format(my_file.get_crc32()))
        md5, sha1, sha256, sha512 = my_file.get_hashes()
        print("MD5: {}".format(md5))
        print("SHA1: {}".format(sha1))
        print("SHA256: {}".format(sha256))
        print("SHA512: {}".format(sha512))
        print("SSDeep: {}".format(my_file.get_ssdeep()))


if __name__ == "__main__":
    sys.exit(main())
