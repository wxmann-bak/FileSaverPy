import unittest

import core.source
from core import target


class TargetSettingTest(unittest.TestCase):

    def test_directory_target_copyfrom(self):
        dir = "C:/Me"
        targ = target.copyfilename().withdir(dir)
        src = core.source.URLSource("http://weather.rap.ucar.edu/radar/nws_nids/BREF1/KDLH/20160511_085022_gray.png")

        filetarg = targ.tofiletarget(src)
        self.assertEqual(filetarg.folder, dir)
        self.assertEqual(filetarg.file, "20160511_085022_gray")
        self.assertEqual(filetarg.ext, "png")