from PIL import Image
from pathlib import Path
import subprocess

def optimize(img, query):

    # may need to change to allow maintaining of alpha layer
    # what to do with "gif" webp?
    # allow svgs to pass through unchanged
    # convert from and to  png ,jpeg, webp
    ext = query['format'] if 'format' in query else img.format # the return format
    quality = int(query['quality']) if 'quality' in query else None
    commands = {
        'JPEG':["./utils/jpegoptim", "--strip-all", "--all-progressive"],
        'PNG':["./utils/pngcrush", "-reduce", "-ow", "-brute"]
    }

    if ext.lower() == "jpg":
        ext = "jpeg"  
    # convert first, then optimize
    if ext.upper() != img.format: #same format so do nothing
        # convert from png to jpeg & webp
        if img.format in ["PNG", "WEBP", "JPEG"]:
            img = img.convert("RGB") # need to convert to RGB first, then can save in any format
            
            if ext.lower() == "jpeg":
                if quality is not None:
                    img.save("converted." + ext.lower(), ext.upper(), quality=quality, progressive=True)
                else:
                    img.save("converted." + ext.lower(), ext.upper(), quality=95, progressive=True)
            else:
                img.save("converted." + ext.lower(), ext.upper())
            
            img = Image.open("converted." + ext.lower())

    if img.format in commands.keys():
        print("optimizable")

    if Path("converted." + ext.lower()).exists(): # delete temporary conversion file
        Path("converted." + ext.lower()).unlink()
    # # using brute on pngcrush takes at least half a minute, so should narrow down a
    # # particular method that it can use
    # # strip-all might remove important info on jpgs
    # # handle alpha channels better
    # # don't only convert to RGB

    # ext = query['format'] if 'format' in query else img.format

    # if ext.upper() == "JPG":
    #     ext = "JPEG"

    # tmp_folder = Path(__file__).parents[0] / "tmp"
    # path = Path(tmp_folder / ("input." + ext.lower()))
    # quality = int(query['quality']) if 'quality' in query else None

    # commands = {
    #     'JPEG':["./utils/jpegoptim", "--strip-all", "--all-progressive", path],
    #     'PNG':["./utils/pngcrush", "-reduce", "-ow", "-brute", path]
    # }

    # # make temporary folder and files
    # # if Path.exists(path):
    # #    path.unlink()

    # # if Path.exists(tmp_folder):
    # #     tmp_folder.rmdir()

    # # Path.mkdir(tmp_folder)
    # # Path.touch(path)

    # # convert image before compression
    # if (ext == "jpg" or ext == "jpeg") and img.format == "PNG":
    #     img.convert('RGB').save(path, ext.upper())
    # else:
    #     img.save(path, ext.upper())
    
    # img = Image.open(path)

    # if ext != "webp":
    #     if quality is None or img.format == "PNG":
    #         try:
    #             subprocess.check_call(commands[img.format])
    #         except subprocess.CalledProcessError as e:
    #             raise e
    #     elif (quality >= 1 and quality <= 100) and img.format == "JPEG":
    #         try:
    #             commands[img.format] = ["./utils/jpegoptim", "--strip-all", "--all-progressive",\
    #                 "--max=" + str(quality), path]
    #             subprocess.check_call(commands[img.format])
    #         except subprocess.CalledProcessError as e:
    #             raise e

    # img = Image.open(path)

    # # remove temporary files
    # # path.unlink()
    # # tmp_folder.rmdir()

    return img
