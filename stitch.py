import os

files_to_stitch = [
    '01_PRD.md',
    '03_API_SPECIFICATION.md',
    'clearpath-ai-prototype/src/App.jsx',
    'clearpath-ai-prototype/src/components/Dashboard.jsx',
    'nyapath-backend/main.py',
    'nyapath-backend/rag_engine.py',
    'nyapath-backend/audit_engine.py',
    'nyapath-backend/chat_engine.py',
    'nyapath-backend/schemes_engine.py'
]

with open('cursor_context.txt', 'w', encoding='utf-8') as out:
    out.write('# NYAPATH - SIH 2026 STITCHED CODEBASE FOR CURSOR\n\n')
    out.write('This file contains the core frontend and backend logic, fully wired and functional. Use this context to continue development, polish UI, or refactor.\n\n')
    
    for path in files_to_stitch:
        if os.path.exists(path):
            out.write('\n\n' + '='*50 + '\n')
            out.write('FILE: ' + path + '\n')
            out.write('='*50 + '\n\n')
            with open(path, 'r', encoding='utf-8') as f:
                out.write(f.read())
        else:
            out.write('\n\n[FILE NOT FOUND: ' + path + ']\n')
