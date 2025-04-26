# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: orangc
import re, toml, mistune, pygments, pathlib
from bs4 import BeautifulSoup
from datetime import datetime
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html

SRC_DIR = pathlib.Path("src")
NOTES_DIR = pathlib.Path("notes")
TEMPLATE_FILE = pathlib.Path("template.html")
INDEX_FILE = pathlib.Path("index.html")

class HighlightRenderer(mistune.HTMLRenderer):
    def block_code(self, code, info=None):
        if info:
            lexer = get_lexer_by_name(info, stripall=True)
            formatter = html.HtmlFormatter()
            return pygments.highlight(code, lexer, formatter)
        return "<pre><code>" + mistune.escape(code) + "</code></pre>"
    
    def heading(self, text, level):
        slug = re.sub(r'[^a-zA-Z0-9 ]', '', text).lower().replace(' ', '-')
        return f'''<h{level} id="{slug}" onclick="navigator.clipboard.writeText(location.href.split('#')[0] + '#{slug}')"> {text} </h{level}>'''

md_parser = mistune.create_markdown(
    renderer=HighlightRenderer(),
    plugins=["spoiler", "footnotes", "url", "task_lists", "abbr", "superscript", "subscript", "table", "strikethrough"]
)

def format_date(date_str):
    dt = datetime.strptime(date_str, "%d.%m.%Y")
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
    return meta, md_parser(body)

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
        formatted_date, datetime_attr = format_date(meta["date"])
        li = soup.new_tag("li")
        filename = meta["src_filename"].replace(".md", ".html")
        a = soup.new_tag("a", attrs={"class": "link2 me-2", "href": f"notes/{filename}"})
        a.string = meta["title"]
        time_tag = soup.new_tag("time", attrs={"class": "text-base-content/70 italic", "datetime": datetime_attr},)
        time_tag.string = formatted_date
        li.append(a); li.append(" ")
        li.append(time_tag)
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
        time_element = f'<time class="text-base-content/70 italic" datetime="{datetime_attr}">{formatted_date}</time>'
        post_html = template.replace("{{ title }}", meta["title"])
        post_html = post_html.replace("{{ short_desc }}", meta["short_desc"])
        post_html = post_html.replace("{{ date }}", time_element)
        post_html = post_html.replace("{{ post-content }}", html_content)
        output_filename = posts_info[i][0]["src_filename"].replace(".md", ".html")
        output_path = NOTES_DIR / output_filename
        write_html(output_path, post_html)

def main():
    posts_info = []
    for md_file in SRC_DIR.glob("*.md"):
        result = read_post(md_file)
        if result:
            meta, html_content = result
            meta["src_filename"] = md_file.name
            posts_info.append((meta, html_content))
    posts_info.sort(key=lambda x: datetime.strptime(x[0]["date"], "%d.%m.%Y"), reverse=True)
    build_index(posts_info)
    build_post_files(posts_info)

if __name__ == "__main__":
    main()