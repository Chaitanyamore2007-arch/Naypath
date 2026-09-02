import re

with open("src/components/Dashboard.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Fix the broken div insertion
content = content.replace("        </div>`n        {/* Floating AI Chatbot */}", "        </div>\n        {/* Floating AI Chatbot */}")

with open("src/components/Dashboard.jsx", "w", encoding="utf-8") as f:
    f.write(content)
