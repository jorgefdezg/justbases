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
from justbases import Rationals, RoundingMethods, Radix

# isort considers this third party, but it is not
from _utils import build_base, build_radix # isort:skip
from pypbt.quantifiers import forall,exists
from pypbt import domains

@forall(base = build_base(16),n_samples = 20)
@forall(radix = lambda base: build_radix(base,3),n_samples = 25)
def test_in_base(base, radix):
    """
    Test that roundtrip is identity modulo number of 0s in
    non repeating part.
    """
    result = radix.in_base(base).in_base(radix.base)
    if result.sign != radix.sign:
        return False
    if result.integer_part != radix.integer_part:
        return False
    if result.repeating_part != radix.repeating_part:
        return False
    if result.base != radix.base:
        return False


    length = len(result.non_repeating_part)
    if result.non_repeating_part != radix.non_repeating_part[:length]:
        return False
    return all(x == 0 for x in radix.non_repeating_part[length:])


@forall(base = build_base(36),n_samples = 25)
@forall(radix = lambda base: build_radix(base,10),n_samples = 20)
def test_str(base,radix):
    
    #Check basic properties of __str__.
    
    result = str(radix)
    return result.startswith("-") == (radix.sign == -1)

@forall(base = build_base(1024),n_samples = 25)
@forall(radix = lambda base: build_radix(base,10),n_samples = 20)
def test_repr(base,radix):

    #Make sure that result is evalable.
    return eval(repr(radix)) == radix

# Tests for rounding Radixes

@forall(base = build_base(16),n_samples = 25)
@forall(radix = lambda base: build_radix(base,10),
        precision = domains.Int(min_value=0, max_value=64),
        method= domains.DomainFromIterable(RoundingMethods.METHODS(),True),n_samples = 20)
def test_round_fraction(base,radix, precision, method):

    # Test that rounding yields the correct number of digits.
    # Test that rounded values are in a good range.

    value = radix.as_rational()
    (result, relation) = radix.rounded(precision, method)
    if len(result.non_repeating_part) != precision:
        return False

    ulp = Fraction(1, radix.base**precision)
    rational_result = result.as_rational()
    if value - ulp > rational_result:
        return False
    if value + ulp < rational_result:
        return False

    if rational_result > value:
        return relation == 1
    elif rational_result < value:
        return relation == -1
    else:
        return relation == 0

@forall(base = build_base(16),n_samples = 25)
@forall(radix = lambda base: build_radix(base,10),
        precision = domains.Int(min_value=0, max_value=64),n_samples = 20)
def test_round_relation(base,radix, precision):

    #Test that all results have the correct relation.

    results = dict(
        (method, radix.rounded(precision, method)[0])
        for method in RoundingMethods.METHODS()
    )

    for _, result in results.items():
        if len(result.non_repeating_part) != precision:
            return False

    if radix.sign in (0, 1):
        if results[RoundingMethods.ROUND_DOWN] != results[RoundingMethods.ROUND_TO_ZERO]:
            return False
        
        if results[RoundingMethods.ROUND_HALF_DOWN] != results[RoundingMethods.ROUND_HALF_ZERO]:
            return False
    else:
        if results[RoundingMethods.ROUND_UP] != results[RoundingMethods.ROUND_TO_ZERO]:
            return False
        if results[RoundingMethods.ROUND_HALF_UP] != results[RoundingMethods.ROUND_HALF_ZERO]:
            return False

    order = [
        RoundingMethods.ROUND_UP,
        RoundingMethods.ROUND_HALF_UP,
        RoundingMethods.ROUND_HALF_DOWN,
        RoundingMethods.ROUND_DOWN,
    ]
    for index in range(len(order) - 1):
        if results[order[index]].as_rational() < results[order[index + 1]].as_rational():
            return False
    return True

@forall(base = build_base(64),n_samples = 25)
@forall(radix = lambda base: build_radix(base,5),
        method= domains.DomainFromIterable(RoundingMethods.METHODS(),True),n_samples = 20)
def test_as_int(base,radix, method):
    # Test equivalence with two paths.

    result1 = Rationals.round_to_int(radix.as_rational(), method)
    result2 = radix.as_int(method)
    return result1 == result2
