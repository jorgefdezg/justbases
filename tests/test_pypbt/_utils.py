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
from fractions import Fraction
import itertools
import string

import random

# isort: THIRDPARTY
from pypbt import domains

# isort: LOCAL
from justbases import BaseConfig, DisplayConfig, Radix, StripConfig
from typing import Iterator

def build_base(max_base):
    """
    Builds a base.

    :param int max_base: the maximum base
    """
    ints = (domains.Int(min_value = 2, max_value = max_base))
    return ints


def build_sign():
    """
    Build a sign value.
    """

    ints = (domains.Int(min_value = -1, max_value = 1))
    return ints


build_relation = build_sign

def build_radix(max_base, max_len):
    """
    Build a well-formed Radix strategy.

    :param int max_base: maximum value for a numeric base
    :param int max_len: the maximum length for the component lists
    """

    def make_radix(base):
        """
        Build a radix from base.

        :param int base: the base of the radix
        """
        list1 = domains.List(domains.Int(min_value = 1,max_value = base-1),min_len = 0, max_len = max_len)
        list2 = domains.List(domains.Int(min_value = 1,max_value = base-1),min_len = 0, max_len = max_len)
        list3 = domains.List(domains.Int(min_value = 1,max_value = base-1),min_len = 0, max_len = max_len)
        if list1 == [] and list2 == [] and list3 == []:
            return domains.DomainPyObject(Radix,0,list1,list2,list3,base)
        return domains.DomainPyObject(Radix,random.randrange(-1,1,2),list1,list2,list3,base)


    base_domain = build_base(max_base)
    base_iterator = iter(base_domain)
    base_value = next(base_iterator)
    return make_radix(base_value)


# def build_radix(max_base, max_len):
#     """
#     Build a well-formed Radix domain.

#     :param int max_base: maximum value for a numeric base
#     :param int max_len: the maximum length for the component lists
#     """
#     base_domain = build_base(max_base)
#     iterator = iter(base_domain)
#     base = next(iterator)
#     list1 = domains.List(domains.Int(min_value = 1,max_value = base-1),min_len = 0, max_len = max_len)
#     list2 = domains.List(domains.Int(min_value = 1,max_value = base-1),min_len = 0, max_len = max_len)
#     list3 = domains.List(domains.Int(min_value = 1,max_value = base-1),min_len = 0, max_len = max_len)
#     if list1 == [] and list2 == [] and list3 == []:
#         return domains.DomainPyObject(Radix,0,list1,list2,list3,base_domain)
#     return domains.DomainPyObject(Radix,random.randrange(-1,1,2),list1,list2,list3,base_domain)

def build_display_config(base_config, digits_config, strip_config):
    """
    Builds a well-formed display configuration.

    :param BaseConfig base_config: the base config
    :param DigitsConfig digits_config: the digits config
    :param StripConfig strip_config: the strip config
    """
    return domains.DomainPyObject(DisplayConfig,
        show_approx_str= domains.Boolean(),
        base_config=base_config,
        digits_config=digits_config,
        strip_config=strip_config)



def build_strip_config():
    """
    Build strip config.
    """
    return domains.DomainPyObject(StripConfig,domains.Boolean(),domains.Boolean(), domains.Boolean())




def build_base_config():
    """
    Build base config.
    """
    return domains.DomainPyObject(BaseConfig,domains.Boolean(),domains.Boolean())
