#!/usr/bin/env python3
"""
Regenerate kb_chunks.jsonl from all markdown files in kb/ folder.
Handles chunking and section parsing.
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def parse_markdown_sections(content: str, file_path: str) -> List[Dict]:
    """Parse markdown content into sections with headers."""
    lines = content.split('\n')
    sections = []
    current_section = {
        'heading': '',
        'heading_path': [],
        'section': 0,
        'text_lines': []
    }
    heading_stack = []
    section_counter = 0

    for i, line in enumerate(lines):
        # Check for markdown headers
        if line.startswith('#'):
            # Save previous section if it has content
            if current_section['text_lines']:
                text = '\n'.join(current_section['text_lines']).strip()
                if text:
                    section_counter += 1
                    sections.append({
                        'section': section_counter,
                        'heading': current_section['heading'],
                        'heading_path': current_section['heading_path'].copy(),
                        'text': text,
                        'line_start': i - len(current_section['text_lines'])
                    })
                current_section['text_lines'] = []

            # Parse header level and text
            level = len(line) - len(line.lstrip('#'))
            heading_text = line[level:].strip()

            # Update heading stack
            heading_stack = heading_stack[:level-1]
            heading_stack.append(heading_text)

            current_section['heading'] = heading_text
            current_section['heading_path'] = heading_stack.copy()

        elif line.strip() or current_section['text_lines']:
            current_section['text_lines'].append(line)

    # Save last section
    if current_section['text_lines']:
        text = '\n'.join(current_section['text_lines']).strip()
        if text:
            section_counter += 1
            sections.append({
                'section': section_counter,
                'heading': current_section['heading'],
                'heading_path': current_section['heading_path'].copy(),
                'text': text,
            })

    return sections


def chunk_text(text: str, max_chunk_size: int = 1000) -> List[str]:
    """Split text into chunks."""
    if len(text) <= max_chunk_size:
        return [text]

    chunks = []
    current_chunk = ""

    paragraphs = text.split('\n\n')
    for para in paragraphs:
        if len(current_chunk) + len(para) + 2 > max_chunk_size:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = para
        else:
            if current_chunk:
                current_chunk += '\n\n'
            current_chunk += para

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def process_kb_files(kb_dir: Path) -> List[Dict]:
    """Process all markdown files in kb/ directory."""
    chunks_list = []
    chunk_id = 0

    # Find all markdown files
    md_files = sorted(kb_dir.rglob('*.md'))

    for md_file in md_files:
        # Skip non-golden files
        if not md_file.read_text().startswith('<!--'):
            rel_path = md_file.relative_to(kb_dir)
            if 'kb-golden' not in md_file.read_text()[:100]:
                print(f"⚠️  Skipping non-golden: {rel_path}")
                continue

        rel_path = md_file.relative_to(kb_dir)
        print(f"Processing: {rel_path}")

        try:
            content = md_file.read_text(encoding='utf-8')

            # Remove the kb-golden marker
            lines = content.split('\n')
            if lines[0].startswith('<!--'):
                lines = lines[1:]
                content = '\n'.join(lines).lstrip()

            # Parse sections
            sections = parse_markdown_sections(content, str(rel_path))

            for section_idx, section in enumerate(sections):
                # Chunk the section text
                text_chunks = chunk_text(section['text'])

                for chunk_idx, chunk_text_content in enumerate(text_chunks):
                    chunk_id += 1
                    chunk_record = {
                        'id': f"{rel_path}::chunk_{chunk_id}",
                        'source': str(rel_path),
                        'chunk': chunk_idx,
                        'section': section['section'],
                        'heading': section['heading'],
                        'heading_path': section['heading_path'],
                        'section_type': 'reference',
                        'is_reference': True,
                        'local_chunk': chunk_idx,
                        'text': chunk_text_content
                    }
                    chunks_list.append(chunk_record)

        except Exception as e:
            print(f"ERROR processing {rel_path}: {e}")
            continue

    return chunks_list


def main():
    repo_root = Path(__file__).resolve().parents[2]
    kb_dir = repo_root / 'kb'
    chunks_output = repo_root / 'kb' / 'kb_chunks.jsonl'

    print("=" * 80)
    print("REGENERATE KB CHUNKS")
    print("=" * 80)
    print(f"KB directory: {kb_dir}")
    print(f"Output: {chunks_output}")
    print()

    if not kb_dir.exists():
        print(f"ERROR: KB directory not found: {kb_dir}")
        return 1

    # Process all KB files
    chunks = process_kb_files(kb_dir)

    print(f"\nGenerated {len(chunks)} chunks from {len(list(kb_dir.glob('**/*.md')))} markdown files")

    # Write to JSONL
    with open(chunks_output, 'w') as f:
        for chunk in chunks:
            f.write(json.dumps(chunk) + '\n')

    print(f"✓ Wrote {len(chunks)} chunks to {chunks_output}")
    print("\n" + "=" * 80)
    return 0


if __name__ == '__main__':
    sys.exit(main())
