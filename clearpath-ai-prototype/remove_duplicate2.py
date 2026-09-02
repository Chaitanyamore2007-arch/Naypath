import re

with open("src/components/Dashboard.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# There are two <div className="mt-6">... Schedule Inspection ... </div> blocks.
# Let's find all occurrences of `<div className="mt-6">` that contain `Schedule Inspection`.
parts = content.split('<div className="mt-6">')
# The first part is everything before the first `<div className="mt-6">`.
# We want to remove the first `<div className="mt-6">` that contains `Schedule Inspection` 
# up to the matching `</div>`. Wait, since the block has nested divs, this is tricky.

# Better: the duplicate block is exactly between "Required Documents" list end and "AI Risk Analysis" start.
# Let's use regex to find the block between those two.

pattern = re.compile(r'(<ul className="space-y-2">\s*\{\s*details\.documents.*?</ul>\s*</div>)\s*<div className="mt-6">.*?Schedule Inspection.*?</button>\s*</div>\s*</div>\s*</div>\s*<div>\s*<h3 className="text-sm font-bold text-\[\#C6742B\]', re.DOTALL)

def repl(match):
    return match.group(1) + '\n                    <div>\n                      <h3 className="text-sm font-bold text-[#C6742B]'

content = pattern.sub(repl, content)

with open("src/components/Dashboard.jsx", "w", encoding="utf-8") as f:
    f.write(content)
