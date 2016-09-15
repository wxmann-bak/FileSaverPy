from datetime import datetime, timedelta
import re
from core import source, saver, target, urlextractors

__author__ = 'tangz'

_OUTPUT_DATETIME = '%Y%m%d-%H%M%S'

_VISIBLE_FILTER = lambda filename: 'color' not in filename and 'hires' not in filename
_IR_COLOR_FILTER = lambda filename: 'color' in filename


def save_target_sector_realtime(sattype, saveloc, save_period=timedelta(hours=1), hours_behind=1,
                                filename_filter=None, addnl_time_filter=lambda ts: True):
    url_raw = 'http://weather-models.info/latest/images/himawari/target/{0}/'.format(sattype)

    def timed_urlset(url):
        current_time = datetime.utcnow()
        save_time = current_time - timedelta(hours=hours_behind)
        save_hr = save_time.hour
        hr_str = str(save_hr) if save_hr >= 10 else ('0' + str(save_hr))
        return urlextractors.listingurl(url + hr_str)

    batchsetting = _get_src_setting(sattype, filename_filter, addnl_time_filter, urlset_func=timed_urlset)
    targsetting = _get_targ_setting(sattype)

    thesaver = saver.Session().create_context('himawari-realtime', batchsetting, targsetting, saveperiod=save_period)

    jobid = '{0}-himawari-realtime'.format(sattype)
    thesaver.submit(jobid, url_raw, saveloc)
    thesaver.runjob(jobid, end=datetime.now() + timedelta(seconds=10))


def save_target_sector_hist(sattype, hours, saveloc, filename_filter=None, addnl_time_filter=lambda ts: True):
    url_raw = 'http://weather-models.info/latest/images/himawari/target/{0}/'.format(sattype)
    batchsetting = _get_src_setting(sattype, filename_filter, addnl_time_filter)
    targsetting = _get_targ_setting(sattype)

    thesaver = saver.Session().create_context('himawari-hist', batchsetting, targsetting)

    for hr in hours:
        hr_str = str(hr) if hr >= 10 else ('0' + str(hr))
        jobid = '{0}-himawari-{1}'.format(sattype, hr_str)
        url = url_raw + hr_str
        thesaver.submit(jobid, url, saveloc)
        thesaver.runjob(jobid)


def _get_src_setting(sattype, filename_filter, addnl_time_filter, urlset_func=urlextractors.listingurl):
    timefilter = lambda ts: ts.minute % 10 == 0 and addnl_time_filter(ts)
    exts = ['png']
    def getfilefilter():
        if filename_filter:
            return filename_filter
        elif sattype.lower() == 'ir':
            return _IR_COLOR_FILTER
        elif sattype.lower() == 'vis':
            return _VISIBLE_FILTER
        else:
            raise ValueError("Invalid satellite type: " + sattype)

    return source.batch(urlset_func=urlset_func, timefilter=timefilter, filename_filter=getfilefilter(),
                        valid_exts=exts, timeextractor=_time_extractor)


def _get_targ_setting(sattype):
    filename_template = sattype + '-himawari-{ts}'
    filename_builder = lambda template, timestamp: template.format(ts=timestamp.strftime(format=_OUTPUT_DATETIME))
    return target.withfiletemplate(filename_builder, filename_template)


def _time_extractor(url):
    regex = '\/(\d{2})(\d{2})(\d{2})-'
    # df = '%H%M%S'
    matches = re.search(regex, url)
    if not matches:
        raise ValueError("Regex is wrong, cannot parse time")
    found_hour = int(matches.group(1))
    found_minute = int(matches.group(2))
    found_second = int(matches.group(3))

    right_now = datetime.utcnow()
    if found_hour > right_now.hour:
        dt = timedelta(days=1)
        day_before = right_now - dt
        return datetime(year=day_before.year, month=day_before.month, day=day_before.day, hour=found_hour,
                        minute=found_minute, second=found_second)
    else:
        return datetime(year=right_now.year, month=right_now.month, day=right_now.day, hour=found_hour,
                        minute=found_minute, second=found_second)

