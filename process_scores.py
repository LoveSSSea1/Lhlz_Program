# process_scores_normal.py
import os
import pandas as pd
import numpy as np

# 科目列表（按需修改）
SUBJECTS = ["物理", "化学", "生物", "政治", "历史", "地理", "技术"]

def map_to_historical_scores_normal(new_scores, historical_scores):
    """
    基于正态分布拟合的赋分方法
    参数:
        new_scores: 当前学生原始分 pd.Series
        historical_scores: 历史赋分 pd.Series
    返回:
        pd.Series，赋分结果
    """
    idx_all = new_scores.index
    valid_mask = new_scores.notna()
    if valid_mask.sum() == 0:
        return pd.Series([None]*len(new_scores), index=idx_all)

    new_valid = new_scores[valid_mask].astype(float)
    hist_valid = historical_scores.dropna().astype(float)
    if hist_valid.empty:
        return pd.Series([None]*len(new_scores), index=idx_all)

    # 原始成绩均值与标准差
    mu_new = new_valid.mean()
    sigma_new = new_valid.std(ddof=0)
    sigma_new = max(sigma_new, 1e-8)  # 避免除零

    # 历史成绩均值与标准差
    mu_hist = hist_valid.mean()
    sigma_hist = hist_valid.std(ddof=0)

    # 计算 z 分数
    z = (new_valid - mu_new) / sigma_new

    # 映射到历史分数
    mapped = z * sigma_hist + mu_hist

    # 限制区间并四舍五入
    mapped = mapped.clip(lower=hist_valid.min(), upper=hist_valid.max()).round()

    # 回填
    result = pd.Series([None]*len(new_scores), index=idx_all)
    result.loc[valid_mask] = mapped.astype(int)

    return result

def process_scores(upload_path, historical_path=None, upload_folder=None):
    """
    主入口：读取上传裸分表、读取历史赋分表（默认 data/副本历次高考_整合.xlsx）
    对 SUBJECTS 中的每个科目进行赋分，输出到 upload_folder/赋分结果.xlsx
    """
    # 读取上传文件
    df_new = pd.read_excel(upload_path)

    # 历史数据路径
    if historical_path is None:
        historical_path = os.path.join(os.path.dirname(__file__), "data", "副本历次高考_整合.xlsx")
    df_hist = pd.read_excel(historical_path)

    # 遍历科目并赋分
    for subj in SUBJECTS:
        if subj in df_new.columns and subj in df_hist.columns:
            try:
                df_new[subj + "_赋分"] = map_to_historical_scores_normal(df_new[subj], df_hist[subj])
            except Exception as e:
                print(f"Error mapping subject {subj}: {e}")
                df_new[subj + "_赋分"] = pd.Series([None]*len(df_new), index=df_new.index)
        else:
            print(f"⚠️ 科目 {subj} 不存在于上传文件或历史赋分表中")
            df_new[subj + "_赋分"] = pd.Series([None]*len(df_new), index=df_new.index)

    # 输出文件
    if upload_folder is None:
        upload_folder = os.path.dirname(upload_path)
    os.makedirs(upload_folder, exist_ok=True)
    output_file = os.path.join(upload_folder, "赋分结果.xlsx")
    df_new.to_excel(output_file, index=False)
    print(f"[INFO] 输出文件：{output_file}")
    return output_file

# 兼容调用
generate_curve_plot = map_to_historical_scores_normal