import os
import sys
import pytest
from ..src.findslot import *
# from freezegun import freeze_time

def test_print():
    assert 'hello' == "hello"

# @freeze_time("2022-07-01 09:00:00")
def test1():
    assert findslot.find_avalible_slot('/openX_task2/in', 30,2) == '2022-07-02 00:00:00'

def test2():
    assert findslot.find_avalible_slot('/openX_task2/in', 10,2) == '2022-07-02 00:00:00'

def test3():
    assert findslot.find_avalible_slot('/openX_task2/in', 10,3) == '2022-07-02 13:02:00'

def test4():
    assert findslot.find_avalible_slot('/openX_task2/in', 30,3) == '2022-07-02 14:00:00'
