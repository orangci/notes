# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: orangc

from pygments.lexers import get_lexer_by_name
from pygments.formatters import html
from bs4 import BeautifulSoup
from datetime import datetime
import pygments
import pathlib
import mistune
import toml
import re
import xml.etree.ElementTree as ET

SRC_DIR = pathlib.Path("src")
NOTES_DIR = pathlib.Path("notes")
TEMPLATE_FILE = pathlib.Path("template.html")
INDEX_FILE = pathlib.Path("index.html")
RSS_FILE = pathlib.Path("rss.xml")
BASE_URL = "https://notes.orangc.net"


class HighlightRenderer(mistune.HTMLRenderer):
    def block_code(self, code, info=None):
        if info:
            lexer = get_lexer_by_name(info, stripall=True)
            formatter = html.HtmlFormatter()
            return pygments.highlight(code, lexer, formatter)
        return "<pre><code>" + mistune.escape(code) + "</code></pre>"

    def heading(self, text, level):
        slug = re.sub(r"[^a-zA-Z0-9 ]", "", text).lower().replace(" ", "-")
        return f'''<h{level} id="{slug}" onclick="navigator.clipboard.writeText(location.href.split('#')[0] + '#{slug}')"> {text} </h{level}>'''


md_parser = mistune.create_markdown(
    renderer=HighlightRenderer(),
    plugins=[
        "spoiler",
        "footnotes",
        "url",
        "task_lists",
        "abbr",
        "superscript",
        "subscript",
        "table",
        "strikethrough",
    ],
)


def format_date(date_str):
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return dt.strftime("%B %d, %Y"), dt.strftime("%Y-%m-%d")


def read_post(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    meta_match = re.match(r"\+\+\+(.+?)\+\+\+", content, re.DOTALL)
    if not meta_match:
        print(f"Skipping {file_path.name}: it appears this file has no metadata set.")
        return None
    meta = toml.loads(meta_match.group(1).strip())
    body = content[meta_match.end() :].strip()
    html_content = md_parser(body)
    # html_content = html_content.replace() # this is possible, if you ever want to replace stuff in le future
    return meta, html_content


def write_html(file_path, content):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)


def build_index(posts_info):
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    posts_list = soup.select_one("#posts-list")
    posts_list.clear()
    for meta, _ in posts_info:
        if meta.get("hidden"):
            continue
        formatted_date, datetime_attr = format_date(meta["date"])
        li = soup.new_tag("li")
        filename = meta["src_filename"].replace(".md", ".html")
        a = soup.new_tag(
            "a", attrs={"class": "link2 me-2", "href": f"notes/{filename}"}
        )
        a.string = meta["title"]
        li.append(a)
        li.append(" ")
        span = soup.new_tag("span", attrs={"class": "post_time"})
        time_tag = soup.new_tag("time", attrs={"datetime": datetime_attr})
        time_tag.string = formatted_date
        span.append(time_tag)
        if meta.get("edited"):
            formatted_date_edited, datetime_attr_edited = format_date(meta["edited"])
            span.append(" (edited ")
            edited_time_tag = soup.new_tag(
                "time", attrs={"datetime": datetime_attr_edited}
            )
            edited_time_tag.string = formatted_date_edited
            span.append(edited_time_tag)
            span.append(")")
        li.append(span)
        posts_list.append(li)
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(str(soup))


def build_post_files(posts_info):
    for file in NOTES_DIR.iterdir():
        if file.name != "template.html" and file.is_file():
            file.unlink()
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        template = f.read()
    for i, (meta, html_content) in enumerate(posts_info):
        formatted_date, datetime_attr = format_date(meta["date"])
        time_element = '<span class="post_time">'
        time_element += f'<time datetime="{datetime_attr}">{formatted_date}</time>'
        if meta.get("edited"):
            formatted_date_edited, datetime_attr_edited = format_date(meta["edited"])
            time_element += f' (edited <time datetime="{datetime_attr_edited}">{formatted_date_edited}</time>)'
        time_element += "</span>"
        post_html = template.replace("{{ title }}", meta["title"])
        post_html = post_html.replace("{{ desc }}", meta["desc"])
        post_html = post_html.replace("{{ date }}", time_element)
        post_html = post_html.replace("{{ post-content }}", html_content)
        output_filename = posts_info[i][0]["src_filename"].replace(".md", ".html")
        output_path = NOTES_DIR / output_filename
        write_html(output_path, post_html)


def build_rss(posts_info):
    rss = ET.Element(
        "rss",
        version="2.0",
        attrib={"xmlns:content": "http://purl.org/rss/1.0/modules/content/"},
    )
    channel = ET.SubElement(rss, "channel")

    ET.SubElement(channel, "title").text = "orangc's notes"
    ET.SubElement(channel, "link").text = BASE_URL
    ET.SubElement(
        channel, "description"
    ).text = "Occasional posts about anything and eveything."

    for meta, html_content in posts_info:
        if meta.get("hidden"):
            continue

        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = meta["title"]

        post_url = f"{BASE_URL}/notes/{meta['src_filename'].replace('.md', '.html')}"
        ET.SubElement(item, "link").text = post_url
        ET.SubElement(item, "guid").text = post_url

        pubdate = datetime.strptime(meta["date"], "%Y-%m-%d")
        ET.SubElement(item, "pubDate").text = pubdate.strftime(
            "%a, %d %b %Y %H:%M:%S +0000"
        )

        desc = ET.SubElement(item, "description")
        desc.text = meta.get("desc", meta["title"])
        content_el = ET.SubElement(
            item, "{http://purl.org/rss/1.0/modules/content/}encoded"
        )
        content_el.text = f"<![CDATA[{html_content}]]>"

    tree = ET.ElementTree(rss)
    tree.write(RSS_FILE, encoding="utf-8", xml_declaration=True)


def main():
    posts_info = []
    for md_file in SRC_DIR.glob("*.md"):
        result = read_post(md_file)
        if result:
            meta, html_content = result
            meta["src_filename"] = md_file.name
            posts_info.append((meta, html_content))
    posts_info.sort(
        key=lambda x: datetime.strptime(x[0]["date"], "%Y-%m-%d"), reverse=True
    )
    build_index(posts_info)
    build_post_files(posts_info)
    build_rss(posts_info)


if __name__ == "__main__":
    main()
