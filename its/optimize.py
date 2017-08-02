from PIL import Image
from pathlib import Path
import subprocess
import tempfile
import uuid
from math import floor
from .errors import ITSTransformError
from its.settings import PNGQUANT_PATH, DEFAULT_JPEG_QUALITY


def optimize(img, query):

    ext = query['format'] if 'format' in query else img.format.lower()  # the return format
    
    try:
        quality = int(query['quality']) if 'quality' in query else None
    except ValueError as e:
        raise ITSTransformError(error="ITSTransform Error: " + str(e))

    with tempfile.NamedTemporaryFile(dir=".", delete=True) as tmp_file:
        
        if ext.lower() == "jpg":
            ext = "jpeg"

        # convert first, then optimize
        if ext.lower() == "jpeg":
            # convert to JPG and/or compress
            # need to convert to RGB first, then can save in any format
            if img.format != "jpeg":
                new_img = Image.new("RGBA", img.size)
                new_img = Image.alpha_composite(new_img, img)
                img = img.convert("RGB") 
            img = optimize_jpg(img, tmp_file, quality)
        else:
            # convert from PNG, JPG and WEBP to formats other than JPG
            img = convert(img, ext, tmp_file)

        # only optimize pngs if quality param is provided
        if img.format == "PNG" and quality is not None:
            img = optimize_png(img, tmp_file, quality)

        return img


def convert(img, ext, tmp_file):
    
    if ext.lower() != img.format.lower():  # same format so do nothing
        if img.format.lower() in ["png", "webp", "jpeg"]:
            img.save(tmp_file.name, ext.upper())
            # reopen newly converted or compressed image
            img = Image.open(tmp_file.name)
    return img



def optimize_jpg(img, tmp_file, quality=None):
    if quality is not None and quality <= 95:
        img.save(tmp_file.name, "JPEG", quality=quality, optimize=True, progressive=True)
    else:
        # 95 is the reccommended upper limit on quality for JPEGs in PIL
        img.save(
            tmp_file.name, "JPEG", quality=DEFAULT_JPEG_QUALITY,
            optimize=True, progressive=True)
    # reopen newly converted or compressed image
    img = Image.open(tmp_file.name)
    return img


def optimize_png(img, tmp_file, quality=None):
    output_path = str(uuid.uuid4())

    if quality < 100:
        # return the image as is since 100% quality means no compression
        if quality % 10 == 0:
            speed = int(quality / 10)  # quality is inversely related to pngquant speed
        else:
            # each interval of 10 is related to one speed:
            # [90 - 99] --> speed 9
            speed = int(floor((quality - (quality % 10)) / 10))

        command = [
                PNGQUANT_PATH, "--strip", "--force", "--output",
                output_path, "-s" + str(speed), tmp_file.name]

        try:
            subprocess.check_output(command, stderr=subprocess.STDOUT)
            img = Image.open(output_path)
            if Path("./" + output_path).exists():
                Path(output_path).unlink()
        except (OSError, subprocess.CalledProcessError) as e:
            print(e)
            raise ITSTransformError(error="ITSTransform Error: " + str(e))
    return img
