from PIL import Image
from pathlib import Path
import subprocess
import tempfile

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
    if ext.upper() != img.format:  # same format so do nothing
        if img.format.upper() in ["PNG", "WEBP", "JPEG"]:
            
            if ext.upper() in ["JPEG", "JPG"]:
                # need to convert to RGB first, then can save in any format
                img = img.convert("RGB")

            if ext.lower() == "jpeg":
                # 95 is the reccommended upper limit on quality for JPEGs in PIL
                if quality is not None and quality <= 95:
                    img.save(
                        tmp_file.name,
                        ext.upper(), quality=quality, progressive=True
                    )
                else:
                    img.save(
                       tmp_file.name,
                        ext.upper(), quality=95, progressive=True)
            else:
                img.save(tmp_file.name, ext.upper())

            img = Image.open(tmp_file.name)

    # only optimize pngs with an alpha channel
    if img.format == "PNG" and img.mode in ["RGBA", "LA"]:
        if quality is not None:
            command = [
                "./its/utils/pngquant", "--force", "--verbose", "--output",
                "./compressed.png", "-s10", "--quality " + str(quality) + "-100", tmp_file.name]
        else:
            command = [
                "./its/utils/pngquant", "--force", "--verbose", "--output",
                "./compressed.png", "-s10", tmp_file.name]
        img.save("./tmp.png", "PNG")
        # output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        subprocess.check_output(command, stderr=subprocess.STDOUT)
        img = Image.open(tmp_file.name)

    if img.format == "JPEG":
        if quality is not None:
            img.save(tmp_file.name, "JPEG", quality=quality, optimize=True, progressive=True)
        else:
            img.save(tmp_file.name, "JPEG", optimize=True, progressive=True)
        img = Image.open(tmp_file.name)

    tmp_file.close()

    return img
