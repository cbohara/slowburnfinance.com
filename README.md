# slowburnfinance.com

A personal finance blog. Patient money. Intentional life.

Built with a Python static site generator — write posts in markdown, build to HTML, deploy to GitHub Pages.

## Local Development

```bash
# First time setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Build the site
python build.py

# Preview locally at http://localhost:8000
python -m http.server -d output
```

## Writing a New Post

Create a markdown file in `content/posts/`:

```markdown
---
title: "Your Post Title"
date: 2026-03-15
excerpt: "A one-line summary for the blog listing."
---

Your post content here...
```

Then rebuild:

```bash
python build.py
```

## Deployment

Handled automatically — push to `main` and the GitHub Action builds and deploys to GitHub Pages.

## Stack

- **Build**: Python (`markdown`, `Jinja2`, `python-frontmatter`)
- **Templates**: Jinja2 (`templates/`)
- **Styles**: Vanilla CSS (`static/css/style.css`)
- **Email signup**: [Buttondown](https://buttondown.com/slowburnfinance)
- **Hosting**: GitHub Pages
