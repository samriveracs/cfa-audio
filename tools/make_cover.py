from PIL import Image, ImageDraw, ImageFont
S=3000
img=Image.new("RGB",(S,S),(16,32,58))
d=ImageDraw.Draw(img)
# subtle grid of ten bars, one per topic
cols=[(46,94,152),(52,110,170),(60,124,184),(70,138,196),(84,152,206),(98,166,214),(116,178,220),(136,190,226),(158,202,232),(182,214,238)]
bw=S//10
for i,c in enumerate(cols):
    h=int(S*0.07+ i*S*0.025)
    d.rectangle([i*bw, S-h, (i+1)*bw-12, S], fill=c)
B="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; R="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def ctext(y,txt,font,fill):
    w=d.textlength(txt,font=font); d.text(((S-w)/2,y),txt,font=font,fill=fill)
ctext(380,"CFA",ImageFont.truetype(B,560),(255,255,255))
ctext(990,"LEVEL I",ImageFont.truetype(B,300),(255,255,255))
ctext(1380,"AUDIO REVIEW",ImageFont.truetype(R,190),(200,220,240))
ctext(1650,"2026 exam · Kaplan module order",ImageFont.truetype(R,110),(160,190,220))
img.save("/home/claude/cfa-audio/cover.jpg",quality=88,optimize=True)
print("ok")
