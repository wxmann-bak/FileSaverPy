import unittest
from unittest.mock import MagicMock, call, patch

from core import source

__author__ = 'tangz'


class SourceConverterTest(unittest.TestCase):
    def setUp(self):
        self.url = 'http://www.ssd.noaa.gov/PS/TROP/floaters/16W/imagery/20160910_1930Z-avn.gif'
        self.current_time = MagicMock()

    def test_should_convert_single_url_to_source(self):
        urlsrc_to_return = MagicMock()
        urlsrc_func = MagicMock(return_value=urlsrc_to_return)

        converter = source.SourceConverter(urlsrc_func)
        srcs = converter.to_sources(self.url)
        urlsrc_func.assert_called_with(self.url)
        self.assertEqual(srcs, [urlsrc_to_return])

    def test_should_convert_single_url_to_source_with_timeextractor(self):
        urlsrc_to_return = MagicMock()
        urlsrc_to_return.url = self.url
        timeextractor = MagicMock(return_value=self.current_time)
        urlsrc_func = MagicMock(return_value=urlsrc_to_return)

        converter = source.SourceConverter(urlsrc_func, timeextractor=timeextractor)
        srcs = converter.to_sources(self.url)

        timeextractor.assert_called_with(urlsrc_to_return.url)
        self.assertEqual(srcs, [urlsrc_to_return])
        self.assertEqual(urlsrc_to_return.timestamp, self.current_time)

    def test_should_convert_url_set_to_sources(self):
        number_of_urls = 4
        urls_in_set = [self.url + '-{0}'.format(i) for i in range(number_of_urls)]
        urlset_func = MagicMock(return_value=urls_in_set)

        urlsrcs_for_set = [MagicMock() for url in urls_in_set]
        urlsrc_func = MagicMock(side_effect=urlsrcs_for_set)

        converter = source.SourceConverter(urlsrc_func, urlset_func)
        srcs = converter.to_sources(self.url)
        urlset_func.assert_called_with(self.url)
        urlsrc_func.assert_has_calls([call(url) for url in urls_in_set])
        self.assertEqual(srcs, urlsrcs_for_set)

    def test_should_convert_url_set_to_sources_with_timeextractor(self):
        number_of_urls = 4
        urls_in_set = [self.url + '-{0}'.format(i) for i in range(number_of_urls)]
        urlset_func = MagicMock(return_value=urls_in_set)

        urlsrcs_for_set = [MagicMock() for url in urls_in_set]
        for i in range(number_of_urls):
            urlsrcs_for_set[i].url = urls_in_set[i]
        urlsrc_func = MagicMock(side_effect=urlsrcs_for_set)
        times_for_urls = [self.current_time + url[-1] for url in urls_in_set]
        timeextractor = MagicMock(side_effect=times_for_urls)

        converter = source.SourceConverter(urlsrc_func, urlset_func, timeextractor)
        srcs = converter.to_sources(self.url)

        calls_expected = []
        for urlsrc in urlsrcs_for_set:
            calls_expected.append(call.__bool__())
            calls_expected.append(call(urlsrc.url))
        timeextractor.assert_has_calls(calls_expected)
        self.assertEqual([src.timestamp for src in srcs], times_for_urls)


class SourceFilterTest(unittest.TestCase):
    def test_should_pass_time_filter(self):
        mock_urlsrc = MagicMock()
        mock_urlsrc.timestamp = MagicMock()
        timefilter_pass = MagicMock(return_value=True)

        srcfilter = source.SourceFilter(timefilter=timefilter_pass)
        should_pass = srcfilter.should_save(mock_urlsrc)

        timefilter_pass.assert_called_with(mock_urlsrc.timestamp)
        self.assertTrue(should_pass)

    def test_should_pass_ext_filter(self):
        mock_urlsrc = MagicMock()
        mock_urlsrc.ext = 'gif'

        filter_fail = source.SourceFilter(valid_exts=['jpg', 'png'])
        filter_pass = source.SourceFilter(valid_exts=['gif', 'png'])

        self.assertFalse(filter_fail.should_save(mock_urlsrc))
        self.assertTrue(filter_pass.should_save(mock_urlsrc))

    def test_should_pass_filename_filter(self):
        mock_urlsrc = MagicMock()
        mock_urlsrc.filebase = '20160910_1930Z-avn'
        mock_filename_filter = MagicMock(return_value=True)

        thefilter = source.SourceFilter(filename_filter=mock_filename_filter)
        passes = thefilter.should_save(mock_urlsrc)

        mock_filename_filter.assert_called_with(mock_urlsrc.filebase)
        self.assertTrue(passes)


class SourceSettingTest(unittest.TestCase):
    def test_should_get_urlsrcs_with_converter_and_filter(self):
        dummyurl = 'dummyurl'
        dummyurlsrcs = [MagicMock() for i in range(3)]
        converter = source.SourceConverter(None)
        srcfilter = source.SourceFilter()
        with patch.object(converter, 'to_sources', return_value=dummyurlsrcs,
                          autospec=True) as mock_conversion, patch.object(srcfilter, 'should_save', return_value=True,
                                                                          autospec=True) as mock_filter:
            srcsetting = source.SourceSetting(converter, srcfilter)
            urlsrcs = srcsetting.urlsrcs_for(dummyurl)

            mock_conversion.assert_called_with(dummyurl)
            mock_filter.assert_has_calls([call(dummysrc) for dummysrc in dummyurlsrcs])
            self.assertEqual(urlsrcs, dummyurlsrcs)