#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created Date : 2018/2/27 17:17
# Created By   : Jason.ma

import platform
import os


class ChromeDriverAdapter():
    """
        chromedriver 适配器
    """
    def __init__(self):
        # windows平台获取所有webview包名称shell
        self.webviewPkForWinSh = 'adb -s %s shell pm list packages | findstr "webview"'
        # windows获取webview版本shell
        self.webviewVersionForWinSh = 'adb -s %s shell pm dump %s | findstr "versionName"'
        # mac平台获取所有webview包名称shell
        self.webviewPkForMacSh = 'adb -s %s shell pm list packages | grep "webview"'
        # mac获取webview版本shell
        self.webviewVersionForMacSh = 'adb -s %s shell pm dump %s | grep "versionName"'
        # chromedriver与webview版本的对应关系
        self.verisonMap = {'2.8': [30, 34],
                           '2.10': [34, 36],
                           '2.12': [36, 40],
                           '2.15': [40, 43],
                           '2.20': [43, 49],
                           '2.22': [49, 53],
                           '2.26': [53, 56],
                           '2.29': [56, 59],
                           '2.32': [59, 61],
                           '2.34': [61, 63]}
        # mac平台名称
        self.mac = 'Darwin'
        # windows平台名称
        self.win = 'Windows'
        self.linux = 'Linux'
        self.platformName = platform.system()

    def adapterChromeDriver(self, udid):
        """
        根据手机预置webview版本适配对应的chromedriver
        :param udid: 手机设备udid
        :return: 返回设备对应的chromedriver版本
        """
        chromeDriverPath = ''
        chromeDriverVerison = ''
        webversion = self._get_webview_version(udid)
        # 判断webversion版本是否以数字开头
        if webversion[:1].isdigit():
            webversion = webversion.split('.')[0]
            for key in self.verisonMap:
                if self.verisonMap[key][0] <= int(webversion) < self.verisonMap[key][1]:
                    chromeDriverVerison = key
                    break
        # 拼接chromeDriver路径
        if chromeDriverVerison != '':
            if self.platformName == self.win:
                chromeDriverPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "..\chromedriver"))
                chromeDriverPath = chromeDriverPath + '\chromedriver%s.exe' % chromeDriverVerison
            if self.platformName == self.mac:
                chromeDriverPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../chromedriver"))
                chromeDriverPath = chromeDriverPath + '/chromedriver-mac%s' % chromeDriverVerison
            if self.platformName == self.linux:
                chromeDriverPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../chromedriver"))
                chromeDriverPath = chromeDriverPath + '/chromedriver-linux%s' % chromeDriverVerison

        return chromeDriverPath

    def _get_webview_version(self, udid):
        """
        获取手机webview版本信息
        :param udid: 手机设备udid
        :return:返回webview包名，如果包含多个webview默认返回第一个包名

        """
        webviewVerison = ''

        if self.platformName == self.win:
            webviewPackageSh = self.webviewPkForWinSh % udid
            webviewPackages = self._execute_shell(webviewPackageSh)
            if webviewPackages.__len__() > 0:
                if 'webview' in webviewPackages[0]:
                    webviewPackage = webviewPackages[0].split(':')[1].strip()
                    webviewVersionSh = self.webviewVersionForWinSh % (udid, webviewPackage)
                    webviewVersionInfo = self._execute_shell(webviewVersionSh)
                    if webviewVersionInfo.__len__() > 0:
                        if 'versionName' in webviewVersionInfo[0]:
                            webviewVersion = webviewVersionInfo[0].split('=')[1].strip()
                            return webviewVersion
        # mac、linux平台处理方式相同
        else:
            webviewPackageSh = self.webviewPkForMacSh % udid
            webviewPackages = self._execute_shell(webviewPackageSh)
            if webviewPackages.__len__() > 0:
                if 'webview' in webviewPackages[0]:
                    webviewPackage = webviewPackages[0].split(':')[1].strip()
                    webviewVersionSh = self.webviewVersionForMacSh % (udid, webviewPackage)
                    webviewVersionInfo = self._execute_shell(webviewVersionSh)
                    if webviewVersionInfo.__len__() > 0:
                        if 'versionName' in webviewVersionInfo[0]:
                            webviewVersion = webviewVersionInfo[0].split('=')[1].strip()
                            return webviewVersion

        return webviewVerison

    def _execute_shell(self, shell):
        return os.popen(shell).readlines()


if __name__ == '__main__':
    print ChromeDriverAdapter().adapterChromeDriver('QMS4C16130000172')
