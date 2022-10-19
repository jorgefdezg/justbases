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

# isort: THIRDPARTY
from pypbt.quantifiers import forall,exists
from pypbt import domains
# isort: LOCAL
from justbases import Radices, Rationals, RoundingMethods

# if sys.gettrace() is not None:
#     settings.load_profile("tracing")


"""Tests for rationals."""

@forall(fraction = domains.DomainPyObject(Fraction, numerator = domains.Int(), denominator = domains.Int(min_value = 1,max_value = 100)),
        to_base = domains.Int(min_value=2),n_samples = 500)
def test_inverses(fraction, to_base):

    #Test that functions are inverses of each other.

    (result, relation) = Radices.from_rational(fraction, to_base)
    return (relation == 0 and
            result.as_rational() == fraction and
            result.sign in (0, 1) or value < 0)

@forall(fraction = domains.DomainPyObject(Fraction, numerator = domains.Int(), denominator = domains.Int(min_value = 1,max_value = 100)),
        base = domains.Int(min_value=2, max_value=64),
        precision = domains.Int(min_value=0, max_value=64),
        method= domains.DomainFromIterable(RoundingMethods.METHODS(),True),n_samples = 500)
def test_rounding_conversion(fraction, base, precision, method):
    
    #Test that converting and then rounding is the same as converting
    #with rounding.
    
    (rounded, rel) = Radices.from_rational(fraction, base, precision, method)
    (unrounded, urel) = Radices.from_rational(fraction, base)

    (frounded, frel) = unrounded.rounded(precision, method)
    rounded_value = rounded.as_rational()

    if rounded_value > fraction:
        return (urel == 0 and
                frounded == rounded and
                rel == frel and
                rel == 1)
    elif rounded_value < fraction:
        return (urel == 0 and
                frounded == rounded and
                rel == frel and
                rel == -1)
    else:
        return (urel == 0 and
                frounded == rounded and
                rel == frel and
                rel == 0)


@forall(fraction = domains.DomainPyObject(Fraction, numerator = domains.Int(), denominator = domains.Int(min_value = 1,max_value = 100)),
        method= domains.DomainFromIterable(RoundingMethods.METHODS(),True),n_samples = 500)
def test_rounding(fraction, method):
    
    #Test rounding to int.
    
    (result, _) = Rationals.round_to_int(fraction, method)
    (lower, upper) = (result - 1, result + 1)

    return (type(result) == int and
            (lower <= fraction <= result) or (result <= fraction <= upper))

@forall(numerator = domains.Int(min_value=1, max_value=9),n_samples = 500)
def test_rounding_precise(numerator):
    
    #Test with predicted value.
    
    #pylint: disable=too-many-statements
    value = Fraction(numerator, 10)
    (result, rel) = Rationals.round_to_int(value, RoundingMethods.ROUND_DOWN)
    if result != 0 or rel != -1:
        return False

    (result, rel) = Rationals.round_to_int(-value, RoundingMethods.ROUND_DOWN)
    if result != -1 or rel != -1:
        return False

    (result, rel) = Rationals.round_to_int(value, RoundingMethods.ROUND_UP)
    if result != 1 or rel != 1:
        return False

    (result, rel) = Rationals.round_to_int(-value, RoundingMethods.ROUND_UP)
    if result != 0 or rel != 1:
        return False

    (result, rel) = Rationals.round_to_int(value, RoundingMethods.ROUND_TO_ZERO)
    if result != 0 or rel != -1:
        return False

    (result, rel) = Rationals.round_to_int(-value, RoundingMethods.ROUND_TO_ZERO)
    if result != 0 or rel != 1:
        return False

    (result, rel) = Rationals.round_to_int(value, RoundingMethods.ROUND_HALF_UP)
    if numerator < 5:
        if result != 0 or rel != -1:
            return False
    else:
        if result != 1 or rel != 1:
            return False

    (result, rel) = Rationals.round_to_int(-value, RoundingMethods.ROUND_HALF_UP)
    if numerator <= 5:
        if result != 0 or rel != 1:
            return False
    else:
        if result != -1 or rel != -1:
            return False

    (result, rel) = Rationals.round_to_int(value, RoundingMethods.ROUND_HALF_DOWN)
    if numerator > 5:
        if result != 1 or rel != 1:
            return False
    else:
        if result != 0 or rel != -1:
            return False

    (result, rel) = Rationals.round_to_int(-value, RoundingMethods.ROUND_HALF_DOWN)
    if numerator >= 5:
        if result != -1 or rel != -1:
            return False
    else:
        if result != 0 or rel != 1:
            return False

    (result, rel) = Rationals.round_to_int(value, RoundingMethods.ROUND_HALF_ZERO)
    if numerator > 5:
        if result != 1 or rel != 1:
            return False

    else:
        if result != 0 or rel != -1:
            return False

    (result, rel) = Rationals.round_to_int(-value, RoundingMethods.ROUND_HALF_ZERO)
    if numerator > 5:
        return(
            result == -1 and
            rel == -1
        )

    else:
        return (
            result == 0 and
            rel == 1
        )