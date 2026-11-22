"""资料读取入口的结构检查。"""
import copy
import unittest
from pathlib import Path
from support.inspect_materials import load_materials, inspect

class MaterialChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema, cls.tables = load_materials(Path(__file__).resolve().parents[1] / "materials")

    def test_structural_integrity(self):
        self.assertEqual([], inspect(self.schema, self.tables))

    def test_duplicate_identity_is_visible(self):
        tables = copy.deepcopy(self.tables)
        name = next(iter(tables))
        tables[name].append(copy.deepcopy(tables[name][0]))
        self.assertTrue(inspect(self.schema, tables))

    def test_missing_cross_reference_is_visible(self):
        tables = copy.deepcopy(self.tables)
        changed = False
        for name, definition in self.schema.items():
            for field, contract in definition["fields"].items():
                if contract.get("ref") and tables[name]:
                    tables[name][0][field] = ["不存在的编号"] if contract["type"] == "array" else "不存在的编号"
                    changed = True
                    break
            if changed:
                break
        self.assertTrue(changed)
        self.assertTrue(inspect(self.schema, tables))

    def test_wrong_field_type_is_visible(self):
        tables = copy.deepcopy(self.tables)
        name = next(iter(tables))
        tables[name][0]["id"] = 8
        self.assertTrue(inspect(self.schema, tables))

if __name__ == "__main__":
    unittest.main()
