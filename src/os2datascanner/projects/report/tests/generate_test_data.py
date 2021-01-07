import string
import random
from randomtimestamp import randomtimestamp

from os2datascanner.engine2.rules.rule import Sensitivity
from os2datascanner.engine2.rules.regex import RegexRule
from os2datascanner.engine2.rules.dimensions import DimensionsRule
from os2datascanner.engine2.pipeline import messages
from os2datascanner.engine2.model.file import (
        FilesystemHandle, FilesystemSource)


def get_different_scan_tag():
    return {
        "scanner": "Dummy test scanner {0}".format(
            str(random.randint(0, 10))
        ),
        "time": randomtimestamp(start_year=2020)
    }


def get_different_filesystemhandle(file_ending, folder_level):
    path = '/'
    for x in range(0, folder_level):
        path += ''.join(random.choice(
            string.ascii_lowercase) for i in range(10)) + '/'
    return FilesystemHandle(
        FilesystemSource("/mnt/fs01.magenta.dk/brugere/af"),
        "{0}{1}{2}".format(path, random.choice(
            string.ascii_lowercase), file_ending)
    )


def get_regex_rule(regex, sensitivity):
    return RegexRule(regex,
                     sensitivity=sensitivity)


def get_common_scan_spec():
    return messages.ScanSpecMessage(
        scan_tag=get_different_scan_tag(),
        source=get_different_filesystemhandle('.txt', 3).source,
        rule=get_regex_rule("Vores hemmelige adgangskode er",
                            Sensitivity.WARNING),
        configuration={},
        progress=None)


def get_positive_match_with_probability_and_sensitivity():
    return messages.MatchesMessage(
        scan_spec=get_common_scan_spec(),
        handle=get_different_filesystemhandle('.txt', 3),
        matched=True,
        matches=[
            get_matches_with_sensitivity_and_probability(),
            get_dimension_rule_match()
        ])


def get_matches_with_sensitivity_and_probability():
    return messages.MatchFragment(
        rule=get_regex_rule("Vores hemmelige adgangskode er",
                            Sensitivity.CRITICAL),
        matches=[{"dummy": "match object",
                  "probability": 0.6, "sensitivity": 750},
                 {"dummy1": "match object",
                  "probability": 0.0, "sensitivity": 1000},
                 {"dummy2": "match object",
                  "probability": 1.0, "sensitivity": 500}])


def get_dimension_rule_match():
    return messages.MatchFragment(
        rule=DimensionsRule(),
        matches=[{"match": [2496, 3508]}])
