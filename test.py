#!/usr/bin/env python3
import os
import sys
import unittest

import sv_mgr


TEST_SV_DIR = "/tmp/sv-mgr-tests/sv"
TEST_SERVICE_DIR = "/tmp/sv-mgr-tests/service"
TEST_SERVICE = os.path.join(TEST_SV_DIR, "testing")
TEST_SERVICE_ENABLED = os.path.join(TEST_SERVICE_DIR, "testing")


def silence_stderr():
    f = open(os.devnull, 'w')
    sys.stderr = f


class SvMgrTests(unittest.TestCase):

    def setUp(self):
        os.makedirs(TEST_SV_DIR, exist_ok=True)
        os.makedirs(TEST_SERVICE_DIR, exist_ok=True)
        os.makedirs(TEST_SERVICE, exist_ok=True)

    def tearDown(self):
        os.rmdir(TEST_SERVICE)
        os.rmdir(TEST_SV_DIR)
        os.rmdir(TEST_SERVICE_DIR)

    def test_check_sv_path_real_service(self):
        self.assertTrue(sv_mgr.check_sv_path(TEST_SERVICE))

    def test_check_sv_path_fake_service(self):
        with self.assertRaises(sv_mgr.NoSuchSvError):
            sv_mgr.check_sv_path(TEST_SERVICE + "foo")

    def test_detect_executable_sv_disable(self):
        self.assertTrue(sv_mgr.detect_executable("sv-disable"))

    def test_detect_executable_sv_enable(self):
        self.assertTrue(sv_mgr.detect_executable("sv-enable"))

    def test_detect_executable_sv_mgr(self):
        self.assertTrue(sv_mgr.detect_executable("sv-mgr"))

    def test_detect_executable_sv_mgr_py(self):
        self.assertTrue(sv_mgr.detect_executable("sv_mgr.py"))

    def test_detect_executable_bad(self):
        with self.assertRaises(sv_mgr.BadExeError):
            sv_mgr.detect_executable("IDK JAJA")

    def test_disable_sv_disabled(self):
        with self.assertRaises(sv_mgr.SvNotEnabledError):
            sv_mgr.disable_sv("testing", TEST_SERVICE_DIR)

    def test_disable_sv_enabled(self):
        sv_mgr.enable_sv("testing", TEST_SV_DIR, TEST_SERVICE_DIR)
        self.assertTrue(sv_mgr.disable_sv("testing", TEST_SERVICE_DIR))

    def test_disable_sv_fake_service(self):
        with self.assertRaises(sv_mgr.SvNotEnabledError):
            sv_mgr.disable_sv("IDK JAJA", TEST_SERVICE_DIR)

    def test_enable_sv_disabled(self):
        self.assertTrue(sv_mgr.enable_sv("testing", TEST_SV_DIR, TEST_SERVICE_DIR))
        os.remove(TEST_SERVICE_ENABLED)

    def test_enable_sv_enabled(self):
        silence_stderr()
        sv_mgr.enable_sv("testing", TEST_SV_DIR, TEST_SERVICE_DIR)
        with self.assertRaises(sv_mgr.SvAlreadyEnabledError):
            sv_mgr.enable_sv("testing", TEST_SV_DIR, TEST_SERVICE_DIR)
        os.remove(TEST_SERVICE_ENABLED)

    def test_enable_sv_fake_service(self):
        with self.assertRaises(sv_mgr.NoSuchSvError):
            sv_mgr.enable_sv("IDK JAJA", TEST_SV_DIR, TEST_SERVICE_DIR)

    def test_list_enabled(self):
        self.assertIsNotNone(sv_mgr.list_services(TEST_SERVICE_DIR))


def main():
    unittest.main()

if __name__ == '__main__':
    main()
