#!/usr/bin/env python3
"""16:9 (1920x1080) HyperFrames composition: base video + clean caption rail
(word-synced) + name lower-third (top-left) + CTA end card. One render.

Usage: python3 build_comp16.py [WORK_DIR]
  WORK_DIR (default: this script's dir) must contain transcript.json and a
  public/ holding input-video.mp4, fonts/, vendor/gsap.min.js. Writes
  WORK_DIR/public/index.html. Edit the EDIT-ME constants (CTA text, name) below.
"""
import json, html, pathlib, sys

WORK = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).parent
words = json.loads((WORK / "transcript.json").read_text())

DUR = 32.0
CAP_END = 29.5      # captions stop just before the end card
CTA_START = 29.7

def gap(a, b): return b["start"] - a["end"]
cues, cur = [], []
for i, w in enumerate(words):
    if w["start"] >= CAP_END:
        break
    cur.append(w)
    nxt = words[i + 1] if i + 1 < len(words) else None
    ends_sentence = w["text"].rstrip().endswith((".", "?", "!"))
    big_gap = nxt and gap(w, nxt) > 0.45
    too_long = (w["end"] - cur[0]["start"]) > 2.6
    too_many = len(cur) >= 7
    if nxt is None or ends_sentence or big_gap or too_long or too_many:
        cues.append(cur); cur = []
if cur:
    cues.append(cur)

caption_divs = []
for idx, grp in enumerate(cues):
    start = round(grp[0]["start"], 2)
    end = min(round(grp[-1]["end"], 2), CAP_END)
    # leave a small gap before the next cue so clips never share a boundary
    if idx + 1 < len(cues):
        end = min(end, round(cues[idx + 1][0]["start"] - 0.04, 2))
    if end - start < 0.4:
        end = start + 0.4
    text = html.escape(" ".join(w["text"] for w in grp).strip())
    cid = f"cap-{idx:02d}"
    caption_divs.append(
        f'      <div id="{cid}" class="caption clip" data-start="{start}" '
        f'data-duration="{round(end-start,2)}" data-track-index="2"><span>{text}</span></div>'
    )
caption_html = "\n".join(caption_divs)

doc = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <style>
      @font-face {{ font-family: "Inter"; src: url("fonts/Inter-700-latin.woff2") format("woff2"); font-weight: 700; font-display: block; }}
      @font-face {{ font-family: "Inter"; src: url("fonts/Inter-400-latin.woff2") format("woff2"); font-weight: 400; font-display: block; }}
      :root {{ --tiger-red:#c41e1e; --tiger-gold:#ffb000; }}
      * {{ box-sizing: border-box; }}
      html, body {{ margin:0; padding:0; width:100%; height:100%; overflow:hidden; background:#000; font-family:"Inter",ui-sans-serif,system-ui,sans-serif; }}
      #stage {{ position:relative; width:100%; height:100%; overflow:hidden; }}
      .video-wrapper {{ position:absolute; inset:0; overflow:hidden; }}
      .video-wrapper video {{ width:100%; height:100%; object-fit:cover; }}

      /* clean caption rail — bottom-center, readable (landscape sizing) */
      .caption {{ position:absolute; left:50%; bottom:70px; transform:translateX(-50%); width:auto; max-width:1320px; text-align:center; }}
      .caption span {{ display:inline; box-decoration-break:clone; -webkit-box-decoration-break:clone;
        background:rgba(0,0,0,0.62); color:#fff; font-size:54px; font-weight:700; line-height:1.34; padding:8px 22px; border-radius:12px; letter-spacing:-0.5px; }}

      /* name lower-third — TOP-LEFT (clears the bottom caption rail). #lt is the clip host; animate inner only */
      #lt {{ position:absolute; left:70px; top:70px; }}
      #lt .lt-inner {{ padding:18px 32px 20px 26px; border-radius:14px;
        background:linear-gradient(90deg, rgba(196,30,30,0.96), rgba(120,12,12,0.96));
        border-left:8px solid var(--tiger-gold); box-shadow:0 14px 44px rgba(0,0,0,0.5); }}
      #lt .name {{ color:#fff; font-size:50px; font-weight:700; line-height:1; }}
      #lt .role {{ color:var(--tiger-gold); font-size:25px; font-weight:700; margin-top:10px; letter-spacing:1px; text-transform:uppercase; }}

      /* CTA end card */
      #cta {{ position:absolute; inset:0; }}
      #cta .cta-inner {{ position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center;
        background:radial-gradient(circle at 50% 44%, rgba(12,12,14,0.9), rgba(0,0,0,0.97)); text-align:center; padding:0 80px; }}
      #cta .kicker {{ color:var(--tiger-gold); font-size:34px; font-weight:700; letter-spacing:6px; text-transform:uppercase; }}
      #cta .headline {{ color:#fff; font-size:84px; font-weight:700; line-height:1.1; margin-top:22px; max-width:1500px; letter-spacing:-1px; }}
      #cta .pill {{ margin-top:42px; padding:24px 54px; border-radius:999px; background:var(--tiger-red); color:#fff; font-size:46px; font-weight:700; box-shadow:0 16px 48px rgba(196,30,30,0.55); }}
    </style>
  </head>
  <body>
    <div id="stage" data-composition-id="captions16" data-start="0" data-duration="{DUR}" data-fps="25" data-width="1920" data-height="1080">
      <div class="video-wrapper" id="video-wrap">
        <video id="bg-video" src="input-video.mp4" playsinline data-has-audio="true" data-start="0" data-duration="{DUR}" data-track-index="1"></video>
      </div>

      <!-- name lower-third (top-left, track 3) -->
      <div id="lt" class="clip" data-start="0.5" data-duration="4.5" data-track-index="3">
        <div class="lt-inner">
          <div class="name">Brent Bryson</div>
          <div class="role">39 Years in Network Marketing</div>
        </div>
      </div>

      <!-- caption rail (word-synced, baked once, track 2) -->
{caption_html}

      <!-- CTA end card (track 4) -->
      <div id="cta" class="clip" data-start="{CTA_START}" data-duration="{round(DUR-CTA_START,2)}" data-track-index="4">
        <div class="cta-inner">
          <div class="kicker">Free Guide</div>
          <div class="headline">Build your own<br />distribution org with AI</div>
          <div class="pill">stan.store/brentbryson</div>
        </div>
      </div>

      <script src="vendor/gsap.min.js"></script>
      <script>
        (function () {{
          const tl = window.gsap.timeline({{ paused: true }});
          tl.fromTo('#lt .lt-inner', {{ opacity: 0, y: -40 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }}, 0.5);
          tl.to('#lt .lt-inner', {{ opacity: 0, duration: 0.35, ease: "power2.in" }}, 4.6);
          tl.fromTo('#cta .cta-inner', {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5, ease: "power2.out" }}, {CTA_START});
          tl.fromTo('#cta .pill', {{ opacity: 0, scale: 0.82 }}, {{ opacity: 1, scale: 1, duration: 0.5, ease: "back.out(1.7)" }}, {round(CTA_START+0.35,2)});
          window.__timelines = window.__timelines || {{}};
          window.__timelines["captions16"] = tl;
        }})();
      </script>
    </div>
  </body>
</html>
"""
out = WORK / "public" / "index.html"
out.write_text(doc)
print(f"wrote {out}; caption cues: {len(cues)}")
for grp in cues:
    print(f'  [{grp[0]["start"]:.2f}-{min(grp[-1]["end"],CAP_END):.2f}] {" ".join(w["text"] for w in grp)}')
