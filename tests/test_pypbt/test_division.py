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

""" Test for integer conversions. """

# isort: STDLIB
import fractions
import unittest
from os import sys

# isort: THIRDPARTY
from pypbt.quantifiers import forall
from pypbt import domains

# isort: LOCAL
from justbases import NatDivision, Nats, RoundingMethods


@forall(n = domains.Int(min_value = 2, max_value = 17),n_samples = 25)
@forall(tupla = lambda n: domains.Tuple(domains.List(domains.Int(min_value = 1,max_value = n-1),min_len = 1,max_len=4),domains.List(domains.Int(max_value = n-1),max_len=4),n),n_samples=20)
def test_inverses_relation(n,tupla):
    """
    Test that division and undivision are inverses.
    """
    (divisor, dividend, base) = tupla
    (
        integer_part,
        non_repeating_part,
        repeating_part,
        relation,
    ) = NatDivision.division(divisor, dividend, base)
    return relation == 0

@forall(n = domains.Int(min_value = 2, max_value = 17),n_samples = 25)
@forall(tupla = lambda n: domains.Tuple(domains.List(domains.Int(min_value = 1,max_value = n-1),min_len = 1,max_len=4),domains.List(domains.Int(max_value = n-1),max_len=4),n),n_samples=20)
def test_inverses_numerator1(n,tupla):
    """
    Test that division and undivision are inverses.
    """
    (divisor, dividend, base) = tupla
    (
        integer_part,
        non_repeating_part,
        repeating_part,
        relation,
    ) = NatDivision.division(divisor, dividend, base)

    (denominator, numerator) = NatDivision.undivision(
        integer_part, non_repeating_part, repeating_part, base)

    return numerator == [] or numerator[0] != 0

@forall(n = domains.Int(min_value = 2, max_value = 17),n_samples = 25)
@forall(tupla = lambda n: domains.Tuple(domains.List(domains.Int(min_value = 1,max_value = n-1),min_len = 1,max_len=4),domains.List(domains.Int(max_value = n-1),max_len=4),n),n_samples=20)
def test_inverses_empty_denominator(n,tupla):
    """
    Test that division and undivision are inverses.
    """
    (divisor, dividend, base) = tupla
    (
        integer_part,
        non_repeating_part,
        repeating_part,
        relation,
    ) = NatDivision.division(divisor, dividend, base)

    (denominator, numerator) = NatDivision.undivision(
        integer_part, non_repeating_part, repeating_part, base)
    
    return denominator != []

@forall(n = domains.Int(min_value = 2, max_value = 17),n_samples = 25)
@forall(tupla = lambda n: domains.Tuple(domains.List(domains.Int(min_value = 1,max_value = n-1),min_len = 1,max_len=4),domains.List(domains.Int(max_value = n-1),max_len=4),n),n_samples=20)
def test_inverses_zero_denominator(n,tupla):
    """
    Test that division and undivision are inverses.
    """
    (divisor, dividend, base) = tupla
    (
        integer_part,
        non_repeating_part,
        repeating_part,
        relation,
    ) = NatDivision.division(divisor, dividend, base)

    (denominator, numerator) = NatDivision.undivision(
        integer_part, non_repeating_part, repeating_part, base)

    return denominator[0] != 0

@forall(n = domains.Int(min_value = 2, max_value = 17),n_samples = 25)
@forall(tupla = lambda n: domains.Tuple(domains.List(domains.Int(min_value = 1,max_value = n-1),min_len = 1,max_len=4),domains.List(domains.Int(max_value = n-1),max_len=4),n),n_samples=20)
def test_inverses(n,tupla):
    """
    Test that division and undivision are inverses.
    """
    (divisor, dividend, base) = tupla
    (
        integer_part,
        non_repeating_part,
        repeating_part,
        relation,
    ) = NatDivision.division(divisor, dividend, base)

    (denominator, numerator) = NatDivision.undivision(
        integer_part, non_repeating_part, repeating_part, base)

    original = fractions.Fraction(
        Nats.convert_to_int(dividend, base), Nats.convert_to_int(divisor, base)
    )
    result = fractions.Fraction(
        Nats.convert_to_int(numerator, base), Nats.convert_to_int(denominator, base)
    )

    return original == result

@forall(n = domains.Int(min_value = 2, max_value = 17),n_samples = 25)
@forall(tupla = lambda n: domains.Tuple(domains.List(domains.Int(min_value = 1,max_value = n-1),min_len = 1,max_len=4),domains.List(domains.Int(max_value = n-1),max_len=4),n),
        precision =domains.Int(min_value = 0, max_value = 32),n_samples=20)
def test_truncation(n,tupla, precision):
    """
    Test just truncating division result to some precision.

    Integer parts of truncated and non-truncated are always the same.

    The length of repeating and non-repeating is always less than the
    precision.

    If precision limit was reached before repeating portion was
    calculated, then the non-repeating portion has ``precision`` digits
    and is a prefix of non-repeating-part + repeating part when
    precision is not bounded.
    """
    (divisor, dividend, base) = tupla
    (integer_part, non_repeating_part, repeating_part, rel) = NatDivision.division(
        divisor, dividend, base, precision
    )
    (
        integer_part_2,
        non_repeating_part_2,
        repeating_part_2,
        rel_2,
    ) = NatDivision.division(divisor, dividend, base, None)

    if rel_2 != 0:
        return False
    if integer_part != integer_part_2:
        return False
    if len(repeating_part) + len(non_repeating_part) > precision:
        return False
    if repeating_part_2 != repeating_part and rel != -1 :
        return False

    return not (repeating_part_2 != [] and repeating_part == []) or (
        len(non_repeating_part) == precision
        and non_repeating_part
        == (non_repeating_part_2 + repeating_part_2)[:precision])
    
@forall(divisor = domains.Int(min_value=1,max_value=2**16),
        dividend = domains.Int(min_value=0,max_value=2**64),
        base = domains.Int(min_value=3),
        precision = domains.Int(min_value=0,max_value=32),n_samples = 500)
def test_up_down(divisor, dividend, base, precision):
    """
    Test that rounding up and rounding down have the right relationship.
    """
    #pylint: disable=too-many-locals
    divisor = Nats.convert_from_int(divisor, base)
    dividend = Nats.convert_from_int(dividend, base)
    (integer_part, non_repeating_part, repeating_part, rel) = NatDivision.division(
        divisor, dividend, base, precision, RoundingMethods.ROUND_UP
    )
    (
        integer_part_2,
        non_repeating_part_2,
        repeating_part_2,
        rel_2,
    ) = NatDivision.division(
        divisor, dividend, base, precision, RoundingMethods.ROUND_DOWN
    )
    (
        integer_part_3,
        non_repeating_part_3,
        repeating_part_3,
        rel_3,
    ) = NatDivision.division(
        divisor, dividend, base, precision, RoundingMethods.ROUND_TO_ZERO
    )

    if integer_part_2 != integer_part_3:
        return False
    if non_repeating_part_2 != non_repeating_part_3:
        return False
    if repeating_part_2 != repeating_part_3:
        return False
    if repeating_part == [] and repeating_part_2 != []:
        return False
    
    if rel < rel_2:
        return False
    if rel_2 != rel_3:
        return False

    round_up_int = Nats.convert_to_int(integer_part + non_repeating_part, base)
    round_down_int = Nats.convert_to_int(
        integer_part_2 + non_repeating_part_2, base
    )

    if repeating_part == []:
        if round_up_int - round_down_int > 1 and round_up_int - round_down_int < 0:
            return False

    if rel == 0:
        if round_down_int != round_up_int:
            return False
        if rel_2 != 0:
            return False
        if rel_3 != 0:
            return False


    for method in RoundingMethods.CONDITIONAL_METHODS():
        (integer_part_c, non_repeating_part_c, _, rel) = NatDivision.division(
            divisor, dividend, base, precision, method
        )
        rounded_int = Nats.convert_to_int(
            integer_part_c + non_repeating_part_c, base
        )
        if repeating_part == []:
            if round_down_int > rounded_int:
                return False
            if rounded_int > round_up_int:
                return False
            if rel == 0:
                return round_up_int == round_down_int
            elif rel == -1:
                return rounded_int == round_down_int
            else:
                return rounded_int == round_up_int
        else: return True