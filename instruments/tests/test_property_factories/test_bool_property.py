#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module containing tests for the bool property factories
"""

# IMPORTS ####################################################################

from __future__ import absolute_import

from nose.tools import raises, eq_

from instruments.util_fns import bool_property
from . import MockInstrument


# TEST CASES #################################################################

# pylint: disable=missing-docstring

def test_bool_property_basics():
    class BoolMock(MockInstrument):
        mock1 = bool_property('MOCK1')
        mock2 = bool_property('MOCK2', inst_true='YES', inst_false='NO')

    mock_inst = BoolMock({'MOCK1?': 'OFF', 'MOCK2?': 'YES'})

    eq_(mock_inst.mock1, False)
    eq_(mock_inst.mock2, True)

    mock_inst.mock1 = True
    mock_inst.mock2 = False

    eq_(mock_inst.value, 'MOCK1?\nMOCK2?\nMOCK1 ON\nMOCK2 NO\n')


def test_bool_property_set_fmt():
    class BoolMock(MockInstrument):
        mock1 = bool_property('MOCK1', set_fmt="{}={}")

    mock_instrument = BoolMock({'MOCK1?': 'OFF'})

    mock_instrument.mock1 = True

    eq_(mock_instrument.value, 'MOCK1=ON\n')


@raises(AttributeError)
def test_bool_property_readonly_writing_fails():
    class BoolMock(MockInstrument):
        mock1 = bool_property('MOCK1', readonly=True)

    mock_instrument = BoolMock({'MOCK1?': 'OFF'})

    mock_instrument.mock1 = True


def test_bool_property_readonly_reading_passes():
    class BoolMock(MockInstrument):
        mock1 = bool_property('MOCK1', readonly=True)

    mock_instrument = BoolMock({'MOCK1?': 'OFF'})

    eq_(mock_instrument.mock1, False)


@raises(AttributeError)
def test_bool_property_writeonly_reading_fails():
    class BoolMock(MockInstrument):
        mock1 = bool_property('MOCK1', writeonly=True)

    mock_instrument = BoolMock({'MOCK1?': 'OFF'})

    _ = mock_instrument.mock1


def test_bool_property_writeonly_writing_passes():
    class BoolMock(MockInstrument):
        mock1 = bool_property('MOCK1', writeonly=True)

    mock_instrument = BoolMock({'MOCK1?': 'OFF'})

    mock_instrument.mock1 = False


def test_bool_property_set_cmd():
    class BoolMock(MockInstrument):
        mock1 = bool_property('MOCK1', set_cmd='FOOBAR')

    mock_inst = BoolMock({'MOCK1?': 'OFF'})

    eq_(mock_inst.mock1, False)
    mock_inst.mock1 = True

    eq_(mock_inst.value, 'MOCK1?\nFOOBAR ON\n')
