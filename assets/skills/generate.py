#!/usr/bin/env python3
"""Generate dark-themed skill radar + proficiency bar SVGs for the GitHub profile."""
import math, os

ASSETS = os.path.dirname(os.path.abspath(__file__))

BG      = "#0d1117"
BORDER  = "#30363d"
GRID    = "#21262d"
TEXT    = "#c9d1d9"
MUTED   = "#8b949e"
ACCENT  = "#58a6ff"
ACCENT2 = "#79c0ff"
TITLE   = "#58a6ff"

FONT = "ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"

os.makedirs(ASSETS, exist_ok=True)

# ---------------------------------------------------------------- Radar chart
def radar():
    W, H = 500, 440
    cx, cy = W/2, 232
    R = 150
    axes = [
        ("Frontend", 90),
        ("Backend", 82),
        ("Database", 74),
        ("DevOps", 60),
        ("Design / UI", 68),
        ("Architecture", 78),
    ]
    n = len(axes)
    def pt(i, r):
        ang = -math.pi/2 + 2*math.pi*i/n
        return cx + r*math.cos(ang), cy + r*math.sin(ang)

    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" role="img" aria-label="Skill radar chart">')
    parts.append(f'''<defs>
  <linearGradient id="rg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{ACCENT}"/><stop offset="1" stop-color="{ACCENT2}"/>
  </linearGradient>
</defs>''')
    parts.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="10" fill="{BG}" stroke="{BORDER}"/>')
    parts.append(f'<text x="24" y="40" fill="{TITLE}" font-family="{FONT}" font-size="17" font-weight="700">Skill Radar</text>')
    parts.append(f'<text x="{W-24}" y="40" text-anchor="end" fill="{MUTED}" font-family="{FONT}" font-size="12">proficiency by domain</text>')

    # concentric rings (as polygons)
    for ring in (0.25, 0.5, 0.75, 1.0):
        pts = " ".join(f"{pt(i, R*ring)[0]:.1f},{pt(i, R*ring)[1]:.1f}" for i in range(n))
        parts.append(f'<polygon points="{pts}" fill="none" stroke="{GRID}" stroke-width="1"/>')
    # spokes + labels
    for i,(name,val) in enumerate(axes):
        x,y = pt(i, R)
        parts.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="{GRID}" stroke-width="1"/>')
        lx,ly = pt(i, R+26)
        anchor = "middle"
        if lx > cx+5: anchor = "start"
        elif lx < cx-5: anchor = "end"
        dy = 4
        if ly < cy-5: dy = -2
        elif ly > cy+5: dy = 12
        parts.append(f'<text x="{lx:.1f}" y="{ly+dy:.1f}" text-anchor="{anchor}" fill="{TEXT}" font-family="{FONT}" font-size="12.5" font-weight="600">{name}</text>')
        parts.append(f'<text x="{lx:.1f}" y="{ly+dy+15:.1f}" text-anchor="{anchor}" fill="{MUTED}" font-family="{FONT}" font-size="11">{val}%</text>')

    # data polygon
    dpts = " ".join(f"{pt(i, R*val/100)[0]:.1f},{pt(i, R*val/100)[1]:.1f}" for i,(_,val) in enumerate(axes))
    parts.append(f'<polygon points="{dpts}" fill="{ACCENT}" fill-opacity="0.18" stroke="url(#rg)" stroke-width="2.5" stroke-linejoin="round"/>')
    for i,(_,val) in enumerate(axes):
        x,y = pt(i, R*val/100)
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="{BG}" stroke="{ACCENT2}" stroke-width="2"/>')
    parts.append('</svg>')
    return "\n".join(parts)

# ------------------------------------------------------------- Proficiency bars
def bars():
    skills = [
        ("TypeScript", 92, "#3178C6"),
        ("React / Next.js", 88, "#61DAFB"),
        ("Node.js / Express", 82, "#339933"),
        ("Python", 68, "#3776AB"),
        ("Go", 62, "#00ADD8"),
        ("Java / Spring", 60, "#6DB33F"),
        ("SQL / NoSQL", 74, "#4479A1"),
        ("Docker / CI-CD", 58, "#2496ED"),
        ("Figma / UI Design", 66, "#F24E1E"),
    ]
    W = 500
    pad_top = 60
    row_h = 38
    H = pad_top + row_h*len(skills) + 14
    bar_x = 172
    bar_w = W - bar_x - 30
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" role="img" aria-label="Skill proficiency bars">']
    parts.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="10" fill="{BG}" stroke="{BORDER}"/>')
    parts.append(f'<text x="24" y="38" fill="{TITLE}" font-family="{FONT}" font-size="17" font-weight="700">Proficiency</text>')
    parts.append(f'<text x="{W-24}" y="38" text-anchor="end" fill="{MUTED}" font-family="{FONT}" font-size="12">self-assessed</text>')
    for i,(name,val,color) in enumerate(skills):
        y = pad_top + i*row_h
        cyc = y + row_h/2 - 3
        gid = f"g{i}"
        parts.append(f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{color}" stop-opacity="0.85"/><stop offset="1" stop-color="{ACCENT2}"/></linearGradient>')
        parts.append(f'<text x="24" y="{cyc+4:.0f}" fill="{TEXT}" font-family="{FONT}" font-size="12.5" font-weight="600">{name}</text>')
        parts.append(f'<rect x="{bar_x}" y="{cyc-7:.0f}" width="{bar_w}" height="10" rx="5" fill="{GRID}"/>')
        fw = max(10, bar_w*val/100)
        parts.append(f'<rect x="{bar_x}" y="{cyc-7:.0f}" width="{fw:.1f}" height="10" rx="5" fill="url(#{gid})"/>')
        parts.append(f'<text x="{W-24}" y="{cyc+4:.0f}" text-anchor="end" fill="{MUTED}" font-family="{FONT}" font-size="11.5" font-weight="600">{val}%</text>')
    parts.append('</svg>')
    return "\n".join(parts)

with open(os.path.join(ASSETS, "radar.svg"), "w") as f:
    f.write(radar())
with open(os.path.join(ASSETS, "proficiency.svg"), "w") as f:
    f.write(bars())
print("wrote", ASSETS)
