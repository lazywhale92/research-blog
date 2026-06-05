#!/usr/bin/env python3
"""Lightweight public-content and generated-site guardrails for the research blog."""
from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {'.md', '.html', '.yml', '.yaml', '.css', '.txt'}
POSTS = ROOT / '_posts'
SITE = ROOT / '_site'

FORBIDDEN_PATTERNS = [
    (re.compile(r'/Users/ms\b'), 'local absolute user path'),
    (re.compile(r'agent-work-log/raw', re.I), 'private raw work-log path'),
    (re.compile(r'raw/kakaotalk', re.I), 'private chat raw path'),
    (re.compile(r'kakao_chat', re.I), 'private chat transcript identifier'),
    (re.compile(r'interpark', re.I), 'company identifier'),
    (re.compile(r'work@interpark\.com', re.I), 'company account'),
]

REQUIRED_FRONTMATTER = {
    'title', 'date', 'layout', 'status', 'topic', 'tags', 'summary',
    'public_safety', 'source_visibility', 'repo_artifacts'
}


def public_files():
    for path in ROOT.rglob('*'):
        if not path.is_file():
            continue
        if any(part in {'.git', '_site', 'vendor', '.bundle'} for part in path.parts):
            continue
        yield path


def text_files():
    for path in public_files():
        if path.suffix in TEXT_SUFFIXES or path.name in {'Gemfile', 'Gemfile.lock', 'README.md'}:
            yield path


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding='utf-8')
    if not text.startswith('---\n'):
        raise ValueError(f'{path.relative_to(ROOT)} missing YAML frontmatter')
    end = text.find('\n---\n', 4)
    if end == -1:
        raise ValueError(f'{path.relative_to(ROOT)} missing closing YAML frontmatter')
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ':' in line and not line.startswith(' '):
            key, value = line.split(':', 1)
            fields[key.strip()] = value.strip()
    return fields


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.refs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        if tag == 'a' and attr.get('href'):
            self.refs.append(attr['href'] or '')
        if tag == 'link' and attr.get('href'):
            self.refs.append(attr['href'] or '')
        if tag == 'script' and attr.get('src'):
            self.refs.append(attr['src'] or '')
        if tag == 'img' and attr.get('src'):
            self.refs.append(attr['src'] or '')


def validate_generated_links(errors: list[str]) -> None:
    if not SITE.exists():
        return
    for html in SITE.rglob('*.html'):
        parser = LinkParser()
        parser.feed(html.read_text(encoding='utf-8', errors='ignore'))
        for ref in parser.refs:
            if ref.startswith(('http://', 'https://', 'mailto:', '#')):
                continue
            rel = ref[len('/research-blog'):] if ref.startswith('/research-blog') else ref
            rel = rel.split('#', 1)[0].split('?', 1)[0]
            if not rel or rel == '/':
                target = SITE / 'index.html'
            elif rel.endswith('/'):
                target = SITE / rel.lstrip('/') / 'index.html'
            else:
                target = SITE / rel.lstrip('/')
            if not target.exists():
                errors.append(f'{html.relative_to(SITE)} references missing generated asset/link {ref}')


def main() -> int:
    errors: list[str] = []
    for path in text_files():
        text = path.read_text(encoding='utf-8', errors='ignore')
        for pattern, label in FORBIDDEN_PATTERNS:
            if pattern.search(text):
                errors.append(f'{path.relative_to(ROOT)} contains forbidden {label}')

    for post in sorted(POSTS.glob('*.md')):
        try:
            fields = parse_frontmatter(post)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        text = post.read_text(encoding='utf-8')
        missing = sorted(REQUIRED_FRONTMATTER - fields.keys())
        if missing:
            errors.append(f'{post.relative_to(ROOT)} missing frontmatter fields: {", ".join(missing)}')
        if fields.get('layout', '').strip('"') != 'paper-note':
            errors.append(f'{post.relative_to(ROOT)} layout must be paper-note')
        if fields.get('public_safety', '').strip('"') != 'reviewed':
            errors.append(f'{post.relative_to(ROOT)} public_safety must be reviewed before commit')
        if fields.get('source_visibility', '').strip('"') not in {'public-only', 'private-sanitized'}:
            errors.append(f'{post.relative_to(ROOT)} source_visibility must be public-only or private-sanitized')
        status = fields.get('status', '').strip('"')
        if status not in {'draft', 'published', 'corrected'}:
            errors.append(f'{post.relative_to(ROOT)} invalid status: {status}')
        if status not in {'published', 'corrected'} and 'published: false' not in text:
            errors.append(f'{post.relative_to(ROOT)} non-public status must include published: false to avoid direct public rendering')

    validate_generated_links(errors)

    if errors:
        for error in errors:
            print(f'ERROR: {error}', file=sys.stderr)
        return 1
    print('content validation passed')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
