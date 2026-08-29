# convert.py
from weasyprint import HTML
import re

def read_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def build_html(raw_text: str) -> str:
    css = """
@page {
    size: A4;
    margin: 2.5cm 2cm;
    @bottom-center {
        content: "— " counter(page) " —";
        font-size:11pt;
        color:#333;
    }
}
body {
    font-family: "SimSun", "Songti SC", serif;
    font-size:16pt;
    line-height:28pt;
}
.title-page{
    page-break-after: always;
    text-align:center;
    padding-top:120px;
}
.book-title{
    font-size:26pt;
    font-weight:bold;
    margin-bottom:40px;
}
.author{
    font-size:18pt;
    font-style:italic;
}
h1{
    font-size:20pt;
    text-align:center;
    font-weight:bold;
    margin:30px 0 20px 0;
    page-break-before: always;
}
h2{
    font-size:17pt;
    text-align:center;
    margin:24px 0 16px 0;
}
p{
    text-indent:2em;
    margin:0;
}
.noindent p{
    text-indent:0;
}
hr{
    margin:30px 0;
    border:none;
}
"""
    html_head = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>{css}</style>
</head>
<body>
"""
    html_end = "</body></html>"
    content = raw_text

    # 简单文本转段落：换行分段
    paragraphs = content.split("\n")
    body_parts = []
    for para in paragraphs:
        line = para.strip()
        if not line:
            continue
        # 匹配章节标题：第X章 xxx
        if re.match(r"^第[\d０-９]+章", line):
            body_parts.append(f"<h2>{line}</h2>")
        # 三部大标题匹配
        elif line.startswith("三体1") or line.startswith("《三体1》"):
            body_parts.append('<div class="title-page"><div class="book-title">三体 Ⅰ 地球往事</div><div class="author">刘慈欣 著</div></div>')
        elif line.startswith("三体2") or line.startswith("《三体2"):
            body_parts.append('<div class="title-page"><div class="book-title">三体 Ⅱ 黑暗森林</div><div class="author">刘慈欣 著</div></div>')
        elif line.startswith("三体3") or line.startswith("《三体3"):
            body_parts.append('<div class="title-page"><div class="book-title">三体 Ⅲ 死神永生</div><div class="author">刘慈欣 著</div></div>')
        else:
            body_parts.append(f"<p>{line}</p>")

    body_html = "\n".join(body_parts)
    full_html = html_head + body_html + html_end
    return full_html


def main():
    src_file = "三体源本.txt"
    out_html = "temp.html"
    out_pdf = "三体三部曲.pdf"

    print(f"读取源文件 {src_file}")
    raw = read_txt(src_file)
    html_text = build_html(raw)

    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html_text)
    print(f"临时html已输出：{out_html}")

    HTML(string=html_text).write_pdf(out_pdf)
    print(f"✅ PDF生成完成 -> {out_pdf}")


if __name__ == "__main__":
    main()
