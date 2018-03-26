# -*- coding: utf-8 -*-
import base64
import os
import robot
import datetime
from datetime import date
from .keywordgroup import KeywordGroup
from robot.libraries.BuiltIn import BuiltIn
from time import sleep

class _ScreenshotKeywords(KeywordGroup):
    def __init__(self):
        self._screenshot_index = 0

    # Public

    def capture_page_screenshot(self, filename=None):
        """Takes a screenshot of the current page and embeds it into the log.

        `filename` argument specifies the name of the file to write the
        screenshot into. If no `filename` is given, the screenshot is saved into file
        `appium-screenshot-<counter>.png` under the directory where
        the Robot Framework log file is written into. The `filename` is
        also considered relative to the same directory, if it is not
        given in absolute format.

        `css` can be used to modify how the screenshot is taken. By default
        the bakground color is changed to avoid possible problems with
        background leaking when the page layout is somehow broken.
        """
        # path, link = self._get_screenshot_paths(filename)
        current_context = self._current_application().current_context
        if str(current_context).lower().startswith('web'):
            self._current_application().switch_to.context('NATIVE_APP')
        path, link = self._get_screenshot(filename)
        if hasattr(self._current_application(), 'get_screenshot_as_file'):
            self._current_application().get_screenshot_as_file(path)
        else:
            self._current_application().save_screenshot(path)

        # Image is shown on its own row and thus prev row is closed on purpose
        # self._html('</td></tr><tr><td colspan="3"><a href="%s">'
        #            '<img src="%s" width="800px"></a>' % (link, link))
        logdir = self._get_log_dir()
        path = path.replace(logdir, '.\\')
        self._html('</td></tr><tr><td colspan="3"><a href="%s">'
                   '<img src="%s" width="800px"></a>' % (path, path))
        if str(current_context).lower().startswith('web'):
            self._current_application().switch_to.context(current_context)


    def screenshot(self, filename=None):
        """根据文件名截图，截图前需要在测试套中设置 ${date}变量（date为图片存放根目录文件夹名称,

        若未设置测试套变量${date}时，文件保存根目录为测试套名称）
        | screenshot | filename=测试 |
        """
        current_context = self._current_application().current_context
        if str(current_context).lower().startswith('web'):
            self._current_application().switch_to.context('NATIVE_APP')
        path, link = self._get_screenshot(filename)
        if hasattr(self._current_application(), 'get_screenshot_as_file'):
            self._current_application().get_screenshot_as_file(path)
        else:
            self._current_application().save_screenshot(path)
        # Image is shown on its own row and thus prev row is closed on purpose

        logdir = self._get_log_dir()
        path = path.replace(logdir, '.\\')
        self._html('</td></tr><tr><td colspan="3"><a href="%s">'
                   '<img src="%s" width="800px"></a>' % (path, path))
        if str(current_context).lower().startswith('web'):
            self._current_application().switch_to.context(current_context)
    def screenshot_for_H5(self, filename=None):
        """适配android部分机型context切换h5后截图卡死.
        该方法仅适用于 appium-server 与脚本执行在同一台机器上，否则报错
        This method only valid for Android.
        """
        sleep(1)
        self._info("ADB Start screnshot_test imge...")
        logdir = self._get_log_dir()
        variables = BuiltIn().get_variables()
        path1, link = self._get_screenshot(filename)
        try:
            udid = variables['${udid}']
            os.system("adb -s %s shell /system/bin/rm /data/local/tmp/screenshot_for_H5.png" % udid)
            os.system("adb -s %s shell /system/bin/screencap -p /data/local/tmp/screenshot_for_H5.png" % udid)
            # res = os.system("adb -s %s pull /data/local/tmp/screenshot_for_H5.png %s " % (udid, logdir))
            # if res > 0:
            #     self._warn("ADB Screenshot Fail, Please check your param.")
            # path2 = os.path.join(logdir, "screenshot.png")
            # os.rename(path2, path1.decode("utf-8"))

            driver = self._current_application()
            theFile = driver.pull_file("/data/local/tmp/screenshot_for_H5.png")
            theFile = base64.b64decode(theFile)
            try:
                with open(path1, 'wb') as f:
                    f.write(theFile)
            except IOError:
                return False
            finally:
                del theFile
            self._html('</td></tr><tr><td colspan="3"><a href="file:\\%s">'
                       '<img src="file:\\\%s" width="800px"></a>' % (path1, path1))
            self._info("ADB Screenshot success.")
        except KeyError:
            self._warn(
                "ADB screenshot must input udid, otherwise ,will be effect your screenshot."
                "Usage: -v udid:GWY0217302002791")

    # Private

    def _get_screenshot(self, filename):
        variables = BuiltIn().get_variables()
        suite_name = variables['${SUITE NAME}']
        test_name = variables['${TEST NAME}']
        date = None
        udid = None
        logdir = self._get_log_dir()
        imgdate = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        if not filename:
            self._screenshot_index += 1
            filename = '%s-%s.png' % (imgdate, self._screenshot_index)
        else:
            filename = filename.replace('/', os.sep)
            filename = '%s-%s.png' % (imgdate, filename)
        try:
            udid = variables['${udid}']
        except KeyError:
            self._warn(
                "Variables ${udid} cannot be None, otherwise ,will be affect your screenshot."
                "Usage: -v udid:GWY0217302002791.")
        try:
            date = variables['${date}']
        except KeyError:
            self._warn(
                "Variables ${date} cannot be None, otherwise ,will be affect your screenshot.")
        if not date:
            imgdir = os.path.join(logdir, suite_name, test_name)
        else:
            imgdir = os.path.join(logdir, date, suite_name, test_name)
        if udid:
            imgdir = os.path.join(imgdir, udid)
        if not os.path.exists(imgdir):
            os.makedirs(imgdir)
        path = os.path.join(imgdir, filename)
        link = robot.utils.get_link_path(path, imgdir)
        return path, link

    def _get_screenshot_paths(self, filename):
        if not filename:
            self._screenshot_index += 1
            filename = 'appium-screenshot-%d.png' % self._screenshot_index
        else:
            filename = filename.replace('/', os.sep)
        logdir = self._get_log_dir()
        path = os.path.join(logdir, filename)
        link = robot.utils.get_link_path(path, logdir)
        return path, link
