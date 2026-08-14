#!/usr/bin/env python3
"""
Phase 2 Consulting Content JSONL Generator
Converts markdown files to JSONL chunks with consulting intent tag
"""

import json
import os
from pathlib import Path
from datetime import datetime

def extract_sections(content, filename):
    """Extract sections from markdown content"""
    lines = content.split('\n')
    sections = []
    current_heading = "Overview"
    current_section = []
    heading_level = 0

    for line in lines:
        if line.startswith('#'):
            # Save previous section if exists
            if current_section and current_section[0].strip():
                section_text = '\n'.join(current_section).strip()
                if section_text:
                    sections.append({
                        'heading': current_heading,
                        'text': section_text
                    })
            # Start new section
            level = len(line) - len(line.lstrip('#'))
            current_heading = line.lstrip('#').strip()
            heading_level = level
            current_section = [line]
        else:
            current_section.append(line)

    # Save final section
    if current_section and current_section[0].strip():
        section_text = '\n'.join(current_section).strip()
        if section_text:
            sections.append({
                'heading': current_heading,
                'text': section_text
            })

    return sections

def get_category(filename):
    """Extract category from filename"""
    if 'channels' in filename:
        return 'Channels'
    elif 'agent-assist' in filename:
        return 'Agent Assist'
    elif 'campaign' in filename:
        return 'Campaign Manager'
    return 'Consulting'

def generate_chunks(markdown_files):
    """Generate JSONL chunks from markdown files"""
    chunks = []
    chunk_counter = 0
    update_date = datetime.now().strftime('%Y-%m-%d')

    for filepath in sorted(markdown_files):
        filename = os.path.basename(filepath)
        category = get_category(filename)

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            sections = extract_sections(content, filename)

            # Get title from first heading
            title = filename.replace('.md', '').replace('-', ' ').title()

            for section_idx, section in enumerate(sections):
                chunk_id = f"kb/{filename}::chunk_{section_idx}"

                chunk_obj = {
                    "id": chunk_id,
                    "source": f"kb/{filename}",
                    "chunk": section_idx,
                    "section": section_idx + 1,
                    "heading": section['heading'],
                    "heading_path": [title, section['heading']],
                    "section_type": "consulting",
                    "is_reference": False,
                    "local_chunk": section_idx,
                    "text": section['text'],
                    "version": "2.0",
                    "update_date": update_date,
                    "intent": "consulting",
                    "audience_level": "intermediate",
                    "category": category
                }

                chunks.append(chunk_obj)
                chunk_counter += 1

        except Exception as e:
            print(f"Error processing {filename}: {e}")
            continue

    return chunks

def validate_jsonl(chunks):
    """Validate JSONL format"""
    valid_count = 0
    errors = []

    for idx, chunk in enumerate(chunks):
        try:
            json_str = json.dumps(chunk)
            valid_count += 1
        except Exception as e:
            errors.append(f"Chunk {idx}: {e}")

    return {
        'total': len(chunks),
        'valid': valid_count,
        'invalid': len(errors),
        'errors': errors,
        'valid': valid_count == len(chunks)
    }

def main():
    base_path = Path('/Users/adwit.sharma/kb_docs')

    # Find Phase 2 markdown files
    phase2_files = []
    for pattern in ['*channels*.md', '*agent-assist*.md', '*campaign*.md']:
        phase2_files.extend(base_path.glob(pattern))

    # Filter to root directory only
    phase2_files = [f for f in phase2_files if f.parent == base_path]
    phase2_files.sort()

    print(f"Found {len(phase2_files)} Phase 2 markdown files:")
    for f in phase2_files:
        print(f"  - {f.name}")

    # Generate chunks
    print("\nGenerating JSONL chunks...")
    chunks = generate_chunks(phase2_files)

    print(f"Generated {len(chunks)} chunks")

    # Validate
    validation = validate_jsonl(chunks)
    print(f"\nValidation: {validation['valid']}/{validation['total']} chunks valid")

    if validation['errors']:
        print("Errors found:")
        for err in validation['errors']:
            print(f"  - {err}")

    # Get current JSONL count
    jsonl_path = base_path / 'kb' / 'kb_chunks.jsonl'
    if jsonl_path.exists():
        with open(jsonl_path, 'r') as f:
            current_lines = len(f.readlines())
    else:
        current_lines = 0

    # Append to JSONL
    print(f"\nAppending {len(chunks)} chunks to kb_chunks.jsonl...")
    with open(jsonl_path, 'a') as f:
        for chunk in chunks:
            f.write(json.dumps(chunk) + '\n')

    # Verify
    with open(jsonl_path, 'r') as f:
        final_lines = len(f.readlines())

    print(f"\nDeployment Summary:")
    print(f"  Total chunks before: {current_lines}")
    print(f"  New chunks added: {len(chunks)}")
    print(f"  Total chunks after: {final_lines}")
    print(f"  Expected after: {current_lines + len(chunks)}")
    print(f"  Validation: {'PASSED' if validation['valid'] else 'FAILED'}")
    print(f"  Files updated: kb/kb_chunks.jsonl")

    return {
        'chunks_added': len(chunks),
        'total_before': current_lines,
        'total_after': final_lines,
        'validation_passed': validation['valid'],
        'markdown_files': len(phase2_files)
    }

if __name__ == '__main__':
    result = main()
    print(f"\nResult: {json.dumps(result, indent=2)}")
