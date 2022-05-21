# Copyright (C) 2015 - 2019 Red Hat, Inc.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; If not, see <http://www.gnu.org/licenses/>.
#
# Red Hat Author(s): Anne Mulhern <amulhern@redhat.com>
# Other Author(s): Anne Mulhern <mulhern@cs.wisc.edu>

""" Test utilities. """

# isort: STDLIB
import itertools

import random

# isort: THIRDPARTY
from pypbt import domain

# isort: LOCAL
from justbases import BaseConfig, DisplayConfig, Radix, StripConfig


def build_nat(base,max_len):
    nats = domain.List(domain.Int(max_value = base -1),min_len = 1, max_len = max_len)
    print(nats)
    return nats


def build_base(max_base):
    """
    Builds a base.

    :param int max_base: the maximum base
    """
    ints = domain.Int(max_value = (max_base-2) +1)
    return ints



def build_sign():
    """
    Build a sign value.
    """

    ints = (domain.Int(max_value = (2))-1)
    return ints


build_relation = build_sign



def build_radix(base,max_len):
    """
    Build a radix from base.

    :param int base: the base of the radix"""
    list1 = build_nat(base,max_len)
    list2 = build_nat(base,max_len)
    list3 = build_nat(base,max_len) 
    if list1 == [] and list2 == [] and list3 == []:
        return Radix(0, list1, list2, list3, base)
    return Radix(
        random.randrange(-1,1,2),
        list1,
        list2,
        list3,
        base,)

def build_display_config(base_config, digits_config, strip_config):
    """
    Builds a well-formed display configuration.

    :param BaseConfig base_config: the base config
    :param DigitsConfig digits_config: the digits config
    :param StripConfig strip_config: the strip config
    """
    return DisplayConfig(
        show_approx_str= domain.Boolean(),
        base_config=base_config,
        digits_config=digits_config,
        strip_config=strip_config,)



def build_strip_config():
    """
    Build strip config.
    """
    return StripConfig(domain.Boolean(),domain.Boolean(), domain.Boolean())




def build_base_config():
    """
    Build base config.
    """
    return BaseConfig(domain.Boolean(),domain.Boolean())
