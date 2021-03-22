import json

from django.test import TestCase

from os2datascanner.utils.system_utilities import parse_isoformat_timestamp
from os2datascanner.engine2.model.file import (
        FilesystemHandle, FilesystemSource)
from os2datascanner.engine2.rules.regex import RegexRule
from os2datascanner.engine2.rules.dimensions import DimensionsRule
from os2datascanner.engine2.rules.logical import AndRule
from os2datascanner.engine2.rules.last_modified import LastModifiedRule
from os2datascanner.engine2.pipeline import messages
from os2datascanner.engine2.rules.rule import Sensitivity

from ..reportapp.models.documentreport_model import DocumentReport
from ..reportapp.management.commands import pipeline_collector


time0 = "2020-10-28T13:51:49+01:00"
time1 = "2020-10-28T14:21:27+01:00"
time2 = "2020-10-28T14:36:20+01:00"
scan_tag0 = messages.ScanTagFragment(
    scanner=messages.ScannerFragment(
            pk=22, name="Dummy test scanner"),
    time=parse_isoformat_timestamp(time0),
    user=None, organisation=None)
scan_tag1 = messages.ScanTagFragment(
    scanner=messages.ScannerFragment(
            pk=22, name="Dummy test scanner"),
    time=parse_isoformat_timestamp(time1),
    user=None, organisation=None)
scan_tag2 = messages.ScanTagFragment(
    scanner=messages.ScannerFragment(
            pk=22, name="Dummy test scanner"),
    time=parse_isoformat_timestamp(time2), user=None, organisation=None)

common_handle = FilesystemHandle(
        FilesystemSource("/mnt/fs01.magenta.dk/brugere/af"),
        "OS2datascanner/Dokumenter/Verdensherredømme - plan.txt")
common_rule = RegexRule("Vores hemmelige adgangskode er",
                        sensitivity=Sensitivity.WARNING)
dimension_rule = DimensionsRule()


common_scan_spec = messages.ScanSpecMessage(
        scan_tag=None, # placeholder
        source=common_handle.source,
        rule=common_rule,
        configuration={},
        progress=None)

positive_match = messages.MatchesMessage(
        scan_spec=common_scan_spec._replace(scan_tag=scan_tag0),
        handle=common_handle,
        matched=True,
        matches=[
            messages.MatchFragment(
                rule=common_rule,
                matches=[{"dummy": "match object"}])
        ])

positive_match_with_dimension_rule_probability_and_sensitivity = messages.MatchesMessage(
        scan_spec=common_scan_spec._replace(scan_tag=scan_tag0),
        handle=common_handle,
        matched=True,
        matches=[
            messages.MatchFragment(
                rule=common_rule,
                matches=[{"dummy": "match object",
                          "probability": 0.6, "sensitivity": 750},
                         {"dummy1": "match object",
                          "probability": 0.0, "sensitivity": 1000},
                         {"dummy2": "match object",
                          "probability": 1.0, "sensitivity": 500}]),
            messages.MatchFragment(
                rule=dimension_rule,
                matches=[{"match": [2496, 3508]}])
        ])

negative_match = messages.MatchesMessage(
        scan_spec=common_scan_spec._replace(
            scan_tag=scan_tag1),
        handle=common_handle,
        matched=False,
        matches=[messages.MatchFragment(
                rule=common_rule,
                matches=[])
        ])

deletion = messages.ProblemMessage(
        scan_tag=scan_tag1,
        source=None,
        handle=common_handle,
        message="There was a file here. It's gone now.",
        missing=True)

transient_handle_error = messages.ProblemMessage(
        scan_tag=scan_tag1,
        source=None,
        handle=common_handle,
        message="Bad command or file name")

transient_source_error = messages.ProblemMessage(
        scan_tag=scan_tag1,
        source=common_handle.source,
        handle=None,
        message="Not ready reading drive A: [A]bort, [R]etry, [F]ail?")

late_rule = LastModifiedRule(parse_isoformat_timestamp(time2))
late_negative_match = messages.MatchesMessage(
        scan_spec=common_scan_spec._replace(
                scan_tag=scan_tag2,
                rule=AndRule(
                        late_rule,
                        common_rule)),
        handle=common_handle,
        matched=False,
        matches=[messages.MatchFragment(
                rule=late_rule,
                matches=[])])


class PipelineCollectorTests(TestCase):
    def test_rejection(self):
        """Failed match messages shouldn't be stored in the database."""
        prev, new = pipeline_collector.get_reports_for(
                negative_match.handle.to_json_object(),
                negative_match.scan_spec.scan_tag)
        pipeline_collector.handle_match_message(
                prev, new, negative_match.to_json_object())
        self.assertEqual(
                new.pk,
                None,
                "negative match was saved anyway")

    def test_acceptance(self):
        """Successful match messages should be stored in the database."""
        prev, new = pipeline_collector.get_reports_for(
                positive_match.handle.to_json_object(),
                positive_match.scan_spec.scan_tag)
        pipeline_collector.handle_match_message(
                prev, new, positive_match.to_json_object())
        self.assertNotEqual(
                new.pk,
                None,
                "positive match was not saved")
        self.assertEqual(
                new.resolution_status,
                None,
                "fresh match was already resolved")
        self.assertEqual(
                new.scan_time,
                positive_match.scan_spec.scan_tag.time,
                "match time was not taken from scan specification")
        self.assertEqual(
                new.source_type,
                common_handle.source.type_label,
                "type label was not extracted to database")
        return new

    def test_edit(self):
        """Removing matches from a file should update the status of the
        previous match message."""
        saved_match = self.test_acceptance()
        self.test_rejection()
        saved_match.refresh_from_db()
        self.assertEqual(
                saved_match.resolution_status,
                DocumentReport.ResolutionChoices.EDITED.value,
                "resolution status not correctly updated")

    def test_removal(self):
        """Deleting a file should update the status of the previous match
        message."""
        saved_match = self.test_acceptance()

        prev, new = pipeline_collector.get_reports_for(
                deletion.handle.to_json_object(),
                deletion.scan_tag)
        pipeline_collector.handle_problem_message(
                prev, new, deletion.to_json_object())

        saved_match.refresh_from_db()
        self.assertEqual(
                saved_match.resolution_status,
                DocumentReport.ResolutionChoices.REMOVED.value,
                "resolution status not correctly updated")

    def test_transient_handle_errors(self):
        """Source types should be correctly extracted from Handle errors."""
        prev, new = pipeline_collector.get_reports_for(
                transient_handle_error.handle.to_json_object(),
                transient_handle_error.scan_tag)
        pipeline_collector.handle_problem_message(
                prev, new, transient_handle_error.to_json_object())

        self.assertEqual(
                new.source_type,
                transient_handle_error.handle.source.type_label,
                "type label was not extracted to database")

    def test_transient_source_errors(self):
        """Source types should be correctly extracted from Source errors."""
        prev, new = pipeline_collector.get_reports_for(
                transient_source_error.source.to_json_object(),
                transient_source_error.scan_tag)
        pipeline_collector.handle_problem_message(
                prev, new, transient_source_error.to_json_object())

        self.assertEqual(
                new.source_type,
                transient_source_error.source.type_label,
                "type label was not extracted to database")

    def test_recycler(self):
        """Receiving a failed match message which failed because of the
        Last-Modified check should update the timestamp of the previous match
        message, but should not create a new database object."""
        saved_match = self.test_acceptance()

        prev, new = pipeline_collector.get_reports_for(
                late_negative_match.handle.to_json_object(),
                late_negative_match.scan_spec.scan_tag)
        pipeline_collector.handle_match_message(
                prev, new, late_negative_match.to_json_object())

        self.assertEqual(
                new.pk,
                None,
                "negative match was saved anyway")
        saved_match.refresh_from_db()
        self.assertEqual(
                saved_match.scan_time,
                parse_isoformat_timestamp(time2),
                "match timestamp not correctly updated")

    def test_filter_internal_rules_matches(self):
        match_to_match = messages.MatchesMessage(
            scan_spec=common_scan_spec._replace(scan_tag=scan_tag0),
            handle=common_handle,
            matched=True,
            matches=[
                messages.MatchFragment(
                    rule=common_rule,
                    matches=[{"dummy2": "match object",
                              "probability": 1.0, "sensitivity": 500},
                             {"dummy": "match object",
                              "probability": 0.6, "sensitivity": 750},
                             {"dummy1": "match object",
                              "probability": 0.0, "sensitivity": 1000}]),
                messages.MatchFragment(
                    rule=dimension_rule,
                    matches=[{"match": [2496, 3508]}])
            ])

        self.assertEqual(pipeline_collector.sort_matches_by_probability(
            positive_match_with_dimension_rule_probability_and_sensitivity.to_json_object()
        )["matches"], match_to_match.to_json_object()["matches"])
