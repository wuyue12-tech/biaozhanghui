from pathlib import Path
import math
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance


ROOT = Path("/Users/wuyue/Documents/自主管理学院")
ASSETS = ROOT / "assets" / "signwall"
OUT_PREVIEW = ROOT / "向九年级出发_签名墙_v11_预览.png"
OUT_PRINT = ROOT / "向九年级出发_签名墙_v11_9000x6000.png"

W, H = 9000, 6000
SCALE_PREVIEW = 3

TITLE = "向九年级出发"
SUBTITLE = "进衢年级成长表彰暨九年级入境仪式 · 2026.7.6"

FONT_TITLE = ASSETS / "LongCang-Regular.ttf"
FONT_SUBTITLE = Path("/System/Library/Fonts/Hiragino Sans GB.ttc")
BG_IMAGE = ASSETS / "nasa_elsewhere_starfield_4k_print.jpg"


def cubic(p0, p1, p2, p3, t):
    mt = 1 - t
    x = mt**3 * p0[0] + 3 * mt**2 * t * p1[0] + 3 * mt * t**2 * p2[0] + t**3 * p3[0]
    y = mt**3 * p0[1] + 3 * mt**2 * t * p1[1] + 3 * mt * t**2 * p2[1] + t**3 * p3[1]
    return x, y


def cubic_tangent(p0, p1, p2, p3, t):
    mt = 1 - t
    x = 3 * mt**2 * (p1[0] - p0[0]) + 6 * mt * t * (p2[0] - p1[0]) + 3 * t**2 * (p3[0] - p2[0])
    y = 3 * mt**2 * (p1[1] - p0[1]) + 6 * mt * t * (p2[1] - p1[1]) + 3 * t**2 * (p3[1] - p2[1])
    return x, y


def star_points(cx, cy, outer, inner, rotation=-math.pi / 2):
    pts = []
    for i in range(10):
        r = outer if i % 2 == 0 else inner
        a = rotation + i * math.pi / 5
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def draw_star(draw, cx, cy, outer, rotation, fill, outline):
    pts = star_points(cx, cy, outer, outer * 0.43, rotation)
    draw.polygon(pts, fill=fill, outline=outline)


def make_background():
    base = Image.new("RGB", (W, H), "#020819")

    if BG_IMAGE.exists():
        bg = Image.open(BG_IMAGE).convert("RGB")
        bg = bg.resize((W, H), Image.Resampling.LANCZOS)
        bg = ImageEnhance.Contrast(bg).enhance(1.85)
        bg = ImageEnhance.Brightness(bg).enhance(0.34)
        bg = ImageEnhance.Color(bg).enhance(0.65)
        base = Image.blend(base, bg, 0.78)

    # Deep blue spatial gradients.
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    px = overlay.load()
    for y in range(H):
        for x in range(W):
            dx = (x - W * 0.68) / W
            dy = (y - H * 0.50) / H
            r = math.sqrt(dx * dx + dy * dy)
            glow = max(0, 1 - r * 2.2)
            top = max(0, 1 - y / H)
            a = int(105 * glow + 35 * top)
            px[x, y] = (15, 55, 118, a)
    base = Image.alpha_composite(base.convert("RGBA"), overlay)

    # Dark vignette.
    vignette = Image.new("L", (W, H), 0)
    vpx = vignette.load()
    for y in range(H):
        for x in range(W):
            dx = abs(x - W / 2) / (W / 2)
            dy = abs(y - H / 2) / (H / 2)
            val = int(230 * max(0, (max(dx, dy) - 0.42) / 0.58))
            vpx[x, y] = min(230, val)
    dark = Image.new("RGBA", (W, H), (0, 0, 0, 210))
    base = Image.composite(dark, base, vignette).convert("RGBA")
    return base


def generate_signature_stars():
    random.seed(90824)
    p0 = (680, 4650)
    p1 = (2600, 4550)
    p2 = (4670, 1500)
    p3 = (8350, 1360)

    stars = []
    min_x, max_x = 410, W - 410
    min_y, max_y = 1030, H - 850

    def make_candidate(t):
        cx, cy = cubic(p0, p1, p2, p3, t)
        tx, ty = cubic_tangent(p0, p1, p2, p3, t)
        length = math.hypot(tx, ty)
        nx, ny = -ty / length, tx / length

        half_width = 1220 * (0.78 + 0.18 * math.sin(math.pi * t))
        # A soft triangular distribution gives the band a dense center and loose edges.
        off = (random.random() + random.random() - 1) * half_width
        along = random.uniform(-34, 34)
        x = cx + nx * off + (tx / length) * along
        y = cy + ny * off + (ty / length) * along
        if not (min_x <= x <= max_x and min_y <= y <= max_y):
            return None
        outer = random.uniform(105, 112)
        rot = -math.pi / 2 + random.uniform(-0.15, 0.15)
        return x, y, outer, rot, t, "signature"

    def has_room(candidate, others, gap):
        x, y, outer, *_ = candidate
        for px, py, pr, *_ in others:
            required = outer + pr + gap
            if (x - px) ** 2 + (y - py) ** 2 < required ** 2:
                return False
        return True

    target_signature_count = 145
    segment_count = 29

    # Large stars are real signature positions. They are accepted only when
    # they keep a practical writing gap and remain outside title/subtitle zones.
    placed = []
    for segment in range(segment_count):
        want = 5
        made = 0
        attempts = 0
        while made < want and attempts < 2600:
            attempts += 1
            t = (segment + random.uniform(0.08, 0.92)) / segment_count
            candidate = make_candidate(t)
            if candidate and has_room(candidate, placed, 55):
                placed.append(candidate)
                made += 1

    attempts = 0
    while len(placed) < target_signature_count and attempts < 20000:
        attempts += 1
        candidate = make_candidate(random.uniform(0.015, 0.985))
        if candidate and has_room(candidate, placed, 50):
            placed.append(candidate)

    if len(placed) < target_signature_count:
        raise RuntimeError(f"Only placed {len(placed)} signature stars; loosen spacing or widen the arc.")

    stars.extend(placed)

    # Decorative stars ride the same flow but remain visibly smaller.
    for i in range(10):
        t = (i + 0.5) / 10
        cx, cy = cubic(p0, p1, p2, p3, t)
        tx, ty = cubic_tangent(p0, p1, p2, p3, t)
        length = math.hypot(tx, ty)
        nx, ny = -ty / length, tx / length
        off = random.choice([-760, 760]) * (0.75 + 0.20 * math.sin(math.pi * t))
        x = cx + nx * off + random.uniform(-110, 110)
        y = cy + ny * off + random.uniform(-110, 110)
        x = max(360, min(W - 360, x))
        y = max(1220, min(H - 1040, y))
        stars.append((x, y, random.uniform(45, 62), -math.pi / 2 + random.uniform(-0.2, 0.2), t, "decor"))

    return stars


def arc_points(count=170):
    p0 = (680, 4650)
    p1 = (2600, 4550)
    p2 = (4670, 1500)
    p3 = (8350, 1360)
    return [cubic(p0, p1, p2, p3, i / (count - 1)) for i in range(count)]


def lerp(a, b, t):
    return int(a + (b - a) * t)


def stream_color(t, alpha):
    # Deep blue at the lower-left, pale blue in the middle, warm gold near the upper-right.
    if t < 0.68:
        k = t / 0.68
        rgb = (lerp(30, 96, k), lerp(76, 145, k), lerp(160, 222, k))
    else:
        k = (t - 0.68) / 0.32
        rgb = (lerp(112, 255, k), lerp(154, 218, k), lerp(226, 114, k))
    return (*rgb, alpha)


def draw_galaxy_stream(img, stars):
    stream = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(stream)

    path = arc_points()
    for width, alpha, blur, phase in [
        (1040, 20, 132, "deep"),
        (650, 28, 92, "mid"),
        (340, 38, 58, "pale"),
        (104, 42, 28, "rim"),
    ]:
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        for i, (a, b) in enumerate(zip(path, path[1:])):
            t = i / (len(path) - 2)
            # Left is a visible starting point, center is the clearest, right fades outward.
            start_boost = 0.22 * math.exp(-((t - 0.08) / 0.12) ** 2)
            center_boost = 0.38 * math.sin(math.pi * t)
            fade_right = 1 - 0.44 * max(0, (t - 0.70) / 0.30)
            a2 = int(alpha * (0.58 + start_boost + center_boost) * fade_right)
            ld.line([a, b], fill=stream_color(t, a2), width=width, joint="curve")
        layer = layer.filter(ImageFilter.GaussianBlur(blur))
        stream = Image.alpha_composite(stream, layer)

    return Image.alpha_composite(img, stream)


def draw_small_stars(img):
    random.seed(726)
    d = ImageDraw.Draw(img)
    for _ in range(120):
        x = random.randint(80, W - 80)
        y = random.randint(80, H - 80)
        r = random.choice([3, 4, 5, 6, 8])
        a = random.randint(16, 62)
        color = random.choice([(255, 255, 255, a), (255, 220, 105, a), (165, 206, 255, a)])
        d.ellipse((x - r, y - r, x + r, y + r), fill=color)
    for _ in range(12):
        x = random.randint(120, W - 120)
        y = random.randint(140, H - 180)
        r = random.randint(18, 42)
        a = random.randint(18, 42)
        d.line((x - r, y, x + r, y), fill=(255, 255, 255, a), width=4)
        d.line((x, y - r, x, y + r), fill=(255, 255, 255, a), width=4)


def draw_signature_stars(img, stars):
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    sd = ImageDraw.Draw(img)

    for x, y, outer, rot, t, role in stars:
        if role == "signature":
            glow_alpha = int(18 + 12 * t)
            draw_star(gd, x, y, outer * 1.035, rot, (255, 222, 128, glow_alpha), None)
        else:
            draw_star(gd, x, y, outer * 1.25, rot, (255, 213, 57, 90), None)
    glow = glow.filter(ImageFilter.GaussianBlur(32))
    img.alpha_composite(glow)

    for x, y, outer, rot, t, role in stars:
        if role == "signature":
            fill = (255, 234, 150, 255)
            inner = (255, 242, 185, 122)
            outline = (255, 249, 205, 210)
        else:
            fill = (255, 216, 78, 235)
            inner = (255, 235, 128, 105)
            outline = (255, 246, 184, 210)
        draw_star(sd, x, y, outer, rot, fill, outline)
        draw_star(sd, x, y, outer * 0.72, rot, inner, None)


def fit_font(draw, text, font_path, target_width, start_size, index=0):
    size = start_size
    while size > 40:
        font = ImageFont.truetype(str(font_path), size=size, index=index)
        bbox = draw.textbbox((0, 0), text, font=font)
        if bbox[2] - bbox[0] <= target_width:
            return font
        size -= 8
    return ImageFont.truetype(str(font_path), size=size, index=index)


def draw_text(img):
    d = ImageDraw.Draw(img)
    title_font = fit_font(d, TITLE, FONT_TITLE, W * 0.67, 710)
    sub_font = fit_font(d, SUBTITLE, FONT_SUBTITLE, W * 0.72, 180)

    bbox = d.textbbox((0, 0), TITLE, font=title_font)
    tx = W / 2 - (bbox[2] - bbox[0]) / 2 - bbox[0]
    ty = 360 - bbox[1]

    # Soft shadow and slight luminous rim.
    for dx, dy, fill in [
        (28, 32, (0, 4, 20, 200)),
        (-7, 0, (205, 232, 255, 60)),
        (7, 0, (205, 232, 255, 60)),
        (0, -5, (205, 232, 255, 54)),
        (0, 5, (205, 232, 255, 54)),
    ]:
        d.text((tx + dx, ty + dy), TITLE, font=title_font, fill=fill)
    d.text((tx, ty), TITLE, font=title_font, fill=(255, 255, 255, 255))

    sb = d.textbbox((0, 0), SUBTITLE, font=sub_font)
    sx = W / 2 - (sb[2] - sb[0]) / 2 - sb[0]
    # Bottom safety strip: about 20 cm high on the final 3m x 2m print.
    band = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(band)
    bd.rectangle((0, H - 650, W, H), fill=(0, 8, 28, 58))
    img.alpha_composite(band.filter(ImageFilter.GaussianBlur(10)))
    sy = H - 455 - sb[1]
    d.text((sx + 8, sy + 10), SUBTITLE, font=sub_font, fill=(0, 0, 18, 110))
    d.text((sx, sy), SUBTITLE, font=sub_font, fill=(220, 236, 255, 235))


def main():
    img = make_background()
    draw_small_stars(img)
    stars = generate_signature_stars()
    img = draw_galaxy_stream(img, stars)
    draw_signature_stars(img, stars)
    draw_text(img)

    img.convert("RGB").save(OUT_PRINT, quality=95)
    preview = img.resize((W // SCALE_PREVIEW, H // SCALE_PREVIEW), Image.Resampling.LANCZOS)
    preview.convert("RGB").save(OUT_PREVIEW, quality=94)
    print(OUT_PREVIEW)
    print(OUT_PRINT)


if __name__ == "__main__":
    main()
