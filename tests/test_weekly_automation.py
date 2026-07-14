from __future__ import annotations

import argparse
import datetime as dt
import json
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

    def test_combined_api_bundle_supports_compact_provider_labels(self) -> None:
        variants = [
            "deepseek: deepseek-value, minimax: minimax-value",
            "DEEPSEEK_API_KEY=deepseek-value；MINIMAX_API_KEY：minimax-value",
            "ds: deepseek-value minimax-token=minimax-value",
        ]
        for bundle in variants:
            with self.subTest(bundle=bundle):
                parsed = auto.parse_api_bundle(bundle)
                self.assertEqual(parsed["DEEPSEEK_API_KEY"], "deepseek-value")
                self.assertEqual(parsed["MINIMAX_API_KEY"], "minimax-value")

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
            args = argparse.Namespace(
                days=30,
                limit_per_query=1,
                citation_limit=1,
                output=output,
                report=report,
                sleep=0.0,
            )
            with (
                mock.patch.object(auto, "load_keywords", return_value=["query"]),
                mock.patch.object(auto, "search_semantic_keyword", side_effect=RuntimeError("rate limited")),
                mock.patch.object(auto, "search_openalex_keyword", return_value=[record]),
                mock.patch.object(auto, "search_arxiv_keyword", return_value=[]),
                mock.patch.object(auto, "search_openalex_citations", return_value=[]),
            ):
                auto.cmd_weekly(args)

            candidates = yaml.safe_load(Path(output).read_text(encoding="utf-8"))
            report_json = yaml.safe_load(Path(report.replace(".md", ".json")).read_text(encoding="utf-8"))
            self.assertEqual(len(candidates), 1)
            self.assertEqual(report_json["search_stats"]["openalex"], 1)
            self.assertIn("rate limited", report_json["details"][0]["error"])

    def test_weekly_search_disables_rate_limited_source_for_remaining_keywords(self) -> None:
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
            args = argparse.Namespace(
                days=30,
                limit_per_query=1,
                citation_limit=1,
                output=output,
                report=report,
                sleep=0.0,
            )
            with (
                mock.patch.object(auto, "load_keywords", return_value=["query one", "query two"]),
                mock.patch.object(
                    auto, "search_semantic_keyword", side_effect=RuntimeError("429 rate limited")
                ) as semantic,
                mock.patch.object(auto, "search_openalex_keyword", return_value=[record]) as openalex,
                mock.patch.object(auto, "search_arxiv_keyword", return_value=[]) as arxiv,
                mock.patch.object(auto, "search_openalex_citations", return_value=[]),
            ):
                auto.cmd_weekly(args)

            self.assertEqual(semantic.call_count, 1)
            self.assertEqual(openalex.call_count, 2)
            self.assertEqual(arxiv.call_count, 2)
            report_json = json.loads(Path(report).with_suffix(".json").read_text(encoding="utf-8"))
            skipped = [
                row
                for row in report_json["details"]
                if row["source"] == "semantic_scholar" and row["query"] == "query two"
            ]
            self.assertEqual(len(skipped), 1)
            self.assertIn("skipped after", skipped[0]["error"])

    def test_openalex_citation_search_applies_recent_date_window(self) -> None:
        captured = {}

        def fake_request(url, *, params=None, **kwargs):
            captured.update(params or {})
            return {"results": [], "meta": {"next_cursor": None}}

        with (
            mock.patch.object(auto, "find_openalex_work_id_by_seed", return_value="W123"),
            mock.patch.object(auto, "request_json", side_effect=fake_request),
        ):
            auto.search_openalex_citations(
                {"dataset": "DenseUAV", "title": "seed"},
                10,
                start_date="2026-06-15",
                end_date="2026-07-14",
            )

        self.assertEqual(
            captured["filter"],
            "cites:W123,from_publication_date:2026-06-15,to_publication_date:2026-07-14",
        )
        self.assertEqual(captured["sort"], "publication_date:desc")

    def test_weekly_parser_defaults_to_broad_recent_citation_search(self) -> None:
        args = auto.build_parser().parse_args(["weekly"])
        self.assertEqual(args.days, 30)
        self.assertEqual(args.citation_limit, 100)

    def test_merge_updates_paper_introduction_pages_without_touching_leaderboards(self) -> None:
        record = {
            "id": "paper-1",
            "title": "A New UAV Cross-view Method",
            "year": 2026,
            "urls": {"paper": "https://example.org/paper", "code": "https://example.org/code"},
            "classification": {"main_category": "retrieval", "datasets": ["DenseUAV"]},
            "summary": {
                "summary_en": "Introduces a robust UAV-to-satellite retrieval method.",
                "benchmarks": ["DenseUAV"],
                "code_url": "https://example.org/code",
                "leaderboard_metrics": [
                    {
                        "dataset": "DenseUAV",
                        "metric": "R@1",
                        "value": "99.0",
                        "verified": False,
                    }
                ],
            },
            "status": "parsed",
            "verified": False,
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            candidate_path = root / "candidate.yml"
            candidate_path.write_text(yaml.safe_dump([record], sort_keys=False), encoding="utf-8")
            with mock.patch.object(auto, "ROOT", root):
                auto.cmd_merge(argparse.Namespace(candidates=str(candidate_path), require_verified=False))

            papers = yaml.safe_load((root / "data" / "papers.yml").read_text(encoding="utf-8"))
            page = (root / "papers" / "retrieval.md").read_text(encoding="utf-8")
            self.assertEqual([paper["title"] for paper in papers], [record["title"]])
            self.assertIn(record["title"], page)
            self.assertIn(record["summary"]["summary_en"], page)
            self.assertIn("DenseUAV", page)
            self.assertFalse((root / "data" / "leaderboards.csv").exists())
            self.assertFalse((root / "leaderboards").exists())


if __name__ == "__main__":
    unittest.main()
