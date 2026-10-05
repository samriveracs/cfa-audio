#!/usr/bin/env python3
"""Build feed.xml, index.html and copy episode files into the repo for every rendered episode."""
import json, os, shutil, html, datetime as dt
from email.utils import format_datetime
ROOT="/home/claude/podcast"; SITE="/home/claude/cfa-audio"
BASE="https://samriveracs.github.io/cfa-audio"
VER="v2"  # default file version; audio/versions.json overrides per episode when one is re-recorded
VERS=json.load(open(f"{ROOT}/audio/versions.json")) if os.path.exists(f"{ROOT}/audio/versions.json") else {}
man=json.load(open(f"{ROOT}/manifest.json"))
os.makedirs(f"{SITE}/episodes",exist_ok=True); os.makedirs(f"{SITE}/transcripts",exist_ok=True)
if VERS: json.dump(VERS,open(f"{SITE}/tools/versions.json","w"),indent=1,sort_keys=True)
open(f"{SITE}/.nojekyll","w").close()
open(f"{SITE}/robots.txt","w").write("User-agent: *\nDisallow: /\n")
tz=dt.timezone(dt.timedelta(hours=-5))
base=dt.datetime(2026,10,3,12,0,tzinfo=tz)
def hms(s):
    s=int(round(s)); return f"{s//3600}:{s%3600//60:02d}:{s%60:02d}" if s>=3600 else f"{s//60}:{s%60:02d}"
items=[]; rows=[]; keep=set()
for e in man:
    n=e['ep']; tag=f"E{n:02d}"; meta=f"{ROOT}/audio/{tag}.json"; mp3=f"{ROOT}/audio/{tag}.mp3"
    if not (os.path.exists(meta) and os.path.exists(mp3)): continue
    info=json.load(open(meta))
    fn=f"{tag}_{VERS.get(str(n),VER)}.mp3"; keep.add(fn)
    shutil.copy2(mp3,f"{SITE}/episodes/{fn}")
    shutil.copy2(f"{ROOT}/scripts/{tag}.txt",f"{SITE}/transcripts/{tag}.txt")
    size=os.path.getsize(f"{SITE}/episodes/{fn}")
    first,last=e['modules'][0]['id'],e['modules'][-1]['id']
    span=f"Module {first}" if first==last else f"Modules {first} to {last}"
    title=f"{tag} {e['title']}"
    mods="".join(f"<li>Module {m['id']}, {html.escape(m['name'])}</li>" for m in e['modules'])
    chaps="".join(f"<li>{hms(t)} {html.escape(c)}</li>" for t,c in info['chapters'])
    desc_html=(f"<p>{html.escape(e['topic'])}, Kaplan {span}.</p><ul>{mods}</ul>"
               f"<p>Chapters</p><ul>{chaps}</ul>"
               f"<p><a href=\"{BASE}/transcripts/{tag}.txt\">Transcript</a></p>"
               "<p>Original review audio keyed to Kaplan Schweser module numbers. Not produced by Kaplan or CFA Institute.</p>")
    summary=f"{e['topic']}, Kaplan {span}. " + ", ".join(f"{m['id']} {m['name']}" for m in e['modules'])
    pub=format_datetime(base+dt.timedelta(minutes=n))
    items.append(f"""  <item>
    <title>{html.escape(title)}</title>
    <itunes:title>{html.escape(e['title'])}</itunes:title>
    <itunes:episode>{n}</itunes:episode>
    <itunes:season>{e['season']}</itunes:season>
    <podcast:season name="{html.escape(e['topic'])}">{e['season']}</podcast:season>
    <itunes:episodeType>full</itunes:episodeType>
    <description>{html.escape(summary)}</description>
    <itunes:summary>{html.escape(summary)}</itunes:summary>
    <content:encoded><![CDATA[{desc_html}]]></content:encoded>
    <enclosure url="{BASE}/episodes/{fn}" length="{size}" type="audio/mpeg"/>
    <guid isPermaLink="false">cfa-l1-audio-2026-{tag.lower()}</guid>
    <pubDate>{pub}</pubDate>
    <itunes:duration>{int(round(info['duration']))}</itunes:duration>
    <itunes:explicit>false</itunes:explicit>
    <podcast:transcript url="{BASE}/transcripts/{tag}.txt" type="text/plain"/>
  </item>""")
    rows.append(f"<tr><td>{n}</td><td>{html.escape(e['topic'])}</td><td>{html.escape(e['title'])}<br><small>{span}</small></td><td>{hms(info['duration'])}</td><td><a href=\"episodes/{fn}\">MP3</a> · <a href=\"transcripts/{tag}.txt\">Text</a></td></tr>")
for f in os.listdir(f"{SITE}/episodes"):
    if f not in keep: os.remove(f"{SITE}/episodes/{f}")
now=format_datetime(dt.datetime.now(tz))
feed=f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:podcast="https://podcastindex.org/namespace/1.0">
<channel>
  <title>CFA Level I Audio Review</title>
  <link>{BASE}/</link>
  <atom:link href="{BASE}/feed.xml" rel="self" type="application/rss+xml"/>
  <language>en-us</language>
  <description>Original review episodes for the November 2026 CFA Level I exam, in Kaplan Schweser module order. Each episode teaches the core ideas and traps for a group of modules and ends with a spoken recall check. Not produced by or affiliated with Kaplan or CFA Institute.</description>
  <itunes:summary>Original review episodes for the November 2026 CFA Level I exam, in Kaplan Schweser module order.</itunes:summary>
  <itunes:author>CFA Level I Audio Review</itunes:author>
  <itunes:image href="{BASE}/cover.jpg"/>
  <image><url>{BASE}/cover.jpg</url><title>CFA Level I Audio Review</title><link>{BASE}/</link></image>
  <itunes:category text="Education"/>
  <itunes:explicit>false</itunes:explicit>
  <itunes:type>serial</itunes:type>
  <itunes:block>Yes</itunes:block>
  <podcast:locked>yes</podcast:locked>
  <lastBuildDate>{now}</lastBuildDate>
{chr(10).join(items)}
</channel>
</rss>
"""
open(f"{SITE}/feed.xml","w",encoding="utf-8").write(feed)
page=f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>CFA Level I Audio Review</title>
<style>body{{font-family:system-ui,sans-serif;max-width:860px;margin:0 auto;padding:16px;color:#14213d;background:#fff}}code{{background:#eef2f7;padding:2px 6px;border-radius:4px;word-break:break-all}}table{{border-collapse:collapse;width:100%;font-size:14px}}td{{border-bottom:1px solid #e3e8ef;padding:8px 6px;vertical-align:top}}small{{color:#5a6b82}}img{{width:120px;border-radius:8px}}</style></head><body>
<img src="cover.jpg" alt="Cover"><h1>CFA Level I Audio Review</h1>
<p>Private, unlisted study feed. In Apple Podcasts on iPhone: Library, the More button (three dots), Follow a Show by URL, then paste:</p>
<p><code>{BASE}/feed.xml</code></p>
<p>Original review audio keyed to Kaplan Schweser module numbers. Not produced by or affiliated with Kaplan or CFA Institute.</p>
<table>{''.join(rows)}</table></body></html>"""
open(f"{SITE}/index.html","w",encoding="utf-8").write(page)
print(len(items),"episodes in feed")
