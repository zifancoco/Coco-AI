"""
将CSV数据注入到HTML仪表板中，生成可独立打开的HTML文件
"""
import pandas as pd
import json
import os

WORK_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(WORK_DIR, "512010_医药ETF易方达.csv")
HTML_TEMPLATE = os.path.join(WORK_DIR, "dashboard.html")
OUTPUT_HTML = os.path.join(WORK_DIR, "512010_医药ETF易方达_面板.html")


def main():
    # 读取CSV数据
    df = pd.read_csv(CSV_PATH, encoding='utf-8-sig')
    print(f"读取 {len(df)} 条数据")

    # 转换为JSON格式（按行记录）
    records = df.to_dict(orient='records')

    # 转换日期格式为字符串
    for r in records:
        r['日期'] = str(r['日期'])[:10]

    data_json = json.dumps(records, ensure_ascii=False)

    # 读取HTML模板
    with open(HTML_TEMPLATE, 'r', encoding='utf-8') as f:
        html = f.read()

    # 替换数据占位符
    html = html.replace('DATA_PLACEHOLDER', data_json)

    # 写入输出文件
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"HTML面板已生成: {OUTPUT_HTML}")
    print(f"文件大小: {os.path.getsize(OUTPUT_HTML):,} bytes")


if __name__ == "__main__":
    main()
