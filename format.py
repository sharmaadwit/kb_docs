import re

with open("Retail & CPG Success Stories Library_2024.md", "r") as f:
    content = f.read()

# Make the first title H1
if content.startswith("# "):
    pass
else:
    # remove the existing '# Presentation: ' or similar
    content = re.sub(r"^# Presentation: (.*?\.pptx)", r"# \1", content)
    
# Remove slide indicators
content = re.sub(r"## Slide \d+\n+", "", content)
content = re.sub(r"‹#›\n+", "", content)

# Remove hr
content = re.sub(r"---\n+", "", content)

with open("kb/Retail & CPG Success Stories Library_2024.md", "w") as f:
    f.write(content)
