"""合成资料的结构及引用检查入口。"""
import argparse
import json
from pathlib import Path

KINDS = {"string": str, "number": (int, float), "boolean": bool, "array": list, "object": dict}

def load_materials(directory):
    """读取资料定义和原始记录，不进行业务计算。"""
    directory = Path(directory)
    schema = json.loads((directory / "schema.json").read_text(encoding="utf-8"))
    tables = {}
    for name in schema:
        with (directory / (name + ".jsonl")).open(encoding="utf-8") as stream:
            tables[name] = [json.loads(line) for line in stream if line.strip()]
    return schema, tables

def inspect(schema, tables):
    """核对字段类型、记录身份和跨表引用是否完整。"""
    errors = []
    identities = {}
    for name, rows in tables.items():
        seen = set()
        for record in rows:
            identifier = record.get("id")
            if not identifier or identifier in seen:
                errors.append(f"{name}: 记录身份缺失或重复 {identifier}")
            seen.add(identifier)
        identities[name] = seen
    for name, definition in schema.items():
        for record in tables.get(name, []):
            location = f"{name}/{record.get('id')}"
            if set(record) != set(definition["fields"]):
                errors.append(f"{location}: 字段集合不匹配")
            for field, contract in definition["fields"].items():
                value = record.get(field)
                if value is None:
                    continue
                expected = KINDS[contract["type"]]
                if not isinstance(value, expected) or (contract["type"] == "number" and isinstance(value, bool)):
                    errors.append(f"{location}/{field}: 字段类型不匹配")
                    continue
                target = contract.get("ref")
                if target:
                    values = value if isinstance(value, list) else [value]
                    for reference in values:
                        if reference not in identities.get(target, set()):
                            errors.append(f"{location}/{field}: 未找到引用 {target}/{reference}")
    return errors

def main():
    parser = argparse.ArgumentParser(description="检查合成资料的结构与引用")
    parser.add_argument("directory", nargs="?", default="materials")
    args = parser.parse_args()
    schema, tables = load_materials(args.directory)
    errors = inspect(schema, tables)
    result = {"资料记录数": {name: len(rows) for name, rows in tables.items()}, "结构错误": errors}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
