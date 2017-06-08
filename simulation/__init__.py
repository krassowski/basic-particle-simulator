from os.path import dirname, basename, isfile
import glob
modules = glob.glob(dirname(__file__) + "/*.so")
__all__ = [basename(f)[:-3] for f in modules if isfile(f)]

