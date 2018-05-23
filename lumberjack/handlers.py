import gzip
import os
import re
import shutil
from logging.handlers import TimedRotatingFileHandler


class GzippedTimedRotatingFileHandler(TimedRotatingFileHandler):

    def __init__(self, filename, when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False):
        """
        :param string filename: path to the desired log file
        :param string when: used with `interval` to determine when to rotate
        :param int interval: used with `when` to determine when to rotate
        :param int backupCount: number of rotated files to keep
        :param string encoding: file encoding to use
        :param boolean delay: defer file opening until first :meth:`BaseRotatingHandler.emit` call
        :param boolean utc: use UTC timestamps

        See :class:`TimedRotatingFileHandler` for more information.
        """
        TimedRotatingFileHandler.__init__(self, filename, when, interval, backupCount, encoding, delay, utc)
        self.recompile_extension_matcher()

    def recompile_extension_matcher(self):
        self.original_matcher = self.extMatch
        new_pattern = self.original_matcher.pattern[:-1] + '.gz$'
        self.extMatch = re.compile(new_pattern)

    def doRollover(self):
        TimedRotatingFileHandler.doRollover(self)
        file_paths = self.get_uncompressed_logs()
        for file_path in file_paths:
            self.compress(file_path)
            os.remove(file_path)

    def get_uncompressed_logs(self):
        dir_name, base_name = os.path.split(self.baseFilename)
        all_files = os.listdir(dir_name)
        return [os.path.join(dir_name, file_name) for file_name in all_files if self.is_uncompressed_rotated_log(file_name, base_name)]

    def is_uncompressed_rotated_log(self, filename, prefix):
        return self.is_log(filename, prefix) and self.is_rotated(filename, prefix) and self.is_uncompressed(filename)

    @staticmethod
    def is_log(filename, prefix):
        return filename.startswith(prefix)

    def is_rotated(self, filename, prefix):
        suffix = filename[len(prefix) + 1:]
        return self.original_matcher.match(suffix)

    @staticmethod
    def is_uncompressed(filename):
        return not filename.endswith('.gz')

    @staticmethod
    def compress(uncompressed_filename):
        compressed_filename = '{}.gz'.format(uncompressed_filename)
        with open(uncompressed_filename, 'rb') as f_in, gzip.open(compressed_filename, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
