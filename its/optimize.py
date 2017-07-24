from PIL import Image
from pathlib import Path
import subprocess
import tempfile
import uuid
from .errors import ITSTransformError
from its.settings import PNGQUANT_PATH, PNGQUANT_DEFAULT_SPEED, PNGQUANT_DEFAULT_MAX_QUALITY
from io import BytesIO

def optimize(img, query):

    # what to do with "gif" webp?
    # allow svgs to pass through unchanged
    # convert from and to  png ,jpeg, webp
    ext = query['format'] if 'format' in query else img.format.lower()  # the return format
    quality = int(query['quality']) if 'quality' in query else None
    tmp_file = tempfile.NamedTemporaryFile(dir=".", delete=True)

    if ext is not None and ext.lower() == "jpg":
        ext = "jpeg"

    # convert first, then optimize
    if ext.lower() != img.format.lower():  # same format so do nothing
        if img.format.lower() in ["png", "webp", "jpeg"]:
            
            if ext.lower() in ["jpeg", "jpg"]:
                # need to convert to RGB first, then can save in any format
                img = img.convert("RGB")
            else:
                img.save(tmp_file.name, ext.upper())

                img = Image.open(tmp_file.name)

    # only optimize pngs with an alpha channel
    if img.format == "PNG" and img.mode in ["RGBA", "LA"]:
        
        if quality is not None:
            command = [
                "./its/utils/pngquant", "--force", "--output",
                str(uuid.uuid4()), "-s" + PNGQUANT_DEFAULT_SPEED,
                "--quality " + str(quality) + "-" + PNGQUANT_DEFAULT_MAX_QUALITY, tmp_file.name]
        else:
            command = [
                "./its/utils/pngquant", "--force", "--output",
                str(uuid.uuid4()), "-s" + PNGQUANT_DEFAULT_SPEED, tmp_file.name]
        img.save(tmp_file.name, "PNG")

        try:
            subprocess.check_output(command, stderr=subprocess.STDOUT)
        except (OSError, subprocess.CalledProcessError) as e:
            print(ITSTransformError(error="ITSTransform Error: " + str(e)))

        img = Image.open(tmp_file.name)

    if img.format == "JPEG":
        if quality is not None:
            img.save(tmp_file.name, "JPEG", quality=quality, optimize=True, progressive=True)
        else:
            # 95 is the reccommended upper limit on quality for JPEGs in PIL
            img.save(tmp_file.name, "JPEG", quality=95, optimize=True, progressive=True)
        img = Image.open(tmp_file.name)

    tmp_file.close()

    return img
