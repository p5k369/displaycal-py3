# -*- coding: utf-8 -*-
import pytest

from DisplayCAL import localization

pytest.skip(allow_module_level=True)
def test_init_1():
    """Test DisplayCAL.localization.init() function."""
    localization.init()
    assert localization.ldict != {}

    result = localization.getstr("comparison_profile")
    expected_result = "Comparison profile"
    assert result == expected_result

    result = localization.getstr("show_advanced_options")
    expected_result = "Show advanced options"
    assert result == expected_result

