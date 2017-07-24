from PIL import Image
from pathlib import Path
import subprocess


def optimize(img, query):

    # what to do with "gif" webp?
    # allow svgs to pass through unchanged
    # convert from and to  png ,jpeg, webp
    ext = query['format'] if 'format' in query else img.format.lower()  # the return format
    quality = int(query['quality']) if 'quality' in query else None

    if ext is not None and ext.lower() == "jpg":
        ext = "jpeg"

    # convert first, then optimize
    if ext.upper() != img.format:  # same format so do nothing
        if img.format in ["PNG", "WEBP", "JPEG"]:
            img = img.convert("RGB")  # need to convert to RGB first, then can save in any format

            if ext.lower() == "jpeg":
                # 95 is the reccommended upper limit on quality for JPEGs in PIL
                if quality is not None and quality <= 95:
                    img.save(
                        "converted." + ext.lower(),
                        ext.upper(), quality=quality, progressive=True
                    )
                else:
                    img.save(
                        "converted." + ext.lower(),
                        ext.upper(), quality=95, progressive=True)
            else:
                img.save("converted." + ext.lower(), ext.upper())

            img = Image.open("converted." + ext.lower())

    # only optimize pngs with an alpha channel
    if img.format == "PNG" and img.mode in ["RGBA", "LA"]:
        if quality is not None:
            command = [
                "./its/utils/pngquant", "--force", "--verbose", "--output",
                "./compressed.png", "-s10", "--quality " + str(quality) + "-100", "./tmp.png"]
        else:
            command = [
                "./its/utils/pngquant", "--force", "--verbose", "--output",
                "./compressed.png", "-s10", "./tmp.png"]
        img.save("./tmp.png", "PNG")
        # output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        subprocess.check_output(command, stderr=subprocess.STDOUT)
        img = Image.open("./compressed.png")

    if img.format == "JPEG":
        if quality is not None:
            img.save("compressed.jpeg", "JPEG", quality=quality, optimize=True, progressive=True)
        else:
            img.save("compressed.jpeg", "JPEG", optimize=True, progressive=True)
        img = Image.open("./compressed.jpeg")

    if Path("converted." + ext.lower()).exists():  # delete temporary conversion file
        Path("converted." + ext.lower()).unlink()

    if Path("tmp." + ext.lower()).exists():  # delete temporary file
        Path("tmp." + ext.lower()).unlink()

    if Path("compressed." + ext.lower()).exists():  # delete temporary compression file
        Path("compressed." + ext.lower()).unlink()

    return img
