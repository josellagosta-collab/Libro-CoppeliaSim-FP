from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import argparse
import json
import textwrap

BLUE = "#1565C0"
YELLOW = "#F5C242"
TEXT = "#263238"
GREY_BORDER = "#D6DCE5"
LABEL_BG = "#FFFFFF"
BG = "#FFFFFF"


def load_font(size: int, bold: bool = False):
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        p = Path(candidate)
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


def rounded_shadow(draw, box, radius=14):
    x1, y1, x2, y2 = box
    for offset, alpha in [(5, 28), (9, 16), (13, 8)]:
        draw.rounded_rectangle(
            (x1 + offset, y1 + offset, x2 + offset, y2 + offset),
            radius=radius,
            fill=(0, 0, 0, alpha),
        )


def parse_inline_callouts(values):
    callouts = []
    for value in values or []:
        try:
            number_part, rest = value.split(":", 1)
            coords_part, text = rest.split(":", 1)
            x_str, y_str = coords_part.split(",", 1)
            callouts.append({
                "number": int(number_part),
                "x": int(x_str),
                "y": int(y_str),
                "text": text.strip(),
            })
        except ValueError:
            raise SystemExit(f"Formato de callout incorrecto: {value}")
    return callouts


def load_callouts(json_path, inline_callouts):
    callouts = []
    if json_path:
        with open(json_path, "r", encoding="utf-8") as f:
            callouts.extend(json.load(f))
    callouts.extend(parse_inline_callouts(inline_callouts))
    return callouts


def draw_callout(draw, x, y, number, text, scale=1.0):
    r = int(22 * scale)
    line_len = int(42 * scale)
    font_num = load_font(int(24 * scale), True)
    font_label = load_font(int(23 * scale), True)

    draw.ellipse((x - r, y - r, x + r, y + r), fill=YELLOW, outline=TEXT, width=max(2, int(2 * scale)))

    bbox = draw.textbbox((0, 0), str(number), font=font_num)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((x - tw / 2, y - th / 2 - 1), str(number), fill=TEXT, font=font_num)

    lx1 = x + r
    lx2 = x + r + line_len
    draw.line((lx1, y, lx2, y), fill=TEXT, width=max(2, int(3 * scale)))

    padding_x = int(12 * scale)
    padding_y = int(7 * scale)
    tb = draw.textbbox((0, 0), text, font=font_label)
    label_w = tb[2] - tb[0] + padding_x * 2
    label_h = tb[3] - tb[1] + padding_y * 2
    label_x = lx2 + int(8 * scale)
    label_y = y - label_h / 2

    draw.rounded_rectangle(
        (label_x, label_y, label_x + label_w, label_y + label_h),
        radius=int(8 * scale),
        fill=LABEL_BG,
        outline=GREY_BORDER,
        width=max(1, int(2 * scale)),
    )
    draw.text((label_x + padding_x, label_y + padding_y - 1), text, fill=TEXT, font=font_label)


def build_figure(input_path, output_path, caption, width=1200, callouts=None, clean_top=False):
    input_path = Path(input_path)
    output_path = Path(output_path)
    callouts = callouts or []

    img = Image.open(input_path).convert("RGB")

    if clean_top:
        d = ImageDraw.Draw(img)
        w, h = img.size
        d.rectangle((int(w * 0.48), 0, w, 36), fill=(245, 245, 245))

    ratio = width / img.width
    img_h = int(img.height * ratio)
    img = img.resize((width, img_h), Image.LANCZOS)

    margin = 38
    caption_gap = 22
    caption_height = 82
    canvas_w = width + margin * 2
    canvas_h = img_h + margin * 2 + caption_gap + caption_height

    canvas = Image.new("RGB", (canvas_w, canvas_h), BG)
    overlay = Image.new("RGBA", (canvas_w, canvas_h), (255, 255, 255, 0))
    od = ImageDraw.Draw(overlay)

    img_x, img_y = margin, margin
    box = (img_x, img_y, img_x + width, img_y + img_h)

    rounded_shadow(od, box)
    canvas.paste(img, (img_x, img_y))
    od.rounded_rectangle(box, radius=14, outline=GREY_BORDER, width=3)

    canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(canvas)

    for c in callouts:
        x = int(c["x"] * ratio) + img_x
        y = int(c["y"] * ratio) + img_y
        draw_callout(draw, x, y, c["number"], c["text"])

    caption_y = margin + img_h + caption_gap
    draw.rounded_rectangle((margin, caption_y, margin + 8, caption_y + 52), radius=4, fill=BLUE)

    title_font = load_font(28, True)
    body_font = load_font(24, False)
    lines = textwrap.wrap(caption, width=96)
    if len(lines) > 2:
        lines = lines[:2]
        lines[-1] = lines[-1].rstrip(".") + "…"

    for i, line in enumerate(lines):
        draw.text(
            (margin + 22, caption_y + i * 32),
            line,
            fill=TEXT,
            font=title_font if i == 0 else body_font,
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(output_path, "PNG", quality=95)
    print(f"Figura generada: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Genera figuras editoriales FPBook con marco, pie y llamadas numeradas."
    )
    parser.add_argument("input", help="Ruta de entrada PNG/JPG")
    parser.add_argument("caption", help="Pie de figura")
    parser.add_argument("-o", "--output", help="Ruta de salida")
    parser.add_argument("--width", type=int, default=1200, help="Ancho de la captura dentro de la plantilla")
    parser.add_argument("--callouts", nargs="*", help='Llamadas inline: "1:120,45:Barra de menús"')
    parser.add_argument("--callouts-json", help="Archivo JSON con llamadas")
    parser.add_argument("--clean-top", action="store_true", help="Tapa la zona superior derecha de la captura")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output) if args.output else input_path.with_name(input_path.stem + "_figure.png")
    callouts = load_callouts(args.callouts_json, args.callouts)

    build_figure(
        input_path=input_path,
        output_path=output_path,
        caption=args.caption,
        width=args.width,
        callouts=callouts,
        clean_top=args.clean_top,
    )


if __name__ == "__main__":
    main()
