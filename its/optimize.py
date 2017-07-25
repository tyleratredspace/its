from PIL import Image
from pathlib import Path
import subprocess
import tempfile
import uuid
from .errors import ITSTransformError
from its.settings import (
    PNGQUANT_PATH, PNGQUANT_DEFAULT_SPEED,
    PNGQUANT_DEFAULT_MAX_QUALITY, DEFAULT_JPEG_QUALITY)


def optimize(img, query):

    ext = query['format'] if 'format' in query else img.format.lower()  # the return format
    quality = int(query['quality']) if 'quality' in query else None
    tmp_file = tempfile.NamedTemporaryFile(dir=".", delete=True)
    output_path = str(uuid.uuid4())

    if ext.lower() == "jpg":
        ext = "jpeg"

    # convert first, then optimize
    if ext.lower() != img.format.lower():  # same format so do nothing
        if img.format.lower() in ["png", "webp", "jpeg"]:

            if ext.lower() == "jpeg":
                # need to convert to RGB first, then can save in any format
                # only necessary when converting to jpeg/jpg
                img = img.convert("RGB")

    if ext.lower() == "jpeg":
        # convert to JPG and/or compress 
        if quality is not None:
            img.save(tmp_file.name, "JPEG", quality=quality, optimize=True, progressive=True)
        else:
            # 95 is the reccommended upper limit on quality for JPEGs in PIL
            img.save(
                tmp_file.name, "JPEG", quality=DEFAULT_JPEG_QUALITY,
                optimize=True, progressive=True)
    else:
        # convert from PNG, JPG and WEBP to formats other than JPG
        img.save(tmp_file.name, ext.upper())
    
    # reopen newly converted or compressed image
    img = Image.open(tmp_file.name)

    # only optimize pngs if quality param is provided
    if img.format == "PNG" and quality is not None:
        
        command = [
                PNGQUANT_PATH, "--skip-if-larger", "--strip", "--force", "--output",
                output_path, "-s" + PNGQUANT_DEFAULT_SPEED,
                "-Q" + str(quality) + "-" + PNGQUANT_DEFAULT_MAX_QUALITY, tmp_file.name]

        try:
            subprocess.check_output(command, stderr=subprocess.STDOUT)
            img = Image.open(output_path)
        except (OSError, subprocess.CalledProcessError) as e:
            raise ITSTransformError(error="ITSTransform Error: " + str(e))

    # remove temporary files
    if Path(tmp_file.name).exists():
        tmp_file.close()

    if Path("./" + output_path).exists():
        Path(output_path).unlink()

    return img
