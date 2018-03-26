# -*- coding: utf-8 -*-

from appium.webdriver.common.touch_action import TouchAction
from AppiumLibrary.locators import ElementFinder
from .keywordgroup import KeywordGroup
import string


class _TouchKeywords(KeywordGroup):
    def __init__(self):
        self._element_finder = ElementFinder()

    # Public, element lookups
    def zoom(self, locator, percent="200%", steps=1):
        """
        Zooms in on an element a certain amount.
        """
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        driver.zoom(element=element, percent=percent, steps=steps)

    def pinch(self, locator, percent="200%", steps=1):
        """
        Pinch in on an element a certain amount.
        """
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        driver.pinch(element=element, percent=percent, steps=steps)

    def swipe(self, start_x, start_y, offset_x, offset_y, duration=1000, isScreenshot='N'):
        """
        Swipe from one point to another point, for an optional duration.

        Args:
         - start_x - x-coordinate at which to start
         - start_y - y-coordinate at which to start
         - offset_x - x-coordinate distance from start_x at which to stop
         - offset_y - y-coordinate distance from start_y at which to stop
         - duration - (optional) time to take the swipe, in ms.
         - isScreenshot - screenshot on-off

        Usage:
        | Swipe | 500 | 100 | 100 | 0 | 1000 |

        *!Important Note:* Android `Swipe` is not working properly, use ``offset_x`` and ``offset_y``
        as if these are destination points.
        """
        driver = self._current_application()
        if isScreenshot.lower() == 'y':
            self._auto_screenshot()
        driver.swipe(start_x, start_y, offset_x, offset_y, duration)
        if isScreenshot.lower() == 'y':
            self._auto_screenshot()

    def scroll(self, start_locator, end_locator):
        """
        Scrolls from one element to another
        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        el1 = self._element_find(start_locator, True, True)
        el2 = self._element_find(end_locator, True, True)
        driver = self._current_application()
        driver.scroll(el1, el2)

    def scroll_down(self, locator):
        """Scrolls down to element"""
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        driver.execute_script("mobile: scroll", {"direction": 'down', 'element': element.id})

    def scroll_up(self, locator):
        """Scrolls up to element"""
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        driver.execute_script("mobile: scroll", {"direction": 'up', 'element': element.id})

    def long_press(self, locator):
        """ Long press the element """
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        long_press = TouchAction(driver).long_press(element)
        long_press.perform()

    def tap(self, locator, x_offset=None, y_offset=None, count=1):
        """ Tap element identified by ``locator``.

        Args:
        - ``x_offset`` - (optional) x coordinate to tap, relative to the top left corner of the element.
        - ``y_offset`` - (optional) y coordinate. If y is used, x must also be set, and vice versa
        - ``count`` - can be used for multiple times of tap on that element
        """
        driver = self._current_application()
        el = self._element_find(locator, True, True)
        action = TouchAction(driver)
        action.tap(el, x_offset, y_offset, count).perform()

    def double_tap(self, locator):
        """ Double Tap element identified by ``locator``.

        This behave differently compared to `Tap(count=2)` since execute double tap event in one action.
        """
        driver = self._current_application()
        el = self._element_find(locator, True, True)
        action = TouchAction(driver)
        action.press(el).move_to(x=100, y=0).release().perform()

    def click_a_point(self, x=0, y=0, duration=100):
        """ Click on a point"""
        self._info("Clicking on a point (%s,%s)." % (x, y))
        driver = self._current_application()
        action = TouchAction(driver)
        try:
            action.press(x=float(x), y=float(y)).wait(float(duration)).release().perform()
        except:
            assert False, "Can't click on a point at (%s,%s)" % (x, y)

    def click_element_at_coordinates(self, coordinate_X, coordinate_Y):
        """ click element at a certain coordinate """
        self._info("Pressing at (%s, %s)." % (coordinate_X, coordinate_Y))
        driver = self._current_application()
        action = TouchAction(driver)
        action.press(x=coordinate_X, y=coordinate_Y).release().perform()

    def click_element_at_screen_scale(self, scale_X, scale_Y):
        """click element at a screen scale

        eg. screen resolution is 1080*1920, coordinate_X = 500,coordinate_Y=1000

        then scale_X should be 500/1800, scale_Y should be 1000/1920

        click_element_at_screen_scale(0.8,0.9)
        """
        width, height = self._get_screen_size()
        try:
            coordinate_X = float(scale_X) * float(width)
            coordinate_Y = float(scale_Y) * float(height)
        except ValueError:
            self._error("Please check your param,scale_X or scale_Y is not float.")
        self._info("Pressing at (%s, %s)." % (coordinate_X, coordinate_Y))
        driver = self._current_application()
        action = TouchAction(driver)
        action.press(x=coordinate_X, y=coordinate_Y).release().perform()

    def get_screen_size(self):
        # driver = self._current_application()
        # size = driver.get_window_size()
        width, height = self._get_screen_size()
        return width, height

    def _get_screen_size(self):
        driver = self._current_application()
        size = driver.get_window_size()
        return size['width'], size['height']

    def _auto_screenshot(self):
        platform_name = self._current_application().desired_capabilities['platformName']
        if platform_name.lower() == "android":
            self.screenshot_for_H5("android_auto")
        if platform_name.lower() == "ios":
            self.screenshot("ios_auto")

    def multi_swipe_for_android(self, Point=None):
        """Point 是手势密码坐标点集合.

        point=第一个点集合，第二个点集合，...

        第二个点坐标是相对于第一个坐标的位置，从a滑动到b  a坐标为 100:200 ,b坐标为 500,200

        那么，Point=100:200，400:0，第二个点相对于第一个点 位置为 (500-100) : (200-200)

        依次类推，第三个点坐标是相对第二个点的位置，例如：三个点原坐标list为：

        list=170:710,538:710,906:710，那么，Point=170:710,368:0,368:0
        """
        driver = self._current_application()
        action = TouchAction(driver)
        point = string.split(Point, ",")
        x1 = string.split(point[0], ":")[0]
        y1 = string.split(point[0], ":")[1]

        cmd = "action.press(x=%s,y=%s).wait(500)" % (x1, y1)

        for i in range(len(point)):
            if i == 0:
                pass
            else:
                x = string.split(point[i], ":")[0]
                y = string.split(point[i], ":")[1]
                cmd += ".move_to(x=%s,y=%s).wait(500)" % (x, y)
        cmd += ".release().perform()"

        self._info("scroll cmd is %s" % cmd)

        exec (cmd)
