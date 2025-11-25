# Lhlz_Program
# 📘 Lhlz_Program

> 高中数据处理与成绩分析工具平台（Flask Web + Excel 操作）

Lhlz_Program 是一个面向教育数据处理的 Web 工具平台，集成绩赋分、切线分析、Excel 数据清洗、拆分合并等功能于一体，方便教师或管理者快速处理和分析学生成绩数据。

---

## 🔹 功能模块

### 1. Excel 数据处理
- 拆分 Excel 文件（按班级、科目等条件）
- 合并多个 Excel 文件
- 清洗 Excel 数据（去空行、去重、统一格式）

### 2. 成绩赋分与分析
- 基于历史分数曲线进行自适应赋分
- 支持“孙渊法”赋分方法
- 多次上一段线统计与分析
- 可生成每门科目的赋分对比结果（原始分 / 赋分 / 孙渊法）

### 3. 高考分数统计与切线分析
- 支持多 Sheet Excel 文件批量分析
- 输入各班上一段线分数
- 自动生成上一段线名单
- 统计一次上一段线 / 两次上一段线名单

---

## 🔹 项目演示

### 主页面
![首页](docs/home_page.png)

### 成绩赋分界面
![赋分页面](docs/score_assign.png)

### 分析结果界面
![分析页面](docs/score_analyze.png)

---

## 🔹 使用说明

### 1️⃣ 安装依赖
建议在 Python 虚拟环境中安装：

```bash
python -m venv venv
source venv/bin/activate   # Mac / Linux
venv\Scripts\activate      # Windows
pip install -r requirements.txt
