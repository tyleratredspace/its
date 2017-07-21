from PIL import Image
from pathlib import Path
import subprocess
from io import BytesIO

def optimize(img, query):

    # may need to change to allow maintaining of alpha layer
    # what to do with "gif" webp?
    # allow svgs to pass through unchanged
    # convert from and to  png ,jpeg, webp
    ext = query['format'] if 'format' in query else img.format # the return format
    quality = int(query['quality']) if 'quality' in query else None

    # if ext.lower() == "jpg":
    #     ext = "jpeg"  
    # # convert first, then optimize
    # if ext.upper() != img.format: #same format so do nothing
    #     # convert from png to jpeg & webp
    #     if img.format in ["PNG", "WEBP", "JPEG"]:
    #         img = img.convert("RGB") # need to convert to RGB first, then can save in any format
            
    #         if ext.lower() == "jpeg":
    #             if quality is not None:
    #                 img.save("converted." + ext.lower(), ext.upper(), quality=quality, progressive=True)
    #             else:
    #                 img.save("converted." + ext.lower(), ext.upper(), quality=95, progressive=True)
    #         else:
    #             img.save("converted." + ext.lower(), ext.upper())
            
    #         img = Image.open("converted." + ext.lower())


    if img.format == "PNG":
        if quality is not None:
            command = ["./its/utils/pngquant", "--force", "--verbose", "--output", "./compressed.png", "-s" + str(quality),  "./tmp.png"]
        else:
            command = ["./its/utils/pngquant", "--force", "--verbose", "--output", "./compressed.png", "./tmp.png"]
        img.save("./tmp.png","PNG")
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        img = Image.open("./compressed.png")

        # if quality is not None:
        #     command = ["./its/utils/pngquant", "--force", "--verbose", "-s" + str(quality), "-"]
        # else:
        #     command = ["./its/utils/pngquant", "--force", "--verbose", "-"]
        # tmp = BytesIO()
        # img.save(tmp, format=img.format.upper())
        # pipe = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # out, err = pipe.communicate(input=tmp.getvalue())
        # # print(out)
        # # print(err)
        # img = Image.open(out)
        # img.show()

    if img.format == "JPEG":
        if quality is not None:
            img.save("compressed.jpeg", "JPEG", quality=quality, optimize=True, progressive=True)
        else:
            img.save("compressed.jpeg", "JPEG", optimize=True, progressive=True)
        img = Image.open("./compressed.jpeg")


    if Path("converted." + ext.lower()).exists(): # delete temporary conversion file
        Path("converted." + ext.lower()).unlink()

    if Path("tmp." + ext.lower()).exists(): # delete temporary conversion file
        Path("tmp." + ext.lower()).unlink()

    if Path("compressed." + ext.lower()).exists(): # delete temporary conversion file
        Path("compressed." + ext.lower()).unlink()
    return img
