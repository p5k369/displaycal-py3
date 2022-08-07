# -*- coding: utf-8 -*-
import os
from pathlib import Path
from typing import Tuple

import pytest
import wx
from wx import AppConsole, Button

from DisplayCAL import display_cal, CGATS, config, util_os
from DisplayCAL.config import geticon
from DisplayCAL.dev.mocks import check_call, check_call_str
from DisplayCAL.display_cal import (
    IncrementingInt,
    webbrowser_open,
    install_scope_handler,
    MainFrame,
    get_cgats_path,
    get_cgats_measurement_mode,
    colorimeter_correction_check_overwrite,
    donation_message,
    app_uptodate,
    check_donation,
    app_update_check,
    show_ccxx_error_dialog,
    get_profile_load_on_login_label,
)
from DisplayCAL.util_str import universal_newlines
from DisplayCAL.worker import Worker
from DisplayCAL.wxwindows import ConfirmDialog, BaseInteractiveDialog


@pytest.fixture(scope="class", name="app", autouse=True)
def fixture_app() -> AppConsole:
    """Return app for tests."""
    return wx.GetApp() or wx.App()


@pytest.fixture(scope="class", name="mainframe")
def fixture_mainframe() -> MainFrame:
    """Return mainframe for tests."""
    worker = Worker()
    return display_cal.MainFrame(worker=worker)


def test_colorimeter_correction_check_overwrite(
    data_files,
    mainframe: MainFrame,
) -> None:
    """Test if function reacts as expected to user input."""
    path = data_files["0_16.ti3"].absolute()
    with open(path, "rb") as cgatsfile:
        cgats = universal_newlines(cgatsfile.read())
    print(get_cgats_path(cgats))
    print(os.path.isfile(path))
    with check_call(BaseInteractiveDialog, "ShowWindowModalBlocking", wx.ID_OK):
        assert colorimeter_correction_check_overwrite(mainframe, cgats, True) == True
