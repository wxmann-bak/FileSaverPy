__author__ = 'tangz'

import saver

if __name__ == '__main__':
    savefromral = saver.BatchSaver(exts=['png'], filter=lambda x: 'black' in x)
    savefromral.saveall('http://weather.rap.ucar.edu/radar/nws_nids/BREF1/KDLH/', 'C:\\Users\\tangz\\Documents\\pythontest')
