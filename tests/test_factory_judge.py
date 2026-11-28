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


if __name__ == "__main__":
    unittest.main()
