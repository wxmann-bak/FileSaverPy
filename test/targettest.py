from datetime import datetime
import os
import unittest

import core.source
from core import target


class TargetSettingTest(unittest.TestCase):

    def test_file_target_output_str(self):
        dir = "C:\Me"
        targ = core.target.FileTarget("C:\Me", "abc", "jpg", None)
        self.assertEqual(str(targ), os.path.join(dir, "abc.jpg"))

    def test_file_target_output_str_with_dot_in_ext(self):
        dir = "C:\Me"
        targ = core.target.FileTarget("C:\Me", "abc", ".jpg", None)
        self.assertEqual(str(targ), os.path.join(dir, "abc.jpg"))

    def test_directory_target_copy_from(self):
        dir = "C:/Me"
        targ = target.copyfilename().withdir(dir)
        src = core.source.URLSource("http://weather.rap.ucar.edu/radar/nws_nids/BREF1/KDLH/20160511_085022_gray.png")

        filetarg = targ.tofiletarget(src)
        self.assertEqual(filetarg.folder, dir)
        self.assertEqual(filetarg.file, "20160511_085022_gray")
        self.assertEqual(filetarg.ext, "png")

    def test_directory_target_copy_from_with_mutator(self):
        dir = "C:/Me"
        mutator = lambda file, ts: 'KDLH-' + file
        targ = target.copyfilename(mutator).withdir(dir)
        src = core.source.URLSource("http://weather.rap.ucar.edu/radar/nws_nids/BREF1/KDLH/20160511_085022_gray.png")

        filetarg = targ.tofiletarget(src)
        self.assertEqual(filetarg.folder, dir)
        self.assertEqual(filetarg.file, "KDLH-20160511_085022_gray")
        self.assertEqual(filetarg.ext, "png")

    def test_use_filetemplate_to_build_file(self):
        filename_func = lambda templt, ts: templt.format(ts=ts.strftime("%Y%m%d_%H%M%S"))
        template = "KDLH-{ts}"
        directory = "C:\\Me"
        targ = target.withfiletemplate(filename_func, template).withdir(directory)

        src = core.source.URLSource("http://weather.rap.ucar.edu/radar/nws_nids/BREF1/KDLH/20160511_085022_gray.png")
        src.timestamp = datetime(year=2016, month=5, day=11, hour=8, minute=50, second=22)

        filetarg = targ.tofiletarget(src)
        self.assertEqual(filetarg.folder, directory)
        self.assertEqual(filetarg.file, "KDLH-20160511_085022")
        self.assertEqual(filetarg.ext, "png")

    def test_use_filetemplate_to_build_file_with_kwargs(self):
        filename_func = lambda templt, ts, bg: templt.format(ts=ts.strftime("%Y%m%d_%H%M%S"), bg=bg)
        template = "KDLH-{ts}-{bg}"
        directory = "C:\\Me"
        targ = target.withfiletemplate(filename_func, template, bg='black').withdir(directory)

        src = core.source.URLSource("http://weather.rap.ucar.edu/radar/nws_nids/BREF1/KDLH/20160511_085022_gray.png")
        src.timestamp = datetime(year=2016, month=5, day=11, hour=8, minute=50, second=22)

        filetarg = targ.tofiletarget(src)
        self.assertEqual(filetarg.folder, directory)
        self.assertEqual(filetarg.file, "KDLH-20160511_085022-black")
        self.assertEqual(filetarg.ext, "png")