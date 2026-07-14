from __future__ import annotations

import argparse
import datetime as dt
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import yaml

from scripts import uav_cvgl_auto as auto


class WeeklyAutomationTests(unittest.TestCase):
    def test_recent_filter_drops_known_old_records_but_keeps_unknown_dates(self) -> None:
        records = [
            {"title": "new", "publication_date": "2026-07-10", "year": 2026},
            {"title": "old", "publication_date": "2025-12-31", "year": 2025},
            {"title": "unknown", "publication_date": "", "year": 2026},
        ]
        result = auto.filter_records_by_date(records, "2026-07-01", "2026-07-14")
        self.assertEqual([row["title"] for row in result], ["new", "unknown"])

    def test_classification_limit_can_skip_cached_rows(self) -> None:
        cached = {
            "status": "parsed",
            "classification": {"main_category": "retrieval"},
            "summary": {"leaderboard_metrics": []},
        }
        raw = {"status": "raw"}
        self.assertFalse(auto.candidate_needs_processing(cached))
        self.assertTrue(auto.candidate_needs_processing(raw))

    def test_classification_limit_counts_unprocessed_papers_not_list_positions(self) -> None:
        records = [
            {
                "title": "cached",
                "status": "parsed",
                "classification": {"main_category": "retrieval"},
                "summary": {"leaderboard_metrics": []},
            },
            {"title": "new one", "status": "raw"},
            {"title": "new two", "status": "raw"},
        ]
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "candidates.yml"
            report_path = Path(temp_dir) / "classification.md"
            input_path.write_text(yaml.safe_dump(records), encoding="utf-8")
            args = argparse.Namespace(
                input=str(input_path),
                output="",
                mode="weekly",
                limit=1,
                skip_minimax=True,
                use_pdf=False,
                force_classification=False,
                force_summary=False,
                report=str(report_path),
                sleep=0.0,
            )
            classification = {
                "is_cvgl": False,
                "is_uav_related": False,
                "main_category": "unrelated",
                "relevance_score": 0.0,
            }
            with mock.patch.object(auto, "deepseek_classify", return_value=classification):
                auto.cmd_classify(args)

            result = yaml.safe_load(input_path.read_text(encoding="utf-8"))
            self.assertNotIn("classification", result[2])
            self.assertEqual(result[1]["classification"]["main_category"], "unrelated")

    def test_official_sues_and_gta_protocols_are_not_filtered_as_ablations(self) -> None:
        rows = [
            {
                "dataset": "SUES-200",
                "task": "Drone-to-Satellite",
                "split": "150m",
                "metric": "R@1",
                "method": "Main Method",
                "value": "98.0",
                "source": "official table",
                "notes": "official altitude protocol",
            },
            {
                "dataset": "GTA-UAV",
                "task": "retrieval",
                "split": "Cross-Area",
                "metric": "R@1",
                "method": "Main Method",
                "value": "61.2",
                "source": "official table",
                "notes": "main result",
            },
            {
                "dataset": "GTA-UAV",
                "task": "retrieval",
                "split": "Cross-Area",
                "metric": "R@1",
                "method": "without module",
                "value": "55.0",
                "source": "ablation table",
                "notes": "ablation",
            },
        ]
        result = auto.filter_leaderboard_metrics(rows, ["SUES-200", "GTA-UAV"])
        self.assertEqual(len(result), 2)
        self.assertEqual({row["dataset"] for row in result}, {"SUES-200", "GTA-UAV"})
        self.assertTrue(all(row["verified"] is False for row in result))

    def test_weekly_digest_only_contains_first_seen_records_from_target_week(self) -> None:
        records = [
            {"title": "this week", "status": "parsed", "discovery": {"found_date": "2026-07-13"}},
            {"title": "last week", "status": "parsed", "discovery": {"found_date": "2026-07-05"}},
            {"title": "rejected", "status": "rejected", "discovery": {"found_date": "2026-07-13"}},
        ]
        result = auto.weekly_digest_records(records, dt.date(2026, 7, 14))
        self.assertEqual([row["title"] for row in result], ["this week"])

    def test_empty_actions_vars_do_not_override_model_defaults(self) -> None:
        with mock.patch.dict(
            os.environ,
            {
                "DEEPSEEK_API_KEY": "test-deepseek-key",
                "MINIMAX_API_KEY": "test-minimax-key",
                "DEEPSEEK_MODEL": "",
                "MINIMAX_MODEL": "",
                "MINIMAX_BASE_URL": "",
            },
            clear=False,
        ):
            self.assertEqual(auto.env_value("DEEPSEEK_MODEL", "deepseek-chat"), "deepseek-chat")
            self.assertEqual(auto.env_value("MINIMAX_MODEL", "MiniMax-M3"), "MiniMax-M3")
            auto.cmd_preflight(argparse.Namespace(require_llm=True))

    def test_preflight_reports_missing_required_secrets_without_api_calls(self) -> None:
        with mock.patch.dict(
            os.environ,
            {
                "API": "",
                "API_BUNDLE": "",
                "DEEPSEEK_API_KEY": "",
                "MINIMAX_API_KEY": "",
                "MINIMAX_MODEL": "",
            },
            clear=False,
        ):
            with self.assertRaisesRegex(RuntimeError, "DEEPSEEK_API_KEY, MINIMAX_API_KEY"):
                auto.cmd_preflight(argparse.Namespace(require_llm=True))

    def test_combined_api_bundle_supports_json_and_provider_aliases(self) -> None:
        with mock.patch.dict(
            os.environ,
            {
                "API_BUNDLE": '{"deepseek": "ds:test-deepseek", "minimax": "test-minimax"}',
                "DEEPSEEK_API_KEY": "",
                "MINIMAX_API_KEY": "",
                "MINIMAX_MODEL": "",
            },
            clear=False,
        ):
            self.assertEqual(auto.api_secret_value("DEEPSEEK_API_KEY"), "ds:test-deepseek")
            self.assertEqual(auto.api_secret_value("MINIMAX_API_KEY"), "test-minimax")
            auto.cmd_preflight(argparse.Namespace(require_llm=True))

    def test_combined_api_bundle_supports_dotenv_and_direct_override(self) -> None:
        bundle = "DEEPSEEK_API_KEY=from-bundle\nMINIMAX_API_KEY='minimax-bundle'"
        with mock.patch.dict(
            os.environ,
            {
                "API_BUNDLE": bundle,
                "DEEPSEEK_API_KEY": "direct-deepseek",
                "MINIMAX_API_KEY": "",
            },
            clear=False,
        ):
            self.assertEqual(auto.api_secret_value("DEEPSEEK_API_KEY"), "direct-deepseek")
            self.assertEqual(auto.api_secret_value("MINIMAX_API_KEY"), "minimax-bundle")

    def test_weekly_search_isolates_one_source_failure(self) -> None:
        today = dt.date.today().isoformat()
        record = {
            "id": "new-paper",
            "title": "New UAV Paper",
            "year": dt.date.today().year,
            "publication_date": today,
            "source": {"doi": "10.1000/test"},
            "discovery": {"found_date": today, "found_by": [{"source": "openalex"}]},
            "status": "raw",
            "verified": False,
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            output = str(Path(temp_dir) / "weekly.yml")
            report = str(Path(temp_dir) / "weekly_report.md")
            args = argparse.Namespace(days=14, limit_per_query=1, output=output, report=report, sleep=0.0)
            with (
                mock.patch.object(auto, "load_keywords", return_value=["query"]),
                mock.patch.object(auto, "search_semantic_keyword", side_effect=RuntimeError("rate limited")),
                mock.patch.object(auto, "search_openalex_keyword", return_value=[record]),
                mock.patch.object(auto, "search_arxiv_keyword", return_value=[]),
            ):
                auto.cmd_weekly(args)

            candidates = yaml.safe_load(Path(output).read_text(encoding="utf-8"))
            report_json = yaml.safe_load(Path(report.replace(".md", ".json")).read_text(encoding="utf-8"))
            self.assertEqual(len(candidates), 1)
            self.assertEqual(report_json["search_stats"]["openalex"], 1)
            self.assertIn("rate limited", report_json["details"][0]["error"])


if __name__ == "__main__":
    unittest.main()
