# serverless-its
ITS rewrite

ITS (Image Transform Service) performs transformations on images by accepting transform requests in the form of query strings. 

## Crop

There are three varieties of crop -- default, focal and smart crop.

*Default*

The default crop crops the input image about the center of the image. To use this crop, use the crop keyword with two arguments split by x's:

<http://images.pbs.org/<file_path/filename.ext>?crop=WWxHH>

Where:
* crop -- indicates that ITS should perform a crop and use the middle of the image as the focal point for the crop.
* WW -- a numerical pixel value representing the desired width of the output image
* HH -- a numerical pixel value representing the desired height of the output image

Example

Original Image: ![Citizen-Kane](http://i.imgur.com/pFndG84.jpg)
Image Credit: https://commons.wikimedia.org/wiki/File:Citizen-Kane-Welles-Coulouris.jpg

>http://images.pbs.org/demo/citizen_kane.jpg?crop=1000x1000

Result Image: ![Citizen-Kane-Crop-1000x1000](http://i.imgur.com/meMAv8Q.jpg)

*Focal*

Focal crop returns an image focused around a user-specified point in the original image of a user-specified size. To use this crop, utilize the crop keyword with four arguments split by x's:

<http://images.pbs.org/<file_path/filename.ext>?crop=WWxHHxXXxYY>

Where:
* crop -- indicates that ITS should perform a crop
* WW -- a numerical pixel value representing the desired width of the output image
* HH -- a numerical pixel value representing the desired height of the output image
* XX -- the x axis of the focal point, represented as a percentage value of the height of the original picture
* YY -- the y axis of the focal point, represented as a percentage value of the height of the original picture

Example

Original Image: ![Citizen-Kane](http://i.imgur.com/pFndG84.jpg)
Image Credit: https://commons.wikimedia.org/wiki/File:Citizen-Kane-Welles-Coulouris.jpg

>http://images.pbs.org/demo/citizen_kane.jpg?crop=1000x1000x15x30

Result Image: ![Citizen-Kane-Focal-1000x1000x15x30](http://i.imgur.com/U3gdnmf.jpg)

*Smart*

Smart crop returns an image focused around a user-specified point in the original image of a user-specified size. To use this crop, the crop keyword and include the focal parameters in the filename of the input image: 

<http://images.pbs.org/<file_path/filename_focus-XXxYY.ext>?crop=WWxHH>

Where:
* crop -- indicates that ITS should perform a crop
* HH -- a numerical pixel value representing the desired height of the output image
* XX -- the x axis of the focal point, represented as a percentage value of the height of the original picture
* YY -- the y axis of the focal point, represented as a percentage value of the height of the original picture

Example

Original Image: ![Citizen-Kane](http://i.imgur.com/pFndG84.jpg)
Image Credit: https://commons.wikimedia.org/wiki/File:Citizen-Kane-Welles-Coulouris.jpg

>http://images.pbs.org/demo/citizen_kane_focus-50x15.jpg?crop=1000x1000

Result Image: ![Citizen-Kane-Smart-1000x1000x50x15](http://i.imgur.com/5w5e8lR.jpg)

## Overlay

Overlay returns the input image with the specified overlay image placed on top of it. The overlay is placed according to the expected position of its top left corner as input by the user. To use overlay, use the overlay keyword:

<http://images.pbs.org/<file_path/filename.ext>?overlay=PXxPYx<overlay_img_path>>

Where:
* overlay -- indicates that ITS should put an overlay on the input image
* overlay_img_path -- path to the overlay (optionally, can be a keyword a keyword in the OVERLAYS dictionary in settings)
* PX -- the x axis of the top left corner of the overlay image,  represented as a percentage value of the height of the original picture (default is 50%)
* PY -- the y axis of the top left corner of the overlay image, represented as a percentage value of the height of the original picture (default is 50%)

Example

Original Image: ![Citizen-Kane](http://i.imgur.com/pFndG84.jpg)
Image Credit: https://commons.wikimedia.org/wiki/File:Citizen-Kane-Welles-Coulouris.jpg

Original Overlay Image: ![Rosebud](http://i.imgur.com/pOH6LJf.png)

Image Credit: https://pixabay.com/en/rose-orange-blossom-bloom-flower-1385970/

>http://images.pbs.org/demo/citizen_kane.jpg?overlay=20x15/demo/rosebud.png

Result Image: ![Citizen-Kane-Overlay-Rosebud](http://i.imgur.com/BcMqXXT.jpg)

## Resize

Resize returns a resized version of the original image without distortion of the aspect ratio. To use it, use the resize keyword:

<http://images.pbs.org/<file_path/filename.ext>?resize=WWxHH>

Where:
* resize -- indicates that ITS should perform a resize transform
* WW -- a numerical pixel value representing the desired width of the output image
* HH -- a numerical pixel value representing the desired height of the output image

Note: Resizing to a larger size isn’t recommended, as it will compromise image quality.
Note: Inputing a single value (either an expected width size or an expected height size followed by an 'x') is also supported.

Example

Original Image: ![Citizen-Kane](http://i.imgur.com/pFndG84.jpg)
Image Credit: https://commons.wikimedia.org/wiki/File:Citizen-Kane-Welles-Coulouris.jpg

>http://images.pbs.org/demo/citizen_kane.jpg?resize=700x400

Result Image: ![Citizen-Kane-Resize-700x400](http://i.imgur.com/CItOntv.jpg)

## Format

Format returns the input image in the specified type, rather than being left as the original image’s type. It currently supports conversion to JPG, PNG, and WEBP. To use it, use the format keyword:

<http://images.pbs.org/<file_path/filename.ext>?format=<ext>>&quality=<integer>>

Where:
* format -- indicates that ITS should perform a format transform
* ext -- the requested output type. Can only be JPG, PNG or WEBP
* quality -- *optional*, allows user to specify the quality that they would like the output image to have. Currently, this parameter only works with PNG and JPG outputs. Accepts a multiple 10 up to 100.

Example

Original Image: ![Citizen-Kane](http://i.imgur.com/pFndG84.jpg)
Image Credit: https://commons.wikimedia.org/wiki/File:Citizen-Kane-Welles-Coulouris.jpg

>http://images.pbs.org/demo/citizen_kane.jpg?format=png&quality=10

Result Image: ![Citizen-Kane-PNG-10](http://i.imgur.com/CItOntv.jpg)


## Combination
All of the transforms described above can be combined into one query by separating them with ‘&’.

Example
The following query crops the input JPG image, applies an overlay to it, and then outputs the result as a WEBP:

>http://images.pbs.org/demo/citizen_kane.jpg?crop=1000x1000&overlay=images/sled.png&format=wbep

