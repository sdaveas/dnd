#!/usr/bin/env python3
import json, sys, os
from PIL import Image, ImageDraw, ImageFont, ImageOps
try:
    from psd_tools import PSDImage
except ImportError:
    PSDImage = None

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
FONT_REG = os.path.join(HERE, "fonts", "animeace2_reg.ttf")
FONT_BLD = os.path.join(HERE, "fonts", "animeace2_bld.ttf")
PAPER = (250, 249, 246)
CARD_BACKING = (8, 8, 8)
CAP_FILL = (252, 251, 247)
CAP_BORDER = (0, 0, 0)

def load_font(path, size):
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    return ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", size)

def wrap(draw, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textbbox((0, 0), t, font=font)[2] <= maxw or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def make_caption(c, rect, title=False):
    size = 54 if title else 34
    font = load_font(FONT_BLD if title else FONT_REG, size)
    x0, y0 = rect[0], rect[1]
    pad = 20 if title else 24
    lh = 54 if title else size + 9
    cap_id = c["id"]
    tangle = ((sum(ord(ch) for ch in cap_id) % 9) - 4) / 2
    return font, x0, y0, pad, lh, tangle

class Page:
    def __init__(self, spec, root=ROOT):
        self.spec = spec
        self.page = spec.get("page")
        self.w, self.h = spec.get("canvas", [2550, 3300])
        self.img = Image.new("RGB", (self.w, self.h), PAPER)
        self.root = root
        self.cap_rects = []

    def panel_card(self, p):
        x0, y0, x1, y1 = p["rect"]
        pw, ph = x1 - x0, y1 - y0
        inset = 11
        back = Image.new("RGB", (pw + 2 * inset, ph + 2 * inset), CARD_BACKING)
        fit = ImageOps.fit(Image.open(os.path.join(self.root, p["art"])).convert("L"),
                           (pw, ph), centering=(0.5, 0.45))
        back.paste(fit, (inset, inset))
        idx = int(p["id"][1:]) - 1
        angle = ((-1) ** idx) * (0.7 + 0.4 * (idx % 3))
        rot = back.rotate(angle, expand=True, fillcolor=PAPER)
        # center the rotated card on the rect: paste so its center lands at rect center
        cx, cy = x0 + pw // 2, y0 + ph // 2
        self.img.paste(rot, (cx - rot.width // 2, cy - rot.height // 2))

    def caption(self, c, title=False, draw_img=None):
        x0, y0 = c["rect"][0], c["rect"][1]
        draw_img = draw_img if draw_img is not None else self.img
        font = load_font(FONT_BLD if title else FONT_REG, 54 if title else 34)
        pad = 20 if title else 24
        # use real font metrics: line height from ascent+descent, ink-top offset from bbox
        ascent, descent = font.getmetrics()
        bb = font.getbbox("Ag")
        ink_top, ink_bottom = bb[1], bb[3]
        lh = ascent + descent + (8 if not title else 10)
        d0 = ImageDraw.Draw(self.img)
        # spec rects are [x, y, w, h]
        lines = wrap(d0, c["text"], font, c["rect"][2] - 2 * pad)
        tw = max(d0.textbbox((0, 0), ln, font=font)[2] for ln in lines)
        th = len(lines) * lh
        bw, bh = tw + 2 * pad, th + 2 * pad
        cap_id = c["id"]
        tangle = ((sum(ord(ch) for ch in cap_id) % 9) - 4) / 2
        cap = Image.new("RGBA", (bw + 24, bh + 24), (0, 0, 0, 0))
        d = ImageDraw.Draw(cap)
        d.rectangle([8, 8, 8 + bw, 8 + bh], fill=CAP_BORDER)  # drop shadow
        d.rectangle([0, 0, bw, bh], fill=CAP_FILL)
        d.rectangle([0, 0, bw, bh], outline=CAP_BORDER, width=8)
        for i, ln in enumerate(lines):
            # center the ink block vertically: line ink spans [ink_top, ink_bottom] within its lh slot
            ty = pad + i * lh + (lh - (ink_bottom - ink_top)) // 2 - ink_top
            d.text((pad, ty), ln, font=font, fill=(0, 0, 0))
        cap = cap.rotate(tangle, center=(bw // 2, bh // 2), expand=True, fillcolor=(0, 0, 0, 0))
        draw_img.paste(cap, (x0, y0), cap)
        if draw_img is self.img:
            self.cap_rects.append((x0, y0, x0 + bw, y0 + bh))

    def build(self):
        for p in self.spec.get("panels", []):
            self.panel_card(p)
        self.base_img = self.img.copy()
        self.cap_layers = []
        for c in self.spec.get("captions", []):
            lay = Image.new("RGBA", (self.w, self.h), (0, 0, 0, 0))
            self.caption(c, draw_img=lay)
            self.caption(c)
            self.cap_layers.append(lay)
        if self.spec.get("title"):
            lay = Image.new("RGBA", (self.w, self.h), (0, 0, 0, 0))
            self.caption({"id": "title", "text": self.spec["title"]["text"],
                          "rect": self.spec["title"]["rect"]}, title=True, draw_img=lay)
            self.caption({"id": "title", "text": self.spec["title"]["text"],
                          "rect": self.spec["title"]["rect"]}, title=True)
            self.cap_layers.append(lay)

    def save(self, out_dir):
        os.makedirs(out_dir, exist_ok=True)
        out = os.path.join(out_dir, f"page-{self.page:02d}.png")
        self.img.save(out, dpi=(300, 300))
        return out

    def save_psd(self, out_dir):
        # ponytail: Pillow 11 ships no PSD writer (reader only), so use psd_tools
        if PSDImage is None:
            raise RuntimeError("psd_tools not installed; PSD export requires it")
        os.makedirs(out_dir, exist_ok=True)
        out = os.path.join(out_dir, f"page-{self.page:02d}.psd")
        psd = PSDImage.frompil(self.base_img)
        for i, lay in enumerate(self.cap_layers):
            psd.create_pixel_layer(lay.convert("RGBA"), name=f"caption-{i}", top=0, left=0)
        psd.save(out)
        return out

def render(path, out_dir, root=ROOT):
    spec = json.load(open(path))
    page = Page(spec, root)
    page.build()
    return page.save(out_dir), page

def main(argv):
    out_dir = os.path.join(HERE, "..", "renders")
    outs, pages = [], []
    for f in argv:
        out, page = render(f, out_dir)
        page.save_psd(out_dir)
        outs.append(out); pages.append(page)
    if outs:
        first = Image.open(outs[0]).convert("RGB")
        first.save(os.path.join(out_dir, "comic-preview.pdf"), "PDF",
                   save_all=True, append_images=[Image.open(o).convert("RGB") for o in outs[1:]],
                   resolution=300)
        print("rendered:", outs)

def check():
    out_dir = os.path.join(HERE, "..", "renders")
    for p in sorted(x for x in os.listdir(os.path.join(HERE, "pagespecs")) if x.endswith(".json")):
        path = os.path.join(HERE, "pagespecs", p)
        out, page = render(path, out_dir)
        over = [r for r in page.cap_rects if r[0] < 0 or r[1] < 0 or r[2] > page.w or r[3] > page.h]
        rects = sorted(page.cap_rects)
        overlap = 0
        for i in range(len(rects)):
            for j in range(i + 1, len(rects)):
                a, b = rects[i], rects[j]
                if not (a[2] <= b[0] + 4 or b[2] <= a[0] + 4 or a[3] <= b[1] + 4 or b[3] <= a[1] + 4):
                    overlap += 1
        print(f"{p}: canvas={Image.open(out).size} captions={len(page.cap_rects)} "
              f"overflows={len(over)} overlaps={overlap}")

if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--check":
        check()
    else:
        main(args)
