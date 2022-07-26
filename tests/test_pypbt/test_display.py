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

""" Test for utility functions. """

# isort: STDLIB
import unittest

# isort: THIRDPARTY
from pypbt.quantifiers import forall,exists
from pypbt import domains
# isort: LOCAL
from justbases import BaseConfig, DigitsConfig, StripConfig
from justbases._display import Number, String, Strip

# isort considers this third party, but it is not
from _utils import build_base, build_base_config, build_display_config, build_radix, build_relation, build_sign, build_strip_config

tc = unittest.TestCase()

@forall(radix = build_radix(20,10))
@forall(display = build_display_config(BaseConfig(),DigitsConfig(use_letters=False),build_strip_config))
@forall(relation = build_relation())
def test_format(radix, display, relation):
    """
    Verify that a xformed string with a repeating part shows that part.
    """
    print(display)
    result = String(display, radix.base).xform(radix, relation)
    tc.assertEqual(
        radix.repeating_part != [] and not display.base_config.use_subscript,
        result[-1] == ")",
    )


"""
Test Number.
"""

@forall(integer_part = domains.String(max_len = 10),n_samples = 5)
@forall(non_repeating_part = domains.String(min_len = 1,max_len = 10),n_samples = 5)
@forall(repeating_part = domains.String(max_len = 10),n_samples = 5)
@forall(config = build_base_config(),n_samples = 5)
@forall(base = build_base(16),n_samples = 5)
@forall(sign = build_sign(),n_samples = 5)
def test_xform(
    integer_part, non_repeating_part, repeating_part, config, base, sign
):
    """
    Test xform.
    """
    # pylint: disable=too-many-arguments

    result = Number(config, base).xform(
        integer_part, non_repeating_part, repeating_part, base, sign
    )
    if config.use_prefix and base == 16 and sign != -1:
        tc.assertTrue(result.startswith("0x"))
    if config.use_prefix and base == 8 and sign != -1:
        tc.assertTrue(result.startswith("0"))
    if config.use_subscript:
        base_str = str(base)
        tc.assertEqual(result.rfind(base_str) + len(base_str), len(result))


"""
Test Strip.
"""

@forall(number = domains.List(domains.Int(min_value = 0, max_value = 9),min_len = 1, max_len = 3),n_samples = 2)
@forall(config = build_strip_config(),n_samples = 2)
@forall(relation = build_relation(),n_samples = 2)
@forall(base = build_base(16),n_samples = 2)
def test_xform(number, config, relation, base):
    """
    Confirm that option strip strips more than other options.
    """
    result = Strip(config, base).xform(number, relation)
    most = Strip(StripConfig(strip=True), base).xform(number, relation)

    tc.assertTrue(len(most) <= len(result))

    if config.strip and number != []:
        tc.assertTrue(result[-1] != 0)
