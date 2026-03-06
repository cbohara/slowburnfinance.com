#!/usr/bin/env python3
"""
build.py — Static site generator for Slow Burn Finance.

Reads markdown posts from content/posts/, renders them through Jinja2 templates,
and outputs a fully static site to output/.

Usage:
    python build.py
    python -m http.server -d output   # preview locally
"""

import os
import shutil
from pathlib import Path

import frontmatter
import markdown
from jinja2 import Environment, FileSystemLoader

# Paths
ROOT = Path(__file__).parent
CONTENT_DIR = ROOT / "content" / "posts"
TEMPLATE_DIR = ROOT / "templates"
STATIC_DIR = ROOT / "static"
OUTPUT_DIR = ROOT / "output"

# Markdown extensions for nicer rendering
MD_EXTENSIONS = ["fenced_code", "tables", "smarty", "toc", "attr_list"]


def load_posts():
    """Load all markdown posts, parse frontmatter, convert to HTML."""
    posts = []
    for md_file in sorted(CONTENT_DIR.glob("*.md")):
        post = frontmatter.load(md_file)
        html_content = markdown.markdown(post.content, extensions=MD_EXTENSIONS)
        posts.append(
            {
                "title": post.get("title", md_file.stem.replace("-", " ").title()),
                "date": post.get("date"),
                "excerpt": post.get("excerpt", ""),
                "slug": md_file.stem,
                "content": html_content,
                "url": f"/posts/{md_file.stem}/",
            }
        )
    # Sort by date, newest first
    posts.sort(key=lambda p: p["date"] or "", reverse=True)
    return posts


def build():
    """Build the entire site."""
    # Clean output
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)

    # Set up Jinja2
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

    # Load posts
    posts = load_posts()

    # --- Render landing page ---
    index_template = env.get_template("index.html")
    index_html = index_template.render(posts=posts, current_page="home")
    (OUTPUT_DIR / "index.html").write_text(index_html)

    # --- Render blog listing ---
    blog_dir = OUTPUT_DIR / "blog"
    blog_dir.mkdir()
    blog_template = env.get_template("blog.html")
    blog_html = blog_template.render(posts=posts, current_page="blog")
    (blog_dir / "index.html").write_text(blog_html)

    # --- Render each post ---
    post_template = env.get_template("post.html")
    for post in posts:
        post_dir = OUTPUT_DIR / "posts" / post["slug"]
        post_dir.mkdir(parents=True)
        post_html = post_template.render(post=post, current_page="blog")
        (post_dir / "index.html").write_text(post_html)

    # --- Copy static assets ---
    if STATIC_DIR.exists():
        for item in STATIC_DIR.iterdir():
            dest = OUTPUT_DIR / item.name
            if item.is_dir():
                shutil.copytree(item, dest)
            else:
                shutil.copy2(item, dest)

    # --- Copy CNAME and .nojekyll for GitHub Pages ---
    for f in ["CNAME", ".nojekyll"]:
        src = ROOT / f
        if src.exists():
            shutil.copy2(src, OUTPUT_DIR / f)

    print(f"✓ Built {len(posts)} post(s) → {OUTPUT_DIR}/")
    print(f"  Preview: python -m http.server -d {OUTPUT_DIR}")


if __name__ == "__main__":
    build()
