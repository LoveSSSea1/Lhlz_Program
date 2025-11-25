from flask import Flask, render_template, request, send_file, redirect, flash
import os
from process_scores import process_scores
from analyze_scores import analyze_scores   # 新功能导入

app = Flask(__name__)
app.secret_key = "secret_key"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
TEMPLATE_FOLDER = os.path.join(BASE_DIR, "templates_files")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TEMPLATE_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("home.html")

# ========= 原赋分功能 =========
@app.route("/score/assign", methods=["GET", "POST"])
def score_assign():
    if request.method == "POST":
        file = request.files.get("file")
        if not file or file.filename == "":
            flash("未选择文件")
            return redirect(request.url)

        upload_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(upload_path)
        output_file = process_scores(upload_path, upload_folder=UPLOAD_FOLDER)

        flash("赋分完成！请下载结果")
        return send_file(output_file, as_attachment=True)

    return render_template("score_assign.html")


# ========= 新增：成绩分析功能（多sheet统计上一段线次数） =========
@app.route("/score/analyze", methods=["GET", "POST"])
def score_analyze():
    if request.method == "POST":
        file = request.files.get("file")
        thresholds = request.form.get("thresholds")  # 例：630,620,615

        if not file or file.filename == "":
            flash("未选择文件")
            return redirect(request.url)

        upload_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(upload_path)

        try:
            threshold_list = [int(x) for x in thresholds.split(",")]
        except:
            flash("阈值格式错误，请输入类似：630,620,615")
            return redirect(request.url)

        output_file = analyze_scores(upload_path, threshold_list)

        flash("成绩分析完成！已生成统计表")
        return send_file(output_file, as_attachment=True)

    return render_template("score_analyze.html")


@app.route("/score/download_template")
def download_template():
    template_path = os.path.join(TEMPLATE_FOLDER, "score_template.xlsx")
    if not os.path.exists(template_path):
        import openpyxl
        wb = openpyxl.Workbook()
        wb.save(template_path)
    return send_file(template_path, as_attachment=True)

from analyze_scores import download_analyze_template

@app.route("/score/analyze/download_template")
def analyze_download_template():
    return download_analyze_template()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)