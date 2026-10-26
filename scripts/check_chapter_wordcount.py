#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chapter word count checker
Counts the words in a chapter file and reports whether it meets the minimum.

Usage:
  python check_chapter_wordcount.py <chapter file> [min_words] [--json]
  python check_chapter_wordcount.py --all <directory> [min_words] [--json]

Exit codes:
  0 = all chapters pass
  1 = some chapters are under the minimum
  2 = file/directory/argument error

--json: output machine-readable JSON (for agents to parse and act on);
        on error output {"error": "..."}; summary.errors counts missing files
"""

import json
import os
import re
import sys
from pathlib import Path

# Fix Windows console encoding issues
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def count_words(text: str) -> int:
    """Count the number of words (whitespace-separated tokens) in English text.

    Markdown markers are stripped first, then the remaining non-empty lines are
    split on whitespace. The count is the total number of tokens.
    """
    # Strip Markdown markers
    text = re.sub(r'#{1,6}\s*', '', text)        # headings
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # bold
    text = re.sub(r'\*(.*?)\*', r'\1', text)     # italic
    text = re.sub(r'~~(.*?)~~', r'\1', text)     # strikethrough
    text = re.sub(r'`(.*?)`', r'\1', text)       # inline code
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)  # links (keep link text)

    # Count whitespace-separated tokens across non-empty lines
    words = 0
    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue  # exclude empty lines
        words += len(line.split())
    return words


def extract_content_from_chapter(file_path: Path) -> str:
    """Extract the body text from a chapter file.

    Chapters are named 'Chapter-XX-<title>.md'. Body text starts after the first
    heading line matching /^#+ Chapter (\\d+)/i (or the first line starting with
    '#' that contains the word 'Chapter'). Everything after that heading is sampled.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')

    # Skip leading frontmatter/metadata up to and including the chapter heading
    content_start = 0
    chapter_heading_re = re.compile(r'^#+\s*Chapter\s+(\d+)', re.IGNORECASE)
    for i, line in enumerate(lines):
        if chapter_heading_re.match(line) or (
            line.startswith('#') and 'chapter' in line.lower()
        ):
            content_start = i + 1
            break

    return '\n'.join(lines[content_start:])


def check_chapter(file_path: str, min_words: int = 1500) -> dict:
    """Check the word count of a single chapter."""
    path = Path(file_path)

    if not path.exists():
        return {
            'file': str(path),
            'exists': False,
            'word_count': 0,
            'status': 'error',
            'message': f'File not found: {file_path}'
        }

    main_content = extract_content_from_chapter(path)
    word_count = count_words(main_content)

    status = 'pass' if word_count >= min_words else 'fail'
    message = f'Words: {word_count}' + (
        f' (✓ meets requirement)' if word_count >= min_words
        else f' (✗ under minimum, needs at least {min_words} words)'
    )

    return {
        'file': str(path),
        'exists': True,
        'word_count': word_count,
        'status': status,
        'message': message
    }


def chapter_sort_key(path: Path):
    """Sort by chapter number numerically (extract \\d+ from 'Chapter-NN'),
    falling back to name order."""
    m = re.search(r'Chapter-(\d+)', path.name, re.IGNORECASE)
    if m:
        try:
            return (int(m.group(1)), path.name)
        except ValueError:
            pass
    return (9999, path.name)


def check_all_chapters(directory: str, pattern: str = 'Chapter-*.md', min_words: int = 1500):
    """Check all matching chapter files in a directory. Returns (results, error_message)."""
    dir_path = Path(directory)
    if not dir_path.exists():
        return [], f'Directory does not exist - {directory}'
    if not dir_path.is_dir():
        return [], f'Path is not a directory - {directory}'

    chapter_files = sorted(dir_path.glob(pattern), key=chapter_sort_key)
    if not chapter_files:
        return [], f'No chapter files found in directory (pattern: {pattern})'

    results = [check_chapter(str(chapter_file), min_words) for chapter_file in chapter_files]
    return results, None


def print_results(results: list, min_words: int = 1500):
    """Print the check results."""
    if not results:
        print('No chapter files found')
        return

    total_words = 0
    passed = 0
    failed = 0
    errors = 0

    print('\n' + '=' * 60)
    print('Chapter Word Count Report')
    print('=' * 60)

    for result in results:
        if not result['exists']:
            errors += 1
            print(f'\n❌ {result["file"]}')
            print(f'   {result["message"]}')
            continue

        total_words += result['word_count']
        if result['status'] == 'pass':
            passed += 1
            icon = '✅'
        else:
            failed += 1
            icon = '⚠️'

        print(f'\n{icon} {Path(result["file"]).name}')
        print(f'   {result["message"]}')

    print('\n' + '-' * 60)
    print(f'Total: {len(results)} chapters | {passed} passed | {failed} failed | '
          f'{errors} errors | total words: {total_words:,}')
    print('-' * 60)

    if failed > 0:
        print(f'\n⚠️  {failed} chapter(s) under {min_words} words. Consider expanding with:')
        print('   - Add sensory detail (environment, action, descriptions)')
        print('   - Deepen the character\'s inner life')
        print('   - Add dialogue scenes')
        print('   - Expand backstory / worldbuilding')
        print('\n   Reference: reports/content-expansion.md')


def main():
    """Main function."""
    args = [a for a in sys.argv[1:] if a != '--json']
    as_json = '--json' in sys.argv[1:]

    def emit_error(msg: str):
        """Print error in the appropriate mode and exit (code 2 = file/dir/arg error)."""
        print(json.dumps({'error': msg}, ensure_ascii=False) if as_json else msg)
        sys.exit(2)

    def parse_min_words(raw: str) -> int:
        try:
            return int(raw)
        except ValueError:
            emit_error(f'min_words must be an integer, got "{raw}"')

    min_words = 1500

    if not args:
        if as_json:
            print(json.dumps({'error': 'no arguments'}, ensure_ascii=False))
            sys.exit(2)
        print('Usage:')
        print('  Single chapter: python check_chapter_wordcount.py <chapter file> [min_words] [--json]')
        print('  All chapters:   python check_chapter_wordcount.py --all <directory> [min_words] [--json]')
        print('')
        print('Exit codes: 0=all pass  1=some chapters under min  2=file/directory/argument error')
        print('')
        print('Examples:')
        print('  python check_chapter_wordcount.py novels/Chapter-01-Opening.md')
        print('  python check_chapter_wordcount.py novels/Chapter-01-Opening.md 1800 --json')
        print('  python check_chapter_wordcount.py --all novels --json')
        sys.exit(2)

    if args[0] == '--all':
        if len(args) < 2:
            emit_error('Error: --all requires a directory path')
        directory = args[1]
        min_words = parse_min_words(args[2]) if len(args) > 2 else 1500
        results, error = check_all_chapters(directory, min_words=min_words)
        if error:
            emit_error(f'Error: {error}')
        has_error = any(not r['exists'] for r in results)
    else:
        file_path = args[0]
        min_words = parse_min_words(args[1]) if len(args) > 1 else 1500
        results = [check_chapter(file_path, min_words)]
        has_error = not results[0]['exists']

    if as_json:
        passed = sum(1 for r in results if r['exists'] and r['status'] == 'pass')
        failed = sum(1 for r in results if r['exists'] and r['status'] == 'fail')
        errors = sum(1 for r in results if not r['exists'])
        output = {
            'results': results,
            'summary': {
                'total': len(results),
                'passed': passed,
                'failed': failed,
                'errors': errors,
                'totalWords': sum(r['word_count'] for r in results),
                'minWords': min_words,
            },
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print_results(results, min_words)

    # Exit codes: 2=file/dir error, 1=some chapters under min, 0=all pass
    if has_error:
        sys.exit(2)
    if any(r['exists'] and r['status'] == 'fail' for r in results):
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()