#!/usr/bin/env python3
"""Render one episode script to MP3 with chapters. Usage: tts_episode.py N"""
import sys, re, json, os, time, subprocess, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

ROOT="/home/claude/podcast"
SR=24000
# Two co hosts share the explaining. voice id, speed, phonemizer language, gain
VOICES={"H":("af_heart",0.95,"en-us",1.0),"L":("bm_lewis",1.0,"en-gb",1.16)}
STMIN, STMAX = 280, 450   # words per stint before the other host takes over
SIG=re.compile(r"^(Here is the trap|The trap|The classic trap|A second trap|Another trap|A third trap|Worked example|Here is one|Here is an example|Now |Second|Third|Finally|On the exam|One more|Next|Example|A quick example|Try this|Put numbers|Let us|Let's|Consider|Picture|Take )", re.I)
other=lambda s: "L" if s=="H" else "H"

def assign(intro, body, outro_text):
    out=[("h",intro[0][1],"H")]+[(k,t,"L") for k,t in intro[1:]]
    secs=[]
    for k,t in body:
        if k=="h": secs.append([t,[]])
        else: secs[-1][1].append((k,t))
    spk="H"
    for title,items in secs:
        tl=title.lower()
        if tl.startswith("recall check"):
            out.append(("h",title,spk)); asker=spk
            for k,t in items:
                if k=="q": out.append(("q",t,asker)); answerer=other(asker); asker=other(asker)
                else: out.append(("p",t,answerer))
            spk=other(spk); continue
        if tl.startswith("recap"):
            out.append(("h",title,spk))
            sents=[x for x in re.split(r"(?<=[.?!])\s+"," ".join(t for _,t in items)) if x]
            cur=spk
            for i in range(0,len(sents),2):
                out.append(("p"," ".join(sents[i:i+2]),cur)); cur=other(cur)
            spk=cur; continue
        out.append(("h",title,spk))
        words=[len(t.split()) for _,t in items]; stint=0
        for i,(k,t) in enumerate(items):
            remaining=sum(words[i:])
            if stint>=STMIN and remaining>=150 and (stint>=STMAX or SIG.match(t)):
                spk=other(spk); stint=0
            out.append((k,t,spk)); stint+=words[i]
        spk=other(spk)
    out.append(("p",outro_text,spk))
    return out

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
 (r"\b[Aa]rbitrageurs\b","arbitrah zhers"),(r"\b[Aa]rbitrageur\b","arbitrah zher"),(r"\b[Aa]rbitrage\b","arbitrahzh"),(r"\b[Aa]rithmetic\b","arithmetik"),(r"\b[Cc]ovariances\b","co-variances"),(r"\b[Cc]ovariance\b","co-variance"),
 (r"\b([Oo]n|[Aa]t the) close\b",r"\1 cloze"),
 (r"\b([Pp])utable\b",r"\1ootable"),
 (r"\bMAD\b","M A D"),(r"\bCournot\b","Coor no"),(r"\bHerfindahl\b","Herfin dahl"),(r"\b[Mm]onopsony\b","mo nopsony"),(r"\bKeynesians\b","Kaynzians"),(r"\bKeynesian\b","Kaynzian"),(r"\bKeynes\b","Kaynz"),(r"\bexcise\b","eksize"),(r"\b([Mm])onetarist",r"\1onitterist"),(r"\bquota rents?\b",lambda m: "kwohtuh "+m.group(0).split()[1]),(r"\bhegemony\b","hejemoany"),(r"\b[Ss]upervisory\b","supervizery"),(r"\bNOPAT\b","no pat"),(r"\bModigliani\b","Mohdilyani"),(r"\b([Ll])essees\b",r"\1e sees"),(r"\b([Ll])essee\b",r"\1e see"),(r"\b([Ll])essors\b",r"\1ess ors"),(r"\b([Ll])essor\b",r"\1ess or"),(r"\b([Ee])xternalit",r"\1ksternalit"),(r"\b(the|of|its|their|cheap|cheaper|more|fewer|less|on|for|foreign|total|net|than|domestic|rising|falling|higher|lower|and|minus|plus|exceed|over) imports\b",r"\1 im ports"),(r"(^|(?<=[.!?] ))Imports\b","Im ports"),(r"\bimports (and|minus|exceed|rise|fall|grow|shrink)\b",r"im ports \1"),(r"\bPlaty\b","Platty"),
 (r"\bANOVA\b","ANOVA"),(r"\bGAAP\b","gap"),(r"\bMM\b","M and M"),(r"’","'"),(r"‘","'"),(r"[“”]",'"'),
]
ROMAN={"VII":"seven","VI":"six","IV":"four","V":"five","III":"three","II":"two","I":"one"}
RN=r"(VII|VI|IV|V|III|II|I)"
def norm(t, header=False):
    t=re.sub(r"\b"+RN+r"\(([A-E])\)", lambda m: ROMAN[m.group(1)]+" "+m.group(2), t)
    t=re.sub(r"(^|(?<=[.?!:] ))A (?=[A-Z] [a-z]|U\.S\.)", "a ", t)   # sentence start article before a capital, e.g. A T bill, A U.S. company
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
    t=re.sub(r"(\d)\.(\d)", r"\1 point \2", t)   # module numbers and decimals, so a final period is not read as a pause
    return re.sub(r"\s+"," ",t).strip()

TAG=re.compile(r"^(HEART|LEWIS)( Q)?: (.*)$")
def parse(text):
    """Blocks: (kind, text, who). who is H or L when the script tags the speaker, else None."""
    blocks=[]; para=[]; who=[None]
    def flush():
        if para: blocks.append(("p"," ".join(para),who[0])); para.clear()
        who[0]=None
    for line in text.splitlines():
        s=line.strip()
        if not s: flush(); continue
        if s.startswith("## "): flush(); blocks.append(("h",s[3:].strip(),None)); continue
        m=TAG.match(s)
        if m and m.group(2): flush(); blocks.append(("q",m.group(3).strip(),m.group(1)[0])); continue
        if s.startswith("Q: "): flush(); blocks.append(("q",s[3:].strip(),None)); continue
        if m: flush(); who[0]=m.group(1)[0]; para.append(m.group(3).strip()); continue
        para.append(s)
    flush(); return blocks

def tagged_plan(intro, blocks, outro_text):
    """Dialogue scripts: every paragraph and question names its host. A header is read by the next speaker."""
    out=[("h",intro[0][1],"H")]+[(k,t,"L") for k,t in intro[1:]]
    for i,(k,t,w) in enumerate(blocks):
        if k=="h":
            nxt=next((b[2] for b in blocks[i+1:] if b[2]),"H"); out.append(("h",t,nxt))
        else:
            assert w, "untagged block in a tagged script: "+t[:60]
            out.append((k,t,w))
    last=next((b[2] for b in reversed(blocks) if b[2]),"H")
    out.append(("p",outro_text,"L" if last=="H" else "H"))
    return out

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
    blocks=parse(script)
    if any(b[2] for b in blocks):
        # Dialogue scripts open with one line naming the episode and module span. The script's own first paragraph lists the topics.
        intro=[("h",f"Episode {n}. {e['topic']}, {span}.")]
        plan=tagged_plan(intro, blocks, outro[0][1])
    else: plan=assign(intro, [(k,t) for k,t,_ in blocks], outro[0][1])
    sil=lambda s: np.zeros(int(SR*s),dtype=np.float32)
    audio=[sil(0.4)]; chapters=[]; t0=time.time(); share={"H":0,"L":0}
    def say(text,who,header=False):
        v,sp,lang,g=VOICES[who]
        s,sr=k.create(norm(text,header),voice=v,speed=sp,lang=lang); assert sr==SR
        share[who]+=len(text.split())
        return (s*g).astype(np.float32)
    pos=lambda: sum(len(a) for a in audio)/SR
    prev=None
    for i,(kind,text,who) in enumerate(plan):
        if kind=="h":
            if i>0: audio.append(sil(1.0))
            if i==0 or i>=len(intro): chapters.append((pos(), "Introduction" if i==0 else text))
            audio.append(say(text,who,header=True)); audio.append(sil(0.6))
        elif kind=="q":
            audio.append(say(text,who)); audio.append(sil(5.0))
        else:
            if prev is not None and prev!=who and plan[i-1][0]=="p": audio.append(sil(0.25))
            audio.append(say(text,who)); audio.append(sil(0.45))
        prev=who
    audio.append(sil(1.0))
    y=np.concatenate(audio); dur=len(y)/SR
    wav=f"{ROOT}/audio/E{n:02d}.wav"; sf.write(wav,y,SR,subtype='FLOAT')
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
    info=dict(voices={k2:round(v2/max(1,sum(share.values())),3) for k2,v2 in share.items()},ep=n,duration=round(dur,1),bytes=os.path.getsize(mp3),words=len(script.split()),compute_s=round(time.time()-t0),chapters=chapters)
    json.dump(info,open(f"{ROOT}/audio/E{n:02d}.json","w"),indent=1)
    print(json.dumps({k:v for k,v in info.items() if k!='chapters'}))

if __name__=="__main__": main(int(sys.argv[1]))
