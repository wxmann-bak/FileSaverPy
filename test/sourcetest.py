from datetime import datetime
import unittest
from unittest.mock import MagicMock, call

from core import source


__author__ = 'tangz'


class SingularSourceSettingTest(unittest.TestCase):
    def setUp(self):
        self.url = 'http://www.ssd.noaa.gov/PS/TROP/floaters/16W/imagery/20160910_1930Z-avn.gif'
        self.current_time = datetime.now()

    def test_should_extract_urlsrc(self):
        mock_urlsrc = MagicMock()
        mock_urlsrc_extractor = MagicMock(return_value=mock_urlsrc)

        srcsetting = source.singular(urlsrc_func=mock_urlsrc_extractor).forurl(self.url)
        actual_urlsrc = srcsetting.geturlsrc()

        mock_urlsrc_extractor.assert_called_with(self.url)
        self.assertEqual(actual_urlsrc, mock_urlsrc)

    def test_should_extract_urlsrc_with_timestamp(self):
        mock_urlsrc = MagicMock()
        mock_urlsrc.url = self.url
        mock_urlsrc_extractor = MagicMock(return_value=mock_urlsrc)
        mock_timeextractor = MagicMock(return_value=self.current_time)

        srcsetting = source.singular(urlsrc_func=mock_urlsrc_extractor,
                                     timeextractor=mock_timeextractor).forurl(self.url)
        actual_urlsrc = srcsetting.geturlsrc()

        mock_urlsrc_extractor.assert_called_with(self.url)
        mock_timeextractor.assert_called_with(mock_urlsrc.url)

        self.assertEqual(actual_urlsrc, mock_urlsrc)
        self.assertEqual(actual_urlsrc.timestamp, self.current_time)

    def _override_urlsrc_for_setting(self, urlsrc):
        def dummyseturl(self, url):
            self._urlsrc = urlsrc
            return self
        source.SourceSetting.forurl = dummyseturl

    def test_should_pass_time_filter(self):
        mock_urlsrc = MagicMock()
        mock_urlsrc.timestamp = self.current_time
        timefilter_pass = MagicMock(return_value=True)

        self._override_urlsrc_for_setting(mock_urlsrc)
        srcsetting = source.singular(timefilter=timefilter_pass).forurl(self.url)
        url_passes = srcsetting.shouldsave()

        timefilter_pass.assert_called_with(mock_urlsrc.timestamp)
        self.assertTrue(url_passes)

    def test_should_pass_ext_filter(self):
        mock_urlsrc = MagicMock()
        mock_urlsrc.ext = 'gif'

        self._override_urlsrc_for_setting(mock_urlsrc)
        srcsetting_fail = source.singular(valid_exts=['jpg', 'png']).forurl(self.url)
        srcsetting_pass = source.singular(valid_exts=['gif', 'png']).forurl(self.url)

        self.assertFalse(srcsetting_fail.shouldsave())
        self.assertTrue(srcsetting_pass.shouldsave())

    def test_should_pass_filename_filter(self):
        mock_urlsrc = MagicMock()
        mock_urlsrc.filebase = '20160910_1930Z-avn'
        mock_filename_filter = MagicMock(return_value=True)

        self._override_urlsrc_for_setting(mock_urlsrc)
        srcsetting = source.singular(filename_filter=mock_filename_filter).forurl(self.url)
        passes = srcsetting.shouldsave()

        mock_filename_filter.assert_called_with(mock_urlsrc.filebase)
        self.assertTrue(passes)


class BatchSourceSettingTest(unittest.TestCase):
    def test_should_extract_urlsrcs(self):
        number_of_urls = 3
        urls = ['http://www.ssd.noaa.gov/20160910_1930Z-avn-{0}.gif'.format(i) for i in range(number_of_urls)]
        parent_url = 'http://www.ssd.noaa.gov/allimages'
        urlsrcs_map = {}
        for url in urls:
            mock_urlsrc_to_add = MagicMock()
            mock_urlsrc_to_add.url = url
            urlsrcs_map[url] = mock_urlsrc_to_add
        urlsrc_mocks = urlsrcs_map.values()

        mock_urlset_func = MagicMock(return_value=urls)
        def set_url_stub(self, url):
            self._urlsrc = urlsrcs_map[url]
        source.SourceSetting.forurl = set_url_stub

        mock_shouldsave = MagicMock(return_value=True)
        source.SourceSetting.shouldsave = mock_shouldsave

        indiv_setting = source.singular()
        batch_setting = source.BatchSourceSetting(indiv_setting, mock_urlset_func).forurl(parent_url)
        all_outputs = batch_setting.geturlsrcs()

        mock_urlset_func.assert_called_with(parent_url)
        mock_shouldsave.assert_has_calls([call() for i in range(number_of_urls)])

        for urlsrc_mock in urlsrc_mocks:
            self.assertIn(urlsrc_mock, all_outputs)