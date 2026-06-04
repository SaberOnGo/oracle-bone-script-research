import unittest
import csv

from tools.validation.check_repository_skeleton import (
    check_bilingual_markers,
    check_file_size_limits,
    check_forbidden_policy_text,
    check_forbidden_paths,
    check_forbidden_top_level_dirs,
    check_required_paths,
    check_root_gitignore_patterns,
    check_source_registers,
    check_tracked_temp_artifacts,
    repo_root,
)


class RepositorySkeletonTests(unittest.TestCase):
    def test_required_paths_exist(self) -> None:
        self.assertEqual(check_required_paths(repo_root()), [])

    def test_bilingual_markers_exist(self) -> None:
        self.assertEqual(check_bilingual_markers(repo_root()), [])

    def test_forbidden_path_patterns_absent(self) -> None:
        self.assertEqual(check_forbidden_paths(repo_root()), [])

    def test_forbidden_top_level_dirs_absent(self) -> None:
        self.assertEqual(check_forbidden_top_level_dirs(repo_root()), [])

    def test_forbidden_old_policy_text_absent(self) -> None:
        self.assertEqual(check_forbidden_policy_text(repo_root()), [])

    def test_file_size_limits(self) -> None:
        self.assertEqual(check_file_size_limits(repo_root()), [])

    def test_root_gitignore_patterns(self) -> None:
        self.assertEqual(check_root_gitignore_patterns(repo_root()), [])

    def test_tracked_temp_artifacts_absent(self) -> None:
        self.assertEqual(check_tracked_temp_artifacts(repo_root()), [])

    def test_source_registers(self) -> None:
        self.assertEqual(check_source_registers(repo_root()), [])

    def test_source_field_map_covers_first_stage_sources(self) -> None:
        path = (
            repo_root()
            / "corpus/006_research-sources-and-bibliography/000_source-registers/"
            / "007_source-field-map.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        source_ids = {row["source_id"] for row in rows}
        expected = {
            "src-hust-obc",
            "src-obimd",
            "src-evobc",
            "src-obid-ancientbooks",
            "src-cambridge-hopkins",
            "src-tsinghua-oracle-bones",
        }
        self.assertTrue(expected.issubset(source_ids))
        self.assertGreaterEqual(len(rows), 20)

    def test_external_prefixes_cover_staging_id_families(self) -> None:
        path = (
            repo_root()
            / "project_registry/003_external-source-prefixes/"
            / "003_external-source-prefixes.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        prefixes = {row["prefix"]: row for row in rows}
        expected = {
            "cam-hopkins-y",
            "cam-hopkins-c",
            "cam-hopkins-h",
            "cam-hopkins-j",
            "hust-obc-cat",
            "ihp-mus-obj",
            "obimd-main",
            "obimd-sub",
            "obimd-glyph-link",
            "evobc-cat",
            "evobc-code",
            "collection-prov",
        }
        self.assertTrue(expected.issubset(prefixes))
        self.assertEqual(prefixes["hust-obc-cat"]["source_id"], "src-hust-obc")
        self.assertEqual(prefixes["obimd-main"]["source_id"], "src-obimd")
        self.assertEqual(prefixes["cam-hopkins-j"]["source_id"], "src-cambridge-hopkins")
        self.assertEqual(prefixes["ihp-mus-obj"]["source_id"], "src-ihp-museum-oracle-bones")
        self.assertEqual(prefixes["evobc-cat"]["source_id"], "src-evobc")
        self.assertIn("not an accepted oracle-character ID", prefixes["hust-obc-cat"]["notes_en"])

    def test_source_package_manifest_covers_large_metadata_boundaries(self) -> None:
        path = (
            repo_root()
            / "corpus/006_research-sources-and-bibliography/000_source-registers/"
            / "009_source-package-file-manifest.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        file_names = {row["file_name"] for row in rows}
        expected = {
            "HUST-OBC.zip",
            "data.json",
            "facsimile.zip",
            "rubbing.zip",
            "Main-character.json",
            "List_of_EVOBC.json",
        }
        self.assertTrue(expected.issubset(file_names))
        for row in rows:
            file_size = int(row["file_size_bytes"])
            if file_size >= 40 * 1024 * 1024:
                self.assertEqual(row["commit_policy"], "do_not_commit_regular_git")

    def test_downloaded_metadata_profiles_include_core_counts(self) -> None:
        path = (
            repo_root()
            / "corpus/006_research-sources-and-bibliography/000_source-registers/"
            / "010_downloaded-metadata-profile.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        metrics = {(row["source_id"], row["profile_metric"]): row["profile_value"] for row in rows}
        self.assertEqual(metrics[("src-hust-obc", "validation_label_count")], "1588")
        self.assertEqual(metrics[("src-obimd", "main_character_uid_count")], "3936")
        self.assertEqual(metrics[("src-evobc", "class_count")], "13714")
        self.assertEqual(metrics[("src-evobc", "image_reference_count")], "229170")

    def test_hust_obc_validation_staging_has_1588_candidate_classes(self) -> None:
        path = (
            repo_root()
            / "corpus/001_oracle-characters/000_character-registers/"
            / "005_hust-obc-validation-class-staging.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(len(rows), 1588)
        self.assertEqual(rows[0]["candidate_class_id"], "obs-cand-000001")
        self.assertEqual(rows[0]["source_category_id"], "0001")
        self.assertEqual(rows[0]["validation_class_id"], "0")
        self.assertEqual(rows[-1]["source_category_id"], "1781")
        self.assertEqual(rows[-1]["validation_class_id"], "1587")
        self.assertEqual(
            {row["project_import_status"] for row in rows},
            {"dataset_candidate_not_promoted"},
        )

    def test_obimd_main_character_staging_has_3936_candidate_uids(self) -> None:
        path = (
            repo_root()
            / "corpus/001_oracle-characters/000_character-registers/"
            / "006_obimd-main-character-staging.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(len(rows), 3936)
        self.assertEqual(rows[0]["candidate_main_character_id"], "obimd-main-cand-000001")
        self.assertEqual(rows[0]["source_uid"], "p8w7ujqanz")
        self.assertEqual(rows[0]["codepoint"], "日")
        self.assertEqual(rows[0]["transcription_values"], "日")
        self.assertEqual(
            {row["project_import_status"] for row in rows},
            {"dataset_candidate_not_promoted"},
        )
        self.assertEqual(
            sum(1 for row in rows if row["has_empty_transcription"] == "true"),
            1159,
        )

    def test_obimd_subcharacter_staging_preserves_hierarchy_and_glyph_links(self) -> None:
        main_path = (
            repo_root()
            / "corpus/003_graphemic-components/000_component-registers/"
            / "002_obimd-subcharacter-main-staging.csv"
        )
        glyph_path = (
            repo_root()
            / "corpus/003_graphemic-components/000_component-registers/"
            / "003_obimd-subcharacter-glyph-staging.csv"
        )
        with main_path.open("r", encoding="utf-8-sig", newline="") as file:
            main_rows = list(csv.DictReader(file))
        with glyph_path.open("r", encoding="utf-8-sig", newline="") as file:
            glyph_rows = list(csv.DictReader(file))
        self.assertEqual(len(main_rows), 2747)
        self.assertEqual(len(glyph_rows), 41686)
        self.assertEqual(main_rows[0]["candidate_subcharacter_id"], "obimd-sub-cand-000001")
        self.assertEqual(main_rows[0]["source_subcharacter_uid"], "p8w7ujqanz")
        self.assertEqual(main_rows[0]["source_main_character_uid"], "p8w7ujqanz")
        self.assertEqual(glyph_rows[0]["candidate_glyph_link_id"], "obimd-glyph-link-000001")
        self.assertEqual(glyph_rows[0]["source_subcharacter_uid"], "p8w7ujqanz")
        self.assertEqual(glyph_rows[0]["glyph_codepoint_uplus"], "U+65E5;U+F0000")
        self.assertEqual(
            {row["project_import_status"] for row in main_rows + glyph_rows},
            {"dataset_candidate_not_promoted"},
        )
        self.assertEqual(len({row["source_subcharacter_uid"] for row in main_rows}), 2747)
        self.assertEqual(len({row["source_main_character_uid"] for row in main_rows}), 1730)
        self.assertEqual(len({row["glyph_codepoint"] for row in glyph_rows}), 41686)

    def test_evobc_evolution_staging_preserves_dataset_scale(self) -> None:
        category_path = (
            repo_root()
            / "corpus/004_bronze-seal-modern-correspondences/000_evolution-registers/"
            / "001_evobc-evolution-category-staging.csv"
        )
        codebook_path = (
            repo_root()
            / "corpus/004_bronze-seal-modern-correspondences/000_evolution-registers/"
            / "002_evobc-era-source-codebook-staging.csv"
        )
        with category_path.open("r", encoding="utf-8-sig", newline="") as file:
            category_rows = list(csv.DictReader(file))
        with codebook_path.open("r", encoding="utf-8-sig", newline="") as file:
            codebook_rows = list(csv.DictReader(file))
        self.assertEqual(len(category_rows), 13714)
        self.assertEqual(category_rows[0]["candidate_evolution_category_id"], "evobc-evo-cat-00001")
        self.assertEqual(category_rows[0]["source_category_id"], "00001")
        self.assertEqual(category_rows[0]["source_character_codepoints"], "U+3401")
        self.assertEqual(category_rows[0]["era_code_counts"], "0:35;3:2")
        self.assertEqual(category_rows[-1]["source_category_id"], "13714")
        self.assertEqual(category_rows[-1]["image_reference_count"], "0")
        self.assertEqual(sum(int(row["image_reference_count"]) for row in category_rows), 229170)
        self.assertEqual(sum(1 for row in category_rows if row["image_reference_count"] == "0"), 2)
        self.assertEqual(
            {row["project_import_status"] for row in category_rows},
            {"dataset_candidate_not_promoted"},
        )
        self.assertEqual(len(codebook_rows), 14)
        era_counts = {
            row["code_value"]: row["image_reference_count"]
            for row in codebook_rows
            if row["code_type"] == "era"
        }
        self.assertEqual(
            era_counts,
            {
                "0": "75681",
                "1": "47314",
                "2": "13434",
                "3": "9131",
                "4": "80042",
                "5": "3568",
            },
        )
        source_counts = {
            row["code_value"]: row["image_reference_count"]
            for row in codebook_rows
            if row["code_type"] == "source"
        }
        self.assertEqual(source_counts["1"], "106010")
        self.assertEqual(
            {row["review_status"] for row in codebook_rows},
            {"reviewed_metadata_only"},
        )

    def test_cambridge_hopkins_crosswalk_preserves_official_references(self) -> None:
        crosswalk_path = (
            repo_root()
            / "corpus/002_oracle-bone-inscriptions/000_inscription-registers/"
            / "002_cambridge-hopkins-crosswalk-staging.csv"
        )
        summary_path = (
            repo_root()
            / "corpus/002_oracle-bone-inscriptions/000_inscription-registers/"
            / "003_cambridge-hopkins-classified-summary.csv"
        )
        with crosswalk_path.open("r", encoding="utf-8-sig", newline="") as file:
            crosswalk_rows = list(csv.DictReader(file))
        with summary_path.open("r", encoding="utf-8-sig", newline="") as file:
            summary_rows = list(csv.DictReader(file))
        self.assertEqual(len(crosswalk_rows), 612)
        self.assertEqual(crosswalk_rows[0]["yingguo_ref_id"], "y1")
        self.assertEqual(crosswalk_rows[0]["cul_ref_id"], "45")
        self.assertEqual(crosswalk_rows[0]["chalfant_ref_id"], "459")
        self.assertEqual(crosswalk_rows[0]["heji_ref_id"], "39502")
        self.assertEqual(crosswalk_rows[-1]["yingguo_ref_id"], "ybu04")
        self.assertEqual(
            {row["project_import_status"] for row in crosswalk_rows},
            {"dataset_candidate_not_promoted"},
        )
        self.assertEqual(sum(1 for row in crosswalk_rows if row["has_missing_cul_ref"] == "true"), 6)
        self.assertEqual(sum(1 for row in crosswalk_rows if row["has_missing_chalfant_ref"] == "true"), 171)
        self.assertEqual(sum(1 for row in crosswalk_rows if row["has_missing_heji_ref"] == "true"), 316)
        self.assertEqual(
            sum(1 for row in crosswalk_rows if row["yingguo_ref_id"] == "y2402"),
            2,
        )
        self.assertEqual(len(summary_rows), 25)
        group_rows = [row for row in summary_rows if row["summary_kind"] == "classified_table_group"]
        self.assertEqual(len(group_rows), 20)
        grand_total = [
            row for row in summary_rows
            if row["summary_kind"] == "classified_table_grand_total"
        ][0]
        self.assertEqual(grand_total["total_count"], "609")

    def test_institutional_collection_provenance_staging_preserves_source_facts(self) -> None:
        path = (
            repo_root()
            / "corpus/005_excavation-sites-periods-and-batches/000_collection-registers/"
            / "001_institutional-collection-provenance-staging.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(len(rows), 4)
        by_source = {row["source_id"]: row for row in rows}
        self.assertEqual(
            set(by_source),
            {
                "src-tsinghua-oracle-bones",
                "src-ihp-oracle-rubbings",
                "src-ihp-museum-oracle-bones",
                "src-cambridge-hopkins",
            },
        )
        self.assertIn("over 1,750", by_source["src-tsinghua-oracle-bones"]["holding_count_statement"])
        self.assertIn("1,495", by_source["src-tsinghua-oracle-bones"]["inscribed_count_statement"])
        self.assertIn("Hu Houxuan", by_source["src-tsinghua-oracle-bones"]["named_provenance_people"])
        self.assertIn("over 40,000", by_source["src-ihp-oracle-rubbings"]["holding_count_statement"])
        self.assertIn("21,556", by_source["src-ihp-oracle-rubbings"]["digitized_record_count_statement"])
        self.assertIn("more than 25,000", by_source["src-ihp-museum-oracle-bones"]["holding_count_statement"])
        self.assertIn("Hsiao-tun Village", by_source["src-ihp-museum-oracle-bones"]["excavation_or_source_context"])
        self.assertIn("grand total 609", by_source["src-cambridge-hopkins"]["holding_count_statement"])
        self.assertIn("50 bones", by_source["src-cambridge-hopkins"]["digitized_record_count_statement"])
        self.assertEqual(
            {row["review_status"] for row in rows},
            {"reviewed_metadata_only"},
        )

    def test_ihp_museum_object_staging_preserves_official_item_links(self) -> None:
        path = (
            repo_root()
            / "corpus/005_excavation-sites-periods-and-batches/000_collection-registers/"
            / "002_ihp-museum-oracle-bone-object-staging.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(len(rows), 52)
        self.assertEqual(rows[0]["candidate_collection_object_id"], "ihp-mus-obj-00001")
        self.assertEqual(rows[0]["source_collection_item_id"], "1212")
        self.assertEqual(rows[0]["catalog_reference_text"], "Jia Bian 3333+3361")
        self.assertEqual(rows[-1]["source_collection_item_id"], "273")
        self.assertEqual(rows[-1]["catalog_reference_text"], "Ping 0264")
        self.assertEqual(len({row["source_collection_item_id"] for row in rows}), 52)
        self.assertTrue(
            all(
                row["object_page_url"].startswith(
                    "https://museum.sinica.edu.tw/en/collection/32/item/"
                )
                for row in rows
            )
        )
        self.assertTrue(
            all(
                row["thumbnail_url"].startswith(
                    "https://museum.sinica.edu.tw/_upload/image/collection_item/thumbnail/"
                )
                for row in rows
            )
        )
        self.assertEqual(
            {row["thumbnail_download_status"] for row in rows},
            {"not_downloaded_metadata_only"},
        )
        self.assertEqual(
            {row["project_import_status"] for row in rows},
            {"object_metadata_not_promoted"},
        )


if __name__ == "__main__":
    unittest.main()
