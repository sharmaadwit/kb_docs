import sys
import re

def get_contextual_heading(text_block):
    lines = [line.strip() for line in text_block.split('\n') if line.strip()]
    if not lines:
        return "Untitled Slide"
    
    # Heuristic 1: If there's an H3, use it
    for line in lines:
        if line.startswith('### '):
            return line.replace('###', '').strip()

    # Heuristic 2: Find the first line that is short enough and doesn't look like a stat
    for line in lines:
        # Ignore numbers like "1.7X", "$ 500,000", "4X"
        if len(line) < 120 and not re.match(r'^[\d\$\.\%\+X\s]+$', line, re.IGNORECASE) and not line.startswith('|') and not line.startswith('www'):
            return line[:100] + '...' if len(line) > 100 else line
            
    # Fallback
    for line in lines:
        if line and not line.startswith('|'):
            return line[:60] + '...' if len(line) > 60 else line
            
    return "Data Slide"

def process_file(filepath, new_h1):
    print(f"Processing {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by slide marker
    slides = re.split(r'\n## Slide \d+\n\n', content)
    if len(slides) == 1:
        slides = re.split(r'\n## Slide \d+\n', content)
        if len(slides) == 1:
            print(f"No slides found in {filepath}.")
            return

    # Replace H1
    header = slides[0]
    header = re.sub(r'^# .*', f'# {new_h1}', header)
    
    new_content = [header]
    
    for slide_text in slides[1:]:
        heading = get_contextual_heading(slide_text)
        new_content.append(f"\n## {heading}\n\n{slide_text}")
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("".join(new_content))
    print(f"Done processing {filepath}")

if __name__ == "__main__":
    process_file("kb/BFSI Success Stories Library_2024.md", "BFSI Success Stories Library 2024")
    process_file("kb/Retail & CPG Success Stories Library_2024.md", "Retail & CPG Success Stories Library 2024")
