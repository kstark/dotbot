import os
from . import Executor

class Cleaner(Executor):
    '''
    Cleans broken symbolic links.
    '''

    _directive = 'clean'

    def can_handle(self, directive):
        return directive == self._directive

    def handle(self, directive, data):
        if directive != self._directive:
            raise ValueError('Cleaner cannot handle directive %s' % directive)
        return self._process_clean(data)

    def _process_clean(self, targets):
        success = True
        for target in targets:
            success &= self._clean(target)
        if success:
            self._log.info('All targets have been cleaned')
        else:
            self._log.error('Some targets were not succesfully cleaned')
        return success

    def _clean(self, target):
        '''
        Cleans all the broken symbolic links in target that point to
        a subdirectory of the base directory.
        '''
        for item in os.listdir(os.path.expanduser(target)):
            path = os.path.join(os.path.expanduser(target), item)
            if not os.path.exists(path) and os.path.islink(path):
                if self._in_directory(path, self._base_directory):
                    self._log.lowinfo('Removing invalid link %s -> %s' %
                        (path, os.path.join(os.path.dirname(path), os.readlink(path))))
                    os.remove(path)
        return True

    def _in_directory(self, path, directory):
        '''
        Returns true if the path is in the directory.
        '''
        directory = os.path.join(os.path.realpath(directory), '')
        path = os.path.realpath(path)
        return os.path.commonprefix([path, directory]) == directory
