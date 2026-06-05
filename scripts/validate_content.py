#!/usr/bin/env python3
"""Lightweight public-content and generated-site guardrails for the research blog."""
from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {'.md', '.html', '.yml', '.yaml', '.css', '.txt'}
POSTS = ROOT / '_posts'
SITE = ROOT / '_site'

# Public, generic leak patterns only. Keep private/personal denylist terms out of this public repo.
FORBIDDEN_PATTERNS = [
    (re.compile(r'/Users/[A-Za-z0-9._-]+\b'), 'local absolute user path'),
    (re.compile(r'(?<![A-Za-z0-9_-])raw/[A-Za-z0-9._/-]+', re.I), 'raw/private source path'),
    (re.compile(r'(?<![A-Za-z0-9_-])(?:jira|slack|notion)://', re.I), 'internal tool URL scheme'),
    (re.compile(r'(?:password|api[_-]?key|token|secret)\s*[:=]\s*["\']?[A-Za-z0-9_./+=-]{16,}', re.I), 'credential-like assignment'),
]

REQUIRED_FRONTMATTER = {
    'title', 'date', 'layout', 'status', 'topic', 'tags', 'summary',
    'public_safety', 'source_visibility', 'repo_artifacts'
}
ALLOWED_ARTIFACT_HOSTS = {'github.com', 'gist.github.com', 'docs.github.com', 'jekyllrb.com'}


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


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding='utf-8')
    if not text.startswith('---\n'):
        raise ValueError(f'{path.relative_to(ROOT)} missing YAML frontmatter')
    end = text.find('\n---\n', 4)
    if end == -1:
        raise ValueError(f'{path.relative_to(ROOT)} missing closing YAML frontmatter')
    yaml_text = text[4:end]
    fields: dict[str, str] = {}
    for line in yaml_text.splitlines():
        if ':' in line and not line.startswith(' '):
            key, value = line.split(':', 1)
            fields[key.strip()] = value.strip()
    return fields, yaml_text


def yaml_bool(fields: dict[str, str], key: str) -> bool | None:
    if key not in fields:
        return None
    value = fields[key].strip().strip('"\'').lower()
    if value == 'true':
        return True
    if value == 'false':
        return False
    return None


def yaml_list_values(yaml_text: str, key: str) -> list[str]:
    lines = yaml_text.splitlines()
    values: list[str] = []
    in_list = False
    for line in lines:
        if line.startswith(f'{key}:'):
            tail = line.split(':', 1)[1].strip()
            if tail.startswith('[') and tail.endswith(']'):
                inner = tail[1:-1].strip()
                if inner:
                    values.extend(part.strip().strip('"\'') for part in inner.split(','))
                in_list = False
            else:
                in_list = True
            continue
        if in_list:
            if line.startswith('  - '):
                values.append(line[4:].strip().strip('"\''))
            elif line and not line.startswith(' '):
                in_list = False
    return [value for value in values if value]


def validate_artifact_urls(path: Path, yaml_text: str, errors: list[str]) -> None:
    for url in yaml_list_values(yaml_text, 'repo_artifacts'):
        parsed = urlparse(url)
        if parsed.scheme != 'https' or not parsed.netloc:
            errors.append(f'{path.relative_to(ROOT)} repo_artifacts entry must be an https URL: {url}')
            continue
        if parsed.netloc.lower() not in ALLOWED_ARTIFACT_HOSTS:
            errors.append(f'{path.relative_to(ROOT)} repo_artifacts host is not allowlisted: {url}')


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
    if (SITE / 'scripts').exists():
        errors.append('generated site must not contain scripts/ helper sources')
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
            fields, yaml_text = parse_frontmatter(post)
        except ValueError as exc:
            errors.append(str(exc))
            continue
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
        published = yaml_bool(fields, 'published')
        if status in {'published', 'corrected'} and published is False:
            errors.append(f'{post.relative_to(ROOT)} cannot combine status {status} with published: false')
        if status not in {'published', 'corrected'} and published is not False:
            errors.append(f'{post.relative_to(ROOT)} non-public status must include frontmatter published: false')
        validate_artifact_urls(post, yaml_text, errors)

    validate_generated_links(errors)

    if errors:
        for error in errors:
            print(f'ERROR: {error}', file=sys.stderr)
        return 1
    print('content validation passed')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
