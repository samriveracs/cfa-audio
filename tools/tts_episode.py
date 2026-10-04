#!/usr/bin/env python3
"""Render one episode script to MP3 with chapters. Usage: tts_episode.py N"""
import sys, re, json, os, time, subprocess, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

ROOT="/home/claude/podcast"
SR=24000
NARR, NARR_SPEED = "af_heart", 0.95
ALT, ALT_SPEED = "am_michael", 0.95

PRON = [
 (r"\bBA II Plus\b","bee eigh two plus"),(r"\bB A two plus\b","bee eigh two plus"),(r"\bIFRS\b","I F R S"),(r"\bU\.S\.","U S"),(r"\bIRR\b","I R R"),(r"\bROE\b","R O E"),(r"\bROA\b","R O A"),
 (r"\bROIC\b","R O I C"),(r"\bEPS\b","E P S"),(r"\bESG\b","E S G"),(r"\bABS\b","A B S"),(r"\bYTM\b","Y T M"),(r"\bOAS\b","O A S"),
 (r"\bDDM\b","D D M"),(r"\bFCFE\b","F C F E"),(r"\bFCFF\b","F C F F"),(r"\bPPE\b","P P E"),(r"\bDTA\b","D T A"),(r"\bDTL\b","D T L"),
 (r"\bDTAs\b","D T As"),(r"\bDTLs\b","D T Ls"),(r"\bVaR\b","var"),(r"\bLBO\b","L B O"),(r"\bVC\b","V C"),(r"\bCPI\b","C P I"),
 (r"\bOTC\b","O T C"),(r"\bCCP\b","C C P"),(r"\bLIBOR\b","lie bore"),(r"\bSOFR\b","sofer"),(r"\bCMO\b","C M O"),(r"\bCMOs\b","C M Os"),
 (r"\bCDO\b","C D O"),(r"\bCDOs\b","C D Os"),(r"\bETF\b","E T F"),(r"\bETFs\b","E T Fs"),(r"\bREIT\b","reet"),(r"\bREITs\b","reets"),
 (r"\bCML\b","C M L"),(r"\bSML\b","S M L"),(r"\bLIFO\b","lie foe"),(r"\bFIFO\b","fie foe"),(r"\bEBITDA\b","ee bit dah"),(r"\bEBIT\b","ee bit"),
 (r"\bIPO\b","I P O"),(r"\bIPOs\b","I P Os"),(r"\bSPAC\b","spack"),(r"\bSPACs\b","spacks"),(r"\bHHI\b","H H I"),(r"\bMBS\b","M B S"),
 (r"\bNPV\b","N P V"),(r"\bGDP\b","G D P"),(r"\bMPC\b","M P C"),(r"\bCFO\b","C F O"),(r"\bCFI\b","C F I"),(r"\bCFF\b","C F F"),
 (r"\bCPT\b","C P T"),(r"\bPMT\b","P M T"),(r"\bPV\b","P V"),(r"\bFV\b","F V"),(r"\bCAPM\b","cap M"),(r"\bWACC\b","wack"),
 (r"\bANOVA\b","ANOVA"),(r"\bGAAP\b","gap"),(r"\bMM\b","M and M"),(r"’","'"),(r"‘","'"),(r"[“”]",'"'),
]
ROMAN={"VII":"seven","VI":"six","IV":"four","V":"five","III":"three","II":"two","I":"one"}
RN=r"(VII|VI|IV|V|III|II|I)"
def norm(t, header=False):
    t=re.sub(r"\b"+RN+r"\(([A-E])\)", lambda m: ROMAN[m.group(1)]+" "+m.group(2), t)
    if header:
        t=t.replace("/"," and ").replace("(","").replace(")","")
        t=re.sub(r"(\w)-(\w)",r"\1 \2",t)
    for a,b in PRON: t=re.sub(a,b,t)
    t=re.sub(r"\b(Level|Standard|Standards|Type|Tier|Part|Basel)\s+"+RN+r"\b", lambda m: m.group(1)+" "+ROMAN[m.group(2)], t)
    t=re.sub(r"\b(VII|VI|IV|III|II)\b", lambda m: ROMAN[m.group(1)], t)
    t=re.sub(r"\b(?:[A-Z] )+[A-Z]\b", lambda m: " ".join("eigh" if c=="A" else c for c in m.group(0).split()), t)
    t=re.sub(r"(?<=[a-z0-9,] )A\b(?!')", "eigh", t)
    t=re.sub(r"\bA(?= (?:and|or|versus|to|is|has|and) [A-Z]\b)", "eigh", t)
    t=t.replace("%"," percent").replace("&"," and ")
    t=re.sub(r"\$([\d,\.]+)",r"\1 dollars",t)
    return re.sub(r"\s+"," ",t).strip()

def parse(text):
    blocks=[]; para=[]
    def flush():
        if para: blocks.append(("p"," ".join(para))); para.clear()
    for line in text.splitlines():
        s=line.strip()
        if not s: flush(); continue
        if s.startswith("## "): flush(); blocks.append(("h",s[3:].strip())); continue
        if s.startswith("Q: "): flush(); blocks.append(("q",s[3:].strip())); continue
        para.append(s)
    flush(); return blocks

def main(n):
    man={e['ep']:e for e in json.load(open(f"{ROOT}/manifest.json"))}
    e=man[n]; nxt=man.get(n+1)
    script=open(f"{ROOT}/scripts/E{n:02d}.txt",encoding="utf-8").read()
    k=Kokoro(f"{ROOT}/tts/kokoro-v1.0.onnx",f"{ROOT}/tts/voices-v1.0.bin")
    first,last=e['modules'][0]['id'],e['modules'][-1]['id']
    span=f"Module {first}" if first==last else f"Modules {first} through {last}"
    intro=[("h",f"Episode {n}. {e['title']}."),("p",f"{e['topic']}, Kaplan {span}.")]
    if n==1:
        intro.append(("p","This series is original review audio, keyed to Kaplan module numbers for the 2026 Level One exam. It is not produced by Kaplan or by CFA Institute. Use it after you read the modules, as spaced review."))
    outro=[("p",f"That is the end of Episode {n}." + (f" Next is Episode {nxt['ep']}, {nxt['title']}." if nxt else ""))]
    blocks=intro+parse(script)+outro
    sil=lambda s: np.zeros(int(SR*s),dtype=np.float32)
    audio=[sil(0.4)]; chapters=[]; t0=time.time()
    def say(text,voice,speed,header=False):
        s,sr=k.create(norm(text,header),voice=voice,speed=speed,lang="en-us"); assert sr==SR
        return s.astype(np.float32)
    pos=lambda: sum(len(a) for a in audio)/SR
    for i,(kind,text) in enumerate(blocks):
        if kind=="h":
            if i>0: audio.append(sil(1.0))
            if i>=len(intro) or i==0:
                title = "Introduction" if i==0 else text
                chapters.append((pos(), title))
            audio.append(say(text,ALT,ALT_SPEED,header=True)); audio.append(sil(0.6))
        elif kind=="q":
            audio.append(say(text,ALT,ALT_SPEED)); audio.append(sil(5.0))
        else:
            audio.append(say(text,NARR,NARR_SPEED)); audio.append(sil(0.45))
    audio.append(sil(1.0))
    y=np.concatenate(audio); dur=len(y)/SR
    wav=f"{ROOT}/audio/E{n:02d}.wav"; sf.write(wav,y,SR)
    # chapters metadata
    meta=f"{ROOT}/audio/E{n:02d}.ffmeta"
    with open(meta,"w") as f:
        f.write(";FFMETADATA1\n")
        f.write(f"title=E{n:02d} {e['title']}\nartist=CFA Level I Audio Review\nalbum=CFA Level I Audio Review\ntrack={n}\ngenre=Podcast\n")
        for j,(st,title) in enumerate(chapters):
            en = chapters[j+1][0] if j+1<len(chapters) else dur
            f.write(f"[CHAPTER]\nTIMEBASE=1/1000\nSTART={int(st*1000)}\nEND={int(en*1000)}\ntitle={title}\n")
    mp3=f"{ROOT}/audio/E{n:02d}.mp3"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",wav,"-i",meta,"-map_metadata","1","-map_chapters","1",
        "-af","loudnorm=I=-16:LRA=11:TP=-1.5","-ac","1","-ar","24000","-c:a","libmp3lame","-b:a","40k","-id3v2_version","3",mp3],check=True)
    os.remove(wav)
    info=dict(ep=n,duration=round(dur,1),bytes=os.path.getsize(mp3),words=len(script.split()),compute_s=round(time.time()-t0),chapters=chapters)
    json.dump(info,open(f"{ROOT}/audio/E{n:02d}.json","w"),indent=1)
    print(json.dumps({k:v for k,v in info.items() if k!='chapters'}))

if __name__=="__main__": main(int(sys.argv[1]))
