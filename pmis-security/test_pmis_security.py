import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location('pmis_security', Path(__file__).with_name('pmis_security.py'))
scanner = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = scanner
SPEC.loader.exec_module(scanner)


class MigrationGuardTest(unittest.TestCase):
    def test_multiline_restricted_update(self):
        sql = 'UPDATE public.apartements\nSET price = CASE WHEN floor < 6 THEN 1700 ELSE 1800 END\nWHERE floor BETWEEN 2 AND 15;'
        self.assertEqual([], list(scanner.unbounded_updates(sql)))

    def test_each_update_needs_its_own_where(self):
        sql = 'UPDATE users SET active = false; UPDATE users SET active = true WHERE id = 1;'
        matches = list(scanner.unbounded_updates(sql))
        self.assertEqual(1, len(matches))
        self.assertEqual(0, matches[0].start())

    def test_comment_literal_and_subquery_do_not_restrict_update(self):
        for sql in [
            "UPDATE users SET name = 'WHERE id = 1';",
            'UPDATE users SET active = false /* WHERE id = 1 */;',
            'UPDATE users SET active = false -- WHERE id = 1\n;',
            'UPDATE users SET name = (SELECT name FROM archive WHERE id = 1);',
            'UPDATE users SET name = $$WHERE id = 1;$$;',
        ]:
            with self.subTest(sql=sql):
                self.assertEqual(1, len(list(scanner.unbounded_updates(sql))))

    def test_cte_update_has_separate_scope(self):
        sql = 'WITH changed AS (UPDATE users SET active = false RETURNING id) UPDATE users SET active = true WHERE id = 1;'
        self.assertEqual(1, len(list(scanner.unbounded_updates(sql))))

    def test_where_in_later_query_does_not_hide_update(self):
        sql = 'UPDATE users SET active = false; SELECT * FROM users WHERE id = 1;'
        self.assertEqual(1, len(list(scanner.unbounded_updates(sql))))

    def test_quoted_identifiers_are_supported(self):
        self.assertEqual([], list(scanner.unbounded_updates('UPDATE "users" SET "password" = \'x\' WHERE "id" = 1;')))

    def test_obvious_always_true_predicates_are_flagged(self):
        for condition in ['TRUE', '(1 = 1)']:
            self.assertEqual(1, len(list(scanner.unbounded_updates('UPDATE users SET active = false WHERE ' + condition + ';'))))


class CredentialGuardTest(unittest.TestCase):
    def test_shared_password_stays_flagged(self):
        value = 'private static final String TEMPORARY_PASSWORD = "example-only-value";'
        self.assertEqual(1, len(list(scanner.hardcoded_credentials(value))))

    def test_generated_password_link_is_not_a_secret_literal(self):
        value = 'return appUrl + "/set-password?token=" + token;'
        self.assertEqual([], list(scanner.hardcoded_credentials(value)))

    def test_environment_reference_does_not_hide_other_credentials(self):
        value = 'api_key: "${{ secrets.API_KEY }}"\npassword: "example-only-value"'
        matches = list(scanner.hardcoded_credentials(value))
        self.assertEqual(1, len(matches))
        self.assertIn('password', matches[0].group())

    def test_dollar_inside_literal_is_still_flagged(self):
        self.assertEqual(1, len(list(scanner.hardcoded_credentials('password = "example$value"'))))

    def test_json_key_and_multiple_assignments(self):
        matches = list(scanner.hardcoded_credentials('{"api_key": "example-key-value", "password": "example-password"}'))
        self.assertEqual(2, len(matches))

    def test_maven_does_not_require_a_node_lockfile(self):
        original = scanner.ROOT
        try:
            with tempfile.TemporaryDirectory() as directory:
                scanner.ROOT = Path(directory)
                pom = scanner.ROOT / 'pom.xml'
                pom.write_text('<project/>')
                findings = []
                scanner.scan([pom], findings, '')
                self.assertFalse(any(item.rule == 'dependency-lock' for item in findings))
        finally:
            scanner.ROOT = original


if __name__ == '__main__':
    unittest.main()
