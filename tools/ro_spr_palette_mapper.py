#!/usr/bin/env python3
"""
Ragnarok Online SPR palette-index mapper.

Reads indexed SPR v2.x files directly and reports exactly which palette
indices are used by every pixel. This avoids in-game diagnostic palettes.

Current scope:
- Indexed SPR frames (tested with SPR 2.1)
- External 1024-byte .pal file
- RLE format used by indexed SPR 2.x frames
- Exact per-index pixel counts and frame counts
- Per-index representative contact sheets

Usage:
    python ro_spr_palette_mapper.py body.spr --pal body_4.pal --out report_dir
    python ro_spr_palette_mapper.py body.spr --pal body_4.pal --out report_dir --indices 72-79
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import argparse, csv, html, math, re

def parse_range_list(spec):
    if not spec:
        return None
    out = set()
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a,b = map(int, part.split("-",1))
            out.update(range(a,b+1))
        else:
            out.add(int(part))
    return sorted(i for i in out if 0 <= i <= 255)

def parse_pal(path):
    b = Path(path).read_bytes()
    if len(b) != 1024:
        raise ValueError(f"PAL must be 1024 bytes; got {len(b)}")
    return [tuple(b[i*4:i*4+3]) for i in range(256)]

def decode_indexed_frame(blob, pos):
    if pos + 6 > len(blob):
        raise ValueError("Unexpected EOF in indexed frame header")
    w = int.from_bytes(blob[pos:pos+2], "little")
    h = int.from_bytes(blob[pos+2:pos+4], "little")
    clen = int.from_bytes(blob[pos+4:pos+6], "little")
    pos += 6
    comp = blob[pos:pos+clen]
    pos += clen

    pixels = bytearray()
    i = 0
    while i < len(comp):
        v = comp[i]
        i += 1
        if v == 0:
            if i >= len(comp):
                raise ValueError("Malformed SPR RLE: zero marker without run length")
            run = comp[i]
            i += 1
            pixels.extend(b"\x00" * run)
        else:
            pixels.append(v)

    expected = w*h
    if len(pixels) != expected:
        raise ValueError(
            f"Decoded frame size mismatch: {len(pixels)} != {expected} ({w}x{h})"
        )
    return {"w":w, "h":h, "pixels":bytes(pixels)}, pos

def parse_spr(path):
    b = Path(path).read_bytes()
    if b[:2] != b"SP":
        raise ValueError("Not an SPR file")
    minor = b[2]
    major = b[3]
    version = major + minor/10.0

    indexed_count = int.from_bytes(b[4:6], "little")
    rgba_count = int.from_bytes(b[6:8], "little") if version >= 2.0 else 0
    pos = 8 if version >= 2.0 else 6

    frames = []
    for n in range(indexed_count):
        fr, pos = decode_indexed_frame(b, pos)
        fr["number"] = n
        frames.append(fr)

    # We don't need truecolor frames for palette-index mapping. Validate scope.
    if rgba_count:
        # The current mapper intentionally does not parse these, because they
        # do not use the indexed palette. Report their count separately.
        pass

    return {
        "version": version,
        "indexed_count": indexed_count,
        "rgba_count": rgba_count,
        "frames": frames,
        "indexed_data_end": pos,
    }

def counts_for_frames(frames):
    pix = [0]*256
    frcnt = [0]*256
    for fr in frames:
        seen=set()
        for v in fr["pixels"]:
            if v == 0:
                continue
            pix[v]+=1
            seen.add(v)
        for v in seen:
            frcnt[v]+=1
    return pix, frcnt

def frame_index_count(fr, idx):
    return fr["pixels"].count(idx)

def render_normal(fr, pal, scale=4):
    w,h=fr["w"],fr["h"]
    im=Image.new("RGBA",(w,h),(0,0,0,0))
    px=im.load()
    p=fr["pixels"]
    for y in range(h):
        for x in range(w):
            idx=p[y*w+x]
            if idx == 0:
                continue
            r,g,b=pal[idx]
            px[x,y]=(r,g,b,255)
    return im.resize((w*scale,h*scale), Image.Resampling.NEAREST)

def render_mask(fr, idx, scale=4):
    """Target index = bright magenta; other visible sprite pixels = dim grayscale."""
    w,h=fr["w"],fr["h"]
    im=Image.new("RGBA",(w,h),(0,0,0,0))
    px=im.load()
    p=fr["pixels"]
    for y in range(h):
        for x in range(w):
            v=p[y*w+x]
            if v == 0:
                continue
            if v == idx:
                px[x,y]=(255,0,255,255)
            else:
                px[x,y]=(58,58,58,180)
    return im.resize((w*scale,h*scale), Image.Resampling.NEAREST)

def framed_panel(im, label, pad=6):
    font=ImageFont.load_default()
    box=Image.new("RGBA",(im.width+pad*2, im.height+pad*2+18),(245,245,245,255))
    box.alpha_composite(im,(pad,pad+18))
    d=ImageDraw.Draw(box)
    d.text((pad,3),label,fill=(0,0,0,255),font=font)
    return box

def contact_sheet(images, cols=5, gap=8, bg=(230,230,230,255)):
    if not images:
        return Image.new("RGBA",(100,50),bg)
    maxw=max(i.width for i in images)
    maxh=max(i.height for i in images)
    rows=math.ceil(len(images)/cols)
    out=Image.new("RGBA",
        (cols*maxw+(cols+1)*gap, rows*maxh+(rows+1)*gap), bg)
    for n,im in enumerate(images):
        x=gap+(n%cols)*maxw+(maxw-im.width)//2
        y=gap+(n//cols)*maxh+(maxh-im.height)//2
        out.alpha_composite(im,(x,y))
    return out

def build_report(spr, pal, outdir, requested=None, scale=4, reps=5):
    outdir=Path(outdir)
    (outdir/"index_masks").mkdir(parents=True,exist_ok=True)
    (outdir/"frames").mkdir(parents=True,exist_ok=True)

    frames=spr["frames"]
    pix,frcnt=counts_for_frames(frames)
    used=[i for i in range(1,256) if pix[i]]
    if requested is not None:
        used=[i for i in used if i in requested]

    # CSV
    with (outdir/"used_indices.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f)
        w.writerow(["index","pixels","frames_used","pal_r","pal_g","pal_b"])
        for i in used:
            w.writerow([i,pix[i],frcnt[i],*pal[i]])

    # Per-index sheets
    rows=[]
    for idx in used:
        ranked=sorted(
            ((frame_index_count(fr,idx),fr) for fr in frames),
            key=lambda x:x[0], reverse=True
        )
        ranked=[x for x in ranked if x[0]>0][:reps]
        panels=[]
        repnums=[]
        for cnt,fr in ranked:
            normal=render_normal(fr,pal,scale)
            mask=render_mask(fr,idx,scale)
            pair=Image.new("RGBA",(normal.width+mask.width+4,max(normal.height,mask.height)),(255,255,255,255))
            pair.alpha_composite(normal,(0,0))
            pair.alpha_composite(mask,(normal.width+4,0))
            panels.append(framed_panel(pair,f"frame {fr['number']} | {cnt}px"))
            repnums.append(fr["number"])
        sheet=contact_sheet(panels,cols=min(reps,5))
        name=f"index_{idx:03d}.png"
        sheet.save(outdir/"index_masks"/name)
        rows.append((idx,pix[idx],frcnt[idx],pal[idx],name,repnums))

    # All-frame normal atlas.
    panels=[]
    for fr in frames:
        panels.append(framed_panel(render_normal(fr,pal,2),f"frame {fr['number']}"))
    contact_sheet(panels,cols=12,gap=5).save(outdir/"all_frames_atlas.png")

    # HTML.
    html_rows=[]
    for idx,pixels,fc,color,name,repnums in rows:
        c="#%02x%02x%02x"%color
        html_rows.append(f"""
        <tr>
          <td class="idx">{idx}</td>
          <td>{pixels:,}</td><td>{fc}</td>
          <td><span class="swatch" style="background:{c}"></span>{c}</td>
          <td>{', '.join(map(str,repnums))}</td>
          <td><img src="index_masks/{name}"></td>
        </tr>""")
    doc=f"""<!doctype html>
<html><head><meta charset="utf-8">
<title>RO SPR Palette Index Map</title>
<style>
body{{font-family:system-ui,Segoe UI,sans-serif;margin:24px;background:#f4f4f4;color:#222}}
table{{border-collapse:collapse;background:white;width:100%}}
th,td{{border:1px solid #ccc;padding:8px;vertical-align:top}}
th{{position:sticky;top:0;background:#222;color:white}}
.idx{{font-size:20px;font-weight:700;text-align:center}}
img{{max-width:100%;image-rendering:pixelated}}
.swatch{{display:inline-block;width:28px;height:18px;border:1px solid #555;vertical-align:middle;margin-right:8px}}
code{{background:#eee;padding:2px 4px}}
</style></head>
<body>
<h1>Ragnarok SPR palette-index map</h1>
<p><b>SPR version:</b> {spr['version']:.1f} &nbsp;
<b>Indexed frames:</b> {spr['indexed_count']} &nbsp;
<b>Truecolor frames:</b> {spr['rgba_count']}</p>
<p>Each representative panel shows the normal sprite on the left and an exact
index mask on the right. <b>Magenta pixels are the selected palette index.</b>
Everything gray is another nontransparent sprite index.</p>
<p><a href="all_frames_atlas.png">All indexed frames atlas</a> |
<a href="used_indices.csv">CSV counts</a></p>
<table>
<thead><tr><th>Index</th><th>Total pixels</th><th>Frames</th><th>PAL color</th><th>Representative frames</th><th>Exact locations</th></tr></thead>
<tbody>{''.join(html_rows)}</tbody>
</table></body></html>"""
    (outdir/"index_report.html").write_text(doc,encoding="utf-8")

    return used, pix, frcnt

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("spr")
    ap.add_argument("--pal",required=True)
    ap.add_argument("--out",required=True)
    ap.add_argument("--indices",help="e.g. 9-15,56,72-79")
    ap.add_argument("--scale",type=int,default=4)
    ap.add_argument("--reps",type=int,default=5)
    a=ap.parse_args()
    spr=parse_spr(a.spr)
    pal=parse_pal(a.pal)
    requested=parse_range_list(a.indices)
    used,pix,frcnt=build_report(spr,pal,a.out,requested,a.scale,a.reps)
    print(f"SPR {spr['version']:.1f}: {spr['indexed_count']} indexed frames")
    print("Mapped indices:", ",".join(map(str,used)))
    for i in used:
        print(f"{i:3d}: {pix[i]:7d} px in {frcnt[i]:3d} frames")

if __name__=="__main__":
    main()
