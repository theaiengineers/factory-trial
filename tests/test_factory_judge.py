import importlib.util
import pathlib
import unittest

spec = importlib.util.spec_from_file_location("factory_judge", pathlib.Path(__file__).parent.parent / "scripts" / "factory_judge.py")
judge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(judge)


class Judge(unittest.TestCase):
    def level(self, **f):
        return judge.classify([f])["review"]

    def test_levels(self):
        self.assertEqual(self.level(filename="README.md"), "none")
        self.assertEqual(self.level(filename="units/length.py", patch="+x"), "code")
        self.assertEqual(self.level(filename=".github/workflows/tests.yml", patch="+x"), "high")
        self.assertEqual(self.level(filename="tests/test_length.py", patch="+    def test_new(self):"), "code")
        self.assertEqual(self.level(filename="tests/test_length.py", patch="-    def test_a_marathon(self):"), "high")
        self.assertEqual(self.level(filename="tests/test_length.py", status="removed"), "high")
        self.assertEqual(self.level(filename="tests/test_length.py"), "high")       # no diff to read

    def test_a_rename_is_judged_under_both_names(self):
        for new, old, want in ((".github/workflows/tests.md", ".github/workflows/tests.yml", "high"), ("ci/tests.yml", ".github/workflows/tests.yml", "high"),
                               ("tests/test_length.md", "tests/test_length.py", "high"), ("old/test_length.py", "tests/test_length.py", "high"),
                               ("units/length.md", "units/length.py", "code"), ("docs/b.md", "docs/a.md", "none")):
            self.assertEqual(self.level(filename=new, previous_filename=old, status="renamed", patch=""), want, (new, old))

    def test_it_runs_as_the_gate_runs_it(self):
        import json, subprocess, sys
        script = pathlib.Path(__file__).parent.parent / "scripts" / "factory_judge.py"
        asked = json.dumps({"factory_judge": 1, "files": [{"filename": ".github/workflows/tests.yml", "status": "modified", "patch": "+x"}]})
        done = subprocess.run([sys.executable, str(script)], input=asked, capture_output=True, text=True)
        answer = json.loads(done.stdout)
        self.assertEqual((done.returncode, answer["review"], answer["reasons"][0]["area"]), (0, "high", "workflows"))
        self.assertNotEqual(subprocess.run([sys.executable, str(script)], input="{}", capture_output=True, text=True).returncode, 0)


if __name__ == "__main__":
    unittest.main()
