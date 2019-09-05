# -*- coding: utf-8 -*-
# -*- author: Floyda -*-

import sublime
import sublime_plugin
import os
import subprocess


def plugin_loaded():
    check_tests_file()


def get_tests_path():
    home_path = os.path.expanduser("~")
    tpath = os.path.join(home_path, ".test")
    return tpath


def check_tests_file():
    tpath = get_tests_path()

    if not os.path.exists(tpath):
        os.mkdir(tpath)

    package_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(package_path, "suffix.txt")) as fp:
        lines = fp.readlines()
        prefix = "test"
        for suffix in lines:
            suffix = suffix.replace("\n", "")
            fname = "%s.%s" % (prefix, suffix)
            path = os.path.join(tpath, fname)
            with open(path, "a+") as fp:
                fp.write("")
                fp.close()


class TestsAddFolderCommand(sublime_plugin.WindowCommand):
    def run(self):
        tpath = get_tests_path()

        executable_path = sublime.executable_path()
        if sublime.platform() == "osx":
            app_path = executable_path[: executable_path.rfind(".app/") + 5]
            executable_path = os.path.join(app_path, "Contents/SharedSupport/bin/subl")
        subprocess.Popen([executable_path, "-a", tpath])


class TestsRemoveFolderCommand(sublime_plugin.WindowCommand):
    def run(self):
        tpath = get_tests_path()
        project_data = self.window.project_data()
        new_folders = []
        for x in project_data.get("folders"):
            if x.get("path") != tpath:
                new_folders.append(x)
        project_data["folders"] = new_folders
        self.window.set_project_data(project_data)
