from PIL import Image
import io

# Maximum resolution (4K)
MAX_DIMENSION = 4096


def resize_if_needed(img: Image.Image) -> Image.Image:
    """
    Resize image if larger than MAX_DIMENSION while keeping aspect ratio
    """
    width, height = img.size
    max_side = max(width, height)

    if max_side <= MAX_DIMENSION:
        return img

    scale = MAX_DIMENSION / max_side
    new_size = (int(width * scale), int(height * scale))

    return img.resize(new_size, Image.LANCZOS)


def remove_background(image_bytes: bytes, model: str) -> bytes:
    """
    Removes background using rembg with optimized preprocessing
    """

    # 1️⃣ Load image from bytes
    img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")

    # 2️⃣ Resize if needed (performance optimization)
    img = resize_if_needed(img)

    # 3️⃣ Convert back to bytes
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # 4️⃣ AI background removal (import lazily to avoid hard dependency at import time)
    from rembg import remove

    return remove(
        buffer.read(),
        model=model,
        alpha_matting=True,
        alpha_matting_foreground_threshold=240,
        alpha_matting_background_threshold=10,
        alpha_matting_erode_size=10,
    )


def add_background(fg_bytes: bytes, bg_type: str, bg_value: str) -> bytes:
    """
    Adds dynamic background (color or image) to foreground
    """

    fg = Image.open(io.BytesIO(fg_bytes)).convert("RGBA")

    if bg_type == "color":
        bg = Image.new("RGBA", fg.size, bg_value)

    elif bg_type == "image":
        bg = Image.open(bg_value).convert("RGBA")
        bg = resize_if_needed(bg)
        bg = bg.resize(fg.size, Image.LANCZOS)

    else:
        raise ValueError("Invalid background type")

    # Composite foreground over background
    bg.paste(fg, (0, 0), fg)

    out = io.BytesIO()
    bg.save(out, format="PNG", optimize=True)
    return out.getvalue()
