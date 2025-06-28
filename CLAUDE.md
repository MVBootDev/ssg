# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Static Site Generator (SSG) project written in Python. It's a learning project following Boot.dev curriculum, focusing on building a markdown-to-HTML static site generator.

**IMPORTANT LEARNING CONTEXT**: This is a student project exercise for boot.dev platform. New instructions are provided sequentially in `/lessons/` directory. The goal is to provide guidance and hints while allowing the student to write the code themselves - do NOT provide complete code solutions or answers directly.

## Development Commands

- **Run the application**: `./main.sh` or `python3 src/main.py`
- **Make main.sh executable**: `chmod +x main.sh`

## Architecture

### Core Components

- `src/main.py` - Entry point for the application
- `src/textnode.py` - Contains TextNode class and TextType enum for representing inline text elements
- `main.sh` - Shell script to run the Python application
- `lessons/` - Contains lesson materials and instructions
- `public/` - Static HTML/CSS files (sample content)

### TextNode System

The project uses a TextNode system to represent different types of inline text:
- Plain text
- Bold text (**bold**)
- Italic text (_italic_)
- Code text (`code`)
- Links [anchor](url)
- Images ![alt](url)

The TextNode class has three properties:
- `text` - The text content
- `text_type` - Member of TextType enum
- `url` - URL for links/images (defaults to None)

## File Structure

```
ssg/
├── src/
│   ├── main.py          # Main application entry
│   └── textnode.py      # TextNode class and TextType enum
├── public/              # Static files (HTML/CSS samples)
├── lessons/             # Course materials
├── main.sh              # Run script
└── .gitignore           # Excludes __pycache__/
```

## SSG Architecture Overview

The complete system flow will be:
1. Markdown files in `/content` directory + `template.html` file in root
2. Python SSG code in `src/` reads markdown and template files
3. Generator converts markdown to HTML files in `/public` directory
4. Python HTTP server serves `/public` content on localhost:8888

### Core Processing Steps
1. Delete everything in `/public` directory
2. Copy static assets to `/public`  
3. For each markdown file in `/content`:
   - Read file contents
   - Split markdown into blocks (paragraphs, headings, lists)
   - Convert blocks to HTMLNode tree: Raw markdown → TextNode → HTMLNode
   - Use recursive `to_html()` method to generate HTML string
   - Inject into template and write to `/public`

## Notes

- This is a Python-based project with no external dependencies currently
- Uses Python 3 standard library (enum module for TextType)
- Project builds components individually with unit tests before final integration
- Development approach: solve individual problems first, then assemble into working program