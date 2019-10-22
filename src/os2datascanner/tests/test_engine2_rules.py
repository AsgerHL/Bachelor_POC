import unittest

from os2datascanner.engine2.rules.cpr import CPRRule
from os2datascanner.engine2.rules.regex import RegexRule
from os2datascanner.engine2.rules.logical import OrRule, AndRule, NotRule


class RuleTests(unittest.TestCase):
    def test_simplerule_matches(self):
        candidates = [
            (
                CPRRule(ignore_irrelevant=False),
                """
2205995008: forbryder,
230500 0003: forbryder,
240501-0006: forbryder""",
                [
                    "2205XXXXXX",
                    "2305XXXXXX",
                    "2405XXXXXX"
                ]
            ),
            (
                CPRRule(ignore_irrelevant=True),
                """
2205995008: forbryder,
230500 0003: forbryder,
240501-0006: forbryder""",
                [
                    "2305XXXXXX",
                    "2405XXXXXX"
                ]
            ),
            (
                RegexRule("((four|six)( [aopt]+)?|(one|seven) [aopt]+)"),
                """
one
one potato
two potato
three potato
four
five potato
six potato
seven potato
more!""",
                [
                    "one potato",
                    "four",
                    "six potato",
                    "seven potato"
                ]
            )
        ]

        for rule, input_string, expected in candidates:
            with self.subTest(rule):
                matches = rule.match(input_string)
                self.assertEqual(
                        [match["match"] for match in matches], expected)

    compound_candidates = [
        (
            AndRule(
                RegexRule("A"),
                OrRule(
                    RegexRule("B"),
                    RegexRule("C")
                )
            ), [
                ("A", False, 3),
                ("AB", True, 2),
                ("ABC", True, 2),
                ("BC", False, 1),
                ("AC", True, 3)
            ]
        ),
        (
            NotRule(
                AndRule(
                    RegexRule("A"),
                    OrRule(
                        RegexRule("B"),
                        RegexRule("C")
                    )
                )
            ), [
                ("A", True, 3),
                ("AB", False, 2),
                ("ABC", False, 2),
                ("BC", True, 1),
                ("AC", False, 3)
            ]
        )
    ]

    def test_compound_rule_matches(self):
        for rule, tests in RuleTests.compound_candidates:
            for input_string, outcome, evaluation_count in tests:
                now = rule
                evaluations = 0

                while True:
                    print(now)
                    head, pve, nve = now.split()
                    evaluations += 1
                    print(head)
                    match = list(head.match(input_string))
                    print(match)
                    if match:
                        now = pve
                    else:
                        now = nve
                    if isinstance(now, bool):
                        break
                print(input_string, now, outcome)
                self.assertEqual(
                        outcome,
                        now,
                        "{0}: wrong result".format(input_string))
                self.assertEqual(
                        evaluation_count,
                        evaluations,
                        "{0}: wrong evaluation count".format(input_string))

    def test_json_round_trip(self):
        for rule, _ in RuleTests.compound_candidates:
            with self.subTest(rule):
                json = rule.to_json_object()
                back_again = rule.from_json_object(json)
                print(rule)
                print(json)
                print(back_again)
                self.assertEqual(rule, back_again)
                print("--")
