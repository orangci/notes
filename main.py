# SPDX-License-Identifier: AGPL-3.0-or-later
import asyncio, os, re, shutil, aiofiles, toml, mistune, pygments, pathlib
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


md_parser = mistune.create_markdown(
    renderer=HighlightRenderer(),
    plugins=["spoiler", "footnotes", "url", "task_lists", "abbr", "superscript", "subscript", "table", "strikethrough"]
)


def format_date(date_str):
    dt = datetime.strptime(date_str, "%d.%m.%Y")
    return dt.strftime("%B %d, %Y"), dt.strftime("%Y-%m-%d")

async def read_post(file_path):
    async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
        content = await f.read()
    meta_match = re.match(r"\+\+\+(.+?)\+\+\+", content, re.DOTALL)
    if not meta_match:
        print(f"Skipping {file_path.name}: it appears this file has no metadata set.")
        return None
    meta = toml.loads(meta_match.group(1).strip())
    body = content[meta_match.end() :].strip()
    return meta, md_parser(body)


async def write_html(file_path, content):
    async with aiofiles.open(file_path, "w", encoding="utf-8") as f:
        await f.write(content)

async def build_index(posts_info):
    async with aiofiles.open(INDEX_FILE, "r", encoding="utf-8") as f:
        html = await f.read()
    soup = BeautifulSoup(html, "html.parser")
    posts_list = soup.select_one("#posts-list")
    posts_list.clear()
    for meta, _ in posts_info:
        formatted_date, datetime_attr = format_date(meta["date"])
        li = soup.new_tag("li")
        filename = f"{meta['title'].lower().replace(' ', '-')}.html"
        a = soup.new_tag("a", attrs={"class": "link2 me-2", "href": f"./notes/{filename}"})
        a.string = meta["title"]
        time_tag = soup.new_tag("time", attrs={"class": "text-base-content/70 italic", "datetime": datetime_attr},)
        time_tag.string = formatted_date
        li.append(a)
        li.append(" ")
        li.append(time_tag)
        posts_list.append(li)
    async with aiofiles.open(INDEX_FILE, "w", encoding="utf-8") as f:
        await f.write(str(soup))

async def build_post_files(posts_info):
    for file in NOTES_DIR.iterdir():
        if file.name != "template.html" and file.is_file():
            file.unlink()
    async with aiofiles.open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        template = await f.read()
    for i, (meta, html_content) in enumerate(posts_info):
        formatted_date, datetime_attr = format_date(meta["date"])
        time_element = f'<time class="text-base-content/70 italic" datetime="{datetime_attr}">{formatted_date}</time>'
        post_html = template.replace("{{ title }}", meta["title"])
        post_html = post_html.replace("{{ short_desc }}", meta["short_desc"])
        post_html = post_html.replace("{{ date }}", time_element)
        post_html = post_html.replace("{{ post-content }}", html_content)
        filename = SRC_DIR / f"{meta['title'].lower().replace(' ', '-')}.md"
        output_filename = filename.name.replace(".md", ".html")
        output_path = NOTES_DIR / output_filename
        await write_html(output_path, post_html)


async def main():
    posts_info = []
    for md_file in SRC_DIR.glob("*.md"):
        result = await read_post(md_file)
        if result:
            posts_info.append(result)
    posts_info.sort(key=lambda x: datetime.strptime(x[0]["date"], "%d.%m.%Y"), reverse=True)
    await asyncio.gather(build_index(posts_info), build_post_files(posts_info))


if __name__ == "__main__":
    asyncio.run(main())
