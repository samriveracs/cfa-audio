#!/bin/bash
# Rebuild feed from rendered audio, commit and push if anything changed.
set -e
cd /home/claude/cfa-audio
python3 /home/claude/podcast/bin/build_site.py
python3 -c "import xml.dom.minidom as m; m.parse('feed.xml')"
git add -A
if git diff --cached --quiet; then echo "nothing new"; exit 0; fi
n=$(grep -c "<item>" feed.xml)
git -c user.name="samriveracs" -c user.email="samriveracs@users.noreply.github.com" commit -q -m "Update feed: $n episodes

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_012Df4mDby1mCKyF89sF67Vm"
git push -q origin main
echo "pushed $n episodes"
