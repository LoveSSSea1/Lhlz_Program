import pandas as pd
from flask import send_file
import os
import openpyxl

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_FOLDER = os.path.join(BASE_DIR, "templates_files")
os.makedirs(TEMPLATE_FOLDER, exist_ok=True)

def download_analyze_template():
    template_path = os.path.join(TEMPLATE_FOLDER, "历次考试总分.xlsx")
    if not os.path.exists(template_path):
        # 创建空模板
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Sheet1"
        ws.append(["班级", "姓名", "总分"])  # 必备列
        wb.save(template_path)
    return send_file(template_path, as_attachment=True)
def analyze_scores(file_path, thresholds):
    xls = pd.ExcelFile(file_path)
    sheet_names = xls.sheet_names
    results = {}
    student_count = {}

    for idx, sheet in enumerate(sheet_names):
        df = pd.read_excel(xls, sheet_name=sheet)
        df = df[["班级", "姓名", "总分"]].dropna()

        df_filtered = df[df["总分"] >= thresholds[idx]]
        results[sheet] = df_filtered

        for name in df_filtered["姓名"]:
            student_count[name] = student_count.get(name, 0) + 1

    summary_df = pd.DataFrame(
        [(name, count) for name, count in student_count.items()],
        columns=["姓名", "上几次一段线"]
    ).sort_values(by="上几次一段线", ascending=False)

    with pd.ExcelWriter("一段线统计结果.xlsx") as writer:
        for sheet, df_up in results.items():
            df_up.sort_values(by="总分", ascending=False).to_excel(writer, sheet_name=f"{sheet}_上段线", index=False)

        summary_df.to_excel(writer, sheet_name="汇总统计", index=False)

    return "一段线统计结果.xlsx"