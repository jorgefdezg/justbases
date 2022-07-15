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

""" Test for rational conversions. """

# isort: STDLIB
import unittest
from fractions import Fraction
from os import sys
import random
# isort: THIRDPARTY

# isort: LOCAL
from justbases import Rationals, RoundingMethods

# isort considers this third party, but it is not
from _utils import RadixDomain, build_base  # isort:skip
from pypbt.quantifier import forall,exists
from pypbt import domain

tc = unittest.TestCase()
@forall(radix = RadixDomain(16,3),n_samples = 5)
@forall(base = build_base(16),n_samples = 5)
def test_in_base(radix, base):
    """
    Test that roundtrip is identity modulo number of 0s in
    non repeating part.
    """
    result = radix.in_base(base).in_base(radix.base)
    tc.assertEqual(result.sign, radix.sign)
    tc.assertEqual(result.integer_part, radix.integer_part)
    tc.assertEqual(result.repeating_part, radix.repeating_part)
    tc.assertEqual(result.base, radix.base)

    length = len(result.non_repeating_part)
    tc.assertEqual(result.non_repeating_part, radix.non_repeating_part[:length])
    tc.assertTrue(all(x == 0 for x in radix.non_repeating_part[length:]))


@forall(radix = RadixDomain(36,10),n_samples = 10)
def test_str(radix):
    
    #Check basic properties of __str__.
    
    result = str(radix)
    tc.assertEqual(result.startswith("-"), (radix.sign == -1))

@forall(radix = RadixDomain(1024,10),n_samples= 10)
def test_repr(radix):

    #Make sure that result is evalable.

    # pylint: disable=import-outside-toplevel, unused-import
    # isort: LOCAL
    tc.assertEqual(eval(repr(radix)), radix)# pylint: disable=eval-used

#Tests for rounding Radixes

@forall(radix = RadixDomain(16,10),n_samples = 2)
@forall(precision = domain.Int(min_value=0, max_value=64))
@exists(method= domain.domain(RoundingMethods.METHODS(), finite= True))
def test_round_fraction(radix, precision, method):

    #Test that rounding yields the correct number of digits.
    #Test that rounded values are in a good range.

    value = radix.as_rational()
    (result, relation) = radix.rounded(precision, method)
    tc.assertEqual(len(result.non_repeating_part), precision)

    ulp = Fraction(1, radix.base**precision)
    rational_result = result.as_rational()
    tc.assertLessEqual(value - ulp, rational_result)
    tc.assertGreaterEqual(value + ulp, rational_result)

    if rational_result > value:
        tc.assertEqual(relation, 1)
    elif rational_result < value:
        tc.assertEqual(relation, -1)
    else:
        tc.assertEqual(relation, 0)

@forall(radix = RadixDomain(16,10),n_samples = 2)
@forall(precision = domain.Int(min_value=0, max_value=64))
def test_round_relation(radix, precision):

    #Test that all results have the correct relation.

    results = dict(
        (method, radix.rounded(precision, method)[0])
        for method in RoundingMethods.METHODS()
    )

    for _, result in results.items():
        tc.assertEqual(len(result.non_repeating_part), precision)

    if radix.sign in (0, 1):
        tc.assertEqual(
            results[RoundingMethods.ROUND_DOWN],
            results[RoundingMethods.ROUND_TO_ZERO],
        )
        tc.assertEqual(
            results[RoundingMethods.ROUND_HALF_DOWN],
            results[RoundingMethods.ROUND_HALF_ZERO],
        )
    else:
        tc.assertEqual(
            results[RoundingMethods.ROUND_UP],
            results[RoundingMethods.ROUND_TO_ZERO],
        )
        tc.assertEqual(
            results[RoundingMethods.ROUND_HALF_UP],
            results[RoundingMethods.ROUND_HALF_ZERO],
        )

    order = [
        RoundingMethods.ROUND_UP,
        RoundingMethods.ROUND_HALF_UP,
        RoundingMethods.ROUND_HALF_DOWN,
        RoundingMethods.ROUND_DOWN,
    ]
    for index in range(len(order) - 1):
        tc.assertGreaterEqual(
            results[order[index]].as_rational(),
            results[order[index + 1]].as_rational(),
        )
@forall(radix = RadixDomain(16,10),n_samples = 2)
@exists(method= domain.domain(RoundingMethods.METHODS(), finite= True))
def test_as_int(tc, radix, method):
    #Test equivalence with two paths.

    result1 = Rationals.round_to_int(radix.as_rational(), method)
    result2 = radix.as_int(method)
    tc.assertEqual(result1, result2)
