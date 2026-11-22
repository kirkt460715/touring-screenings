# 巡回放映的新增参与与场次兑现

本项目收录巡回放映的新增参与与场次兑现所需的本地合成资料。记录语义、字段和用途见 [资料语义](docs/资料语义.md)，资料文件位于 materials，字段定义位于 materials/schema.json。

现有入口读取原始资料并检查字段、身份及引用；不生成分析结论、业务安排或签发结果。support 提供这一资料检查入口，tests 检验其对结构损坏的识别。资料是导入用的输入记录，不等于应用已经受理、签准或执行的业务状态。

Python 3.11 环境，依赖固定在 requirements.txt。统计、图分析和本地分析存储所用的库均为本地库，不需要外部账号。安装依赖：

```sh
python3 -m pip install -r requirements.txt
```

检查资料：

```sh
python3 -m support.inspect_materials
```

运行现有测试和语法编译：

```sh
python3 -m unittest discover -s tests -v
python3 -m compileall -q support tests
```

也可以向资料检查入口传入另一份同格式资料目录。它只读输入，不修改合成记录。业务实现产生的状态与输入资料应在使用说明中区分，后续运行入口由应用本身提供。
