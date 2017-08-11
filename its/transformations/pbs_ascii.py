from PIL import Image, ImageDraw
from math import floor
from .base import BaseTransform


class PBSASCIITransform(BaseTransform):

    """
    Generic image transform type class
    """
    slug = 'pbs'  # unique string that identifies a given transform

    def apply_transform(img, fill_color=None):

        pos_x = 5
        pos_y = 85

        if fill_color is not None:
            if len(fill_color) < 3:
                fill_color = (0, 0, 0)
            elif len(fill_color) == 5:
                pos_x, pos_y, *fill_color = fill_color
            else:
                fill_color = (
                    int(floor(int(fill_color[0]))),
                    int(floor(int(fill_color[1]))),
                    int(floor(int(fill_color[2])))
                )


        draw = ImageDraw.Draw(img)
        pbs_ascii = """
            -:::::::::::::::-.`          -::::::::::::::::---.`                 .-://+++//:-`         
         :yyyyyyyyyyyyyyyyyyys+:`      :++++++++++++++++++++++/-`         `-+ooooooooooooooo/.      
        :yyyyyyyyyyyyyyyyyyyyyyyyo-    :+++++++++++++++++++++++++:`     `/ooooooooooooooooooooo-    
       :yyyyyyyyyyyyyyyyyyyyyyyyyyys.  :+++++++++++++++++++++++++++-   -oooooooooooooooooooooooo+`  
      :yyyyyyyyyyyyyyyyyyyyyyyyyyyyyy: :++++++++++++++++++++++++++++- -ooooooooooooooooooooooooooo` 
     :yyyyyysosyyyyyyyyyyyyyyyyyyyyyyy-:+++++++++++++//++++++++++++++.ooooooooooooo//+oooooooooooo+ 
    :yyyyy/`   `+yyyyyyyyyyyyyyyyyyyyys/++++++++++:`    -+++++++++++++ooooooooooo-     :ooooooooooo`
   /yyyyyo      `yyyyyyyyyyyyyyyyyyyyyyo++++++++++`      /+++++++++++ooooooooooo+      `oo+////////`
  /yyyyyyy-     /yyyyyyyyyyyyyyyyyyyyyyo++++++++++:     .+++++++++++/:ooooooooooo:`   `/oooo/.      
 /yyyyyyyyys++oyyyyyyyyyyyyyyyyyyyyyyyy/++++++++++++/:/+++++++++++++``ooooooooooooo++ooooooooo+-    
`////+yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy/:++++++++++++++++++++++++++/`  .ooooooooooooooooooooooooo+`  
     :yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy+ :++++++++++++++++++++++++++/`   `+oooooooooooooooooooooooo+` 
     :yyyyyyyyyyyyyyyyyyyyyyyyyyyyyy/  :++++++++++++///+++++++++++++`    -ooooooooo//+oooooooooooo/ 
     :yyyyyyyyyyyyyyyyyyyyyyyyyyyy+`   :++++++++++/`    -++++++++++++      ./oooo-     /ooooooooooo`
     `oyyyyyyyyyyyyyyyyyyyyyyys+-`     :++++++++++`      :++++++++++++///////++o+      `ooooooooooo.
       .://oyyyyyyyyyyyyyy/:.`         :++++++++++:`    .+++++++++++++ooooooooooo:    `/ooooooooooo`
           :yyyyyyyyyyyyyy.            :++++++++++++///++++++++++++++.ooooooooooooo+++oooooooooooo/ 
           :yyyyyyyyyyyyyy.            :++++++++++++++++++++++++++++- -oooooooooooooooooooooooooo+` 
           :yyyyyyyyyyyyyy.            :+++++++++++++++++++++++++++-   .oooooooooooooooooooooooo/`  
           :yyyyyyyyyyyyyy.            :+++++++++++++++++++++++++:`      :oooooooooooooooooooo+.    
           :yyyyyyyyyyyyyy.            :++++++++++++++++++++++/-`          ./oooooooooooooo+:`      
           .//////////////`            .-------------------.`                 `.-:////::-.
        """
        draw.multiline_text((int(floor(int(pos_x))), int(floor(int(pos_y)))), pbs_ascii, fill=fill_color, align="center")
        del draw
        return img