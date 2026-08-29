#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《三体》三部曲 txt -> 精排 HTML/PDF 转换脚本
按照 README 排版要求：
- A4，白底黑字
- 页边距：上3.7cm / 下3.5cm / 左2.8cm / 右2.6cm
- 书名页：黑体二号居中，楷体署名
- 章标题：黑体三号居中
- 正文：仿宋三号(16pt)，首行缩进两字符，固定28pt行距
- 页码：页脚居中"— n —"，四号宋体
"""

import re
import html

INPUT_FILE = "三体源本.txt"
OUTPUT_HTML = "三体三部曲.html"
OUTPUT_MD = "三体三部曲.md"

def read_lines(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.readlines()

def is_blank(line):
    return line.strip() == ""

def classify_line(line, line_num, total_lines):
    """分类行，返回 (type, content)"""
    s = line.rstrip("\r\n")
    stripped = s.strip()

    if stripped == "":
        return ("blank", "")

    # 跳过文件首行总标题
    if line_num == 0 and stripped.startswith("《三体》"):
        return ("skip", "")

    # 过滤星号分隔符
    if re.match(r"^\*+$", stripped):
        return ("skip", "")

    # 内容简介中的子标题：《三体1》《三体2·黑暗森林》《三体3·死神永生》
    if stripped in ("《三体1》", "《三体2·黑暗森林》", "《三体3·死神永生》"):
        return ("intro_subtitle", stripped)

    # 三部曲大标题
    if re.match(r"^三体1\s*$", stripped):
        return ("book1", "三体Ⅰ")
    if re.match(r"^三体2[：:]\s*黑暗森林\s*$", stripped):
        return ("book2", "三体Ⅱ·黑暗森林")
    if re.match(r"^三体3[：:]\s*死神永生\s*$", stripped):
        return ("book3", "三体Ⅲ·死神永生")

    # 内容简介 / 作者简介
    if stripped == "内容简介：":
        return ("section_title", "内容简介")
    if stripped == "作者简介：":
        return ("section_title", "作者简介")

    # 序
    if stripped == "序" and line_num < 60:
        return ("preface_title", "序")
    if stripped == "序章":
        return ("preface_title", "序章")
    if stripped == "后记":
        return ("preface_title", "后记")

    # 第三部的序言
    if stripped.startswith("写在") and "基石" in stripped:
        return ("preface_title", stripped)
    if stripped == "心事浩渺连广宇":
        return ("preface_title", "心事浩渺连广宇")
    if stripped == "纪年对照表":
        return ("preface_title", "纪年对照表")

    # 第一部的章节：第X章 标题
    m = re.match(r"^第(\d+)章\s+(.+)$", stripped)
    if m:
        return ("chapter", f"第{m.group(1)}章　{m.group(2)}")

    # 第二部的部标题
    if re.match(r"^上部\s+", stripped):
        return ("part_title", stripped)
    if re.match(r"^中部\s+", stripped):
        return ("part_title", stripped)
    if re.match(r"^下部\s+", stripped):
        return ("part_title", stripped)

    # 第三部的部标题
    if stripped == "第一部":
        return ("part_title", "第一部")
    if stripped == "第二部":
        return ("part_title", "第二部")
    if stripped == "第三部":
        return ("part_title", "第三部")

    # 第三部的小节标题：【...】
    if stripped.startswith("【") and stripped.endswith("】"):
        return ("subsection", stripped.strip("【】"))

    # 《时间之外的往事》标记
    if stripped.startswith("**《时间之外的往事》") or stripped.startswith("《时间之外的往事》"):
        return ("time_marker", stripped.replace("**", ""))

    # 正文（以全角空格开头）
    if s.startswith("\u3000") or s.startswith("  "):
        return ("text", stripped)

    # 其他非空行，也当作正文
    return ("text", stripped)


def build_html(lines):
    """构建HTML内容"""
    body_parts = []
    in_book = False
    current_book = ""

    i = 0
    n = len(lines)

    while i < n:
        ltype, content = classify_line(lines[i], i, n)

        if ltype == "blank":
            i += 1
            continue

        if ltype == "skip":
            i += 1
            continue

        if ltype == "intro_subtitle":
            body_parts.append(f'<p class="intro-subtitle">{html.escape(content)}</p>')
            i += 1
            continue

        if ltype == "book1":
            current_book = "三体Ⅰ"
            body_parts.append(f'<div class="book-page"><h1 class="book-title">{content}</h1><p class="book-author">刘慈欣　著</p></div>')
            i += 1
            continue

        if ltype == "book2":
            current_book = "三体Ⅱ·黑暗森林"
            body_parts.append(f'<div class="book-page"><h1 class="book-title">{content}</h1><p class="book-author">刘慈欣　著</p></div>')
            i += 1
            continue

        if ltype == "book3":
            current_book = "三体Ⅲ·死神永生"
            body_parts.append(f'<div class="book-page"><h1 class="book-title">{content}</h1><p class="book-author">刘慈欣　著</p></div>')
            i += 1
            continue

        if ltype == "section_title":
            body_parts.append(f'<h2 class="section-title">{html.escape(content)}</h2>')
            i += 1
            continue

        if ltype == "preface_title":
            body_parts.append(f'<h2 class="preface-title">{html.escape(content)}</h2>')
            i += 1
            continue

        if ltype == "chapter":
            body_parts.append(f'<h2 class="chapter-title">{html.escape(content)}</h2>')
            i += 1
            continue

        if ltype == "part_title":
            body_parts.append(f'<h2 class="part-title">{html.escape(content)}</h2>')
            i += 1
            continue

        if ltype == "subsection":
            body_parts.append(f'<h3 class="subsection">{html.escape(content)}</h3>')
            i += 1
            continue

        if ltype == "time_marker":
            body_parts.append(f'<p class="time-marker">{html.escape(content)}</p>')
            i += 1
            continue

        if ltype == "text":
            # 收集连续的正文行
            para_lines = [content]
            i += 1
            while i < n:
                lt2, c2 = classify_line(lines[i], i, n)
                if lt2 == "text":
                    para_lines.append(c2)
                    i += 1
                elif lt2 == "blank":
                    i += 1
                    break
                else:
                    break
            text = "".join(para_lines)
            body_parts.append(f'<p class="body-text">{html.escape(text)}</p>')
            continue

        i += 1

    return "\n".join(body_parts)


def build_markdown(lines):
    """构建Markdown内容"""
    parts = []
    i = 0
    n = len(lines)

    while i < n:
        ltype, content = classify_line(lines[i], i, n)

        if ltype == "blank":
            i += 1
            continue

        if ltype == "skip":
            i += 1
            continue

        if ltype == "intro_subtitle":
            parts.append(f"\n**{content}**\n")
            i += 1
            continue

        if ltype in ("book1", "book2", "book3"):
            parts.append(f"\n# {content}\n")
            parts.append("*刘慈欣 著*\n")
            i += 1
            continue

        if ltype == "section_title":
            parts.append(f"\n## {content}\n")
            i += 1
            continue

        if ltype == "preface_title":
            parts.append(f"\n## {content}\n")
            i += 1
            continue

        if ltype == "chapter":
            parts.append(f"\n## {content}\n")
            i += 1
            continue

        if ltype == "part_title":
            parts.append(f"\n## {content}\n")
            i += 1
            continue

        if ltype == "subsection":
            parts.append(f"\n### {content}\n")
            i += 1
            continue

        if ltype == "time_marker":
            parts.append(f"\n**{content}**\n")
            i += 1
            continue

        if ltype == "text":
            para_lines = [content]
            i += 1
            while i < n:
                lt2, c2 = classify_line(lines[i], i, n)
                if lt2 == "text":
                    para_lines.append(c2)
                    i += 1
                elif lt2 == "blank":
                    i += 1
                    break
                else:
                    break
            text = "".join(para_lines)
            parts.append(f"\n{text}\n")
            continue

        i += 1

    return "\n".join(parts)


CSS = """
@page {
    size: A4;
    margin: 3.7cm 2.6cm 3.5cm 2.8cm;
    @bottom-center {
        content: "— " counter(page) " —";
        font-family: "Noto Serif CJK SC", serif;
        font-size: 14pt;
        color: #000;
    }
}

@page :first {
    @bottom-center {
        content: none;
    }
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: "Noto Serif CJK SC", "AR PL UMing CN", serif;
    font-size: 16pt;
    line-height: 28pt;
    color: #000;
    background: #fff;
}

/* 书名页 */
.book-page {
    page-break-after: always;
    page-break-inside: avoid;
    text-align: center;
    margin-top: 5cm;
    margin-bottom: 5cm;
}

.book-title {
    font-family: "Noto Sans CJK SC", "WenQuanYi Micro Hei", sans-serif;
    font-size: 36pt;
    font-weight: 900;
    letter-spacing: 0.5em;
    margin: 0 0 3cm 0;
    text-indent: 0.5em;
}

.book-author {
    font-family: "AR PL UKai CN", "KaiTi", cursive;
    font-size: 20pt;
    letter-spacing: 0.3em;
    text-indent: 0.3em;
    margin: 0;
    white-space: nowrap;
}

/* 内容简介/作者简介标题 */
.section-title {
    font-family: "Noto Sans CJK SC", sans-serif;
    font-size: 20pt;
    font-weight: bold;
    text-align: center;
    margin: 1.5em 0 1em 0;
    page-break-after: avoid;
}

/* 序/后记标题 */
.preface-title {
    font-family: "Noto Sans CJK SC", sans-serif;
    font-size: 20pt;
    font-weight: bold;
    text-align: center;
    margin: 2em 0 1.5em 0;
    page-break-after: avoid;
}

/* 章标题：黑体三号居中 */
.chapter-title {
    font-family: "Noto Sans CJK SC", "WenQuanYi Micro Hei", sans-serif;
    font-size: 18pt;
    font-weight: bold;
    text-align: center;
    margin: 2em 0 1.5em 0;
    page-break-after: avoid;
    letter-spacing: 0.1em;
}

/* 部标题（上部/中部/下部，第一部/第二部/第三部） */
.part-title {
    font-family: "Noto Sans CJK SC", sans-serif;
    font-size: 22pt;
    font-weight: 900;
    text-align: center;
    margin: 3em 0 2em 0;
    page-break-before: always;
    page-break-after: avoid;
    letter-spacing: 0.3em;
    text-indent: 0.3em;
}

/* 第三部小节标题 */
.subsection {
    font-family: "Noto Sans CJK SC", sans-serif;
    font-size: 15pt;
    font-weight: bold;
    text-align: center;
    margin: 1.5em 0 1em 0;
    page-break-after: avoid;
}

/* 《时间之外的往事》标记 */
.time-marker {
    font-family: "AR PL UKai CN", "KaiTi", cursive;
    font-size: 14pt;
    text-align: center;
    margin: 1em 0;
    color: #333;
}

/* 内容简介子标题 */
.intro-subtitle {
    font-family: "Noto Sans CJK SC", sans-serif;
    font-size: 15pt;
    font-weight: bold;
    margin: 1em 0 0.3em 0;
    text-indent: 0;
}

/* 正文：仿宋三号(16pt)，首行缩进两字符，固定28pt行距 */
.body-text {
    font-family: "Noto Serif CJK SC", "AR PL UMing CN", "FangSong", serif;
    font-size: 16pt;
    line-height: 28pt;
    text-indent: 2em;
    text-align: justify;
    margin: 0;
    widows: 2;
    orphans: 2;
}
"""


def main():
    lines = read_lines(INPUT_FILE)
    print(f"读取 {len(lines)} 行")

    # 生成HTML
    body = build_html(lines)
    html_doc = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>《三体》三部曲 — 刘慈欣</title>
<style>
{CSS}
</style>
</head>
<body>
{body}
</body>
</html>"""

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_doc)
    print(f"HTML 已生成: {OUTPUT_HTML}")

    # 生成Markdown
    md = build_markdown(lines)
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Markdown 已生成: {OUTPUT_MD}")


if __name__ == "__main__":
    main()
