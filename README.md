# serverless-its

ITS (Image Transform Service) performs transformations on images by accepting transform requests in the form of query strings.

## Crop

There are three varieties of crop -- default, focal and smart crop.

### _Crop (Default)_

The default crops the input image about the center of the image. The image will be resized down first, depending on the lesser dimension of the image.

To use this crop, use the `crop` keyword with **two** arguments split by x's:

> https://image.pbs.org/path/to/file.jpg?crop=WWxHH

Where:

- crop -- indicates that ITS should perform a crop and use the middle of the image as the focal point for the crop.
- WW -- a numerical pixel value representing the desired width of the output image
- HH -- a numerical pixel value representing the desired height of the output image

#### Example

Original Image:

> https://image.pbs.org/video-assets/5jJewwH-asset-mezzanine-16x9-esGHBDK.png

![A Chocolate Cake](https://image.pbs.org/video-assets/5jJewwH-asset-mezzanine-16x9-esGHBDK.png)

Applying `crop`:

> https://image.pbs.org/video-assets/5jJewwH-asset-mezzanine-16x9-esGHBDK.png?crop=700x200

![A Cropped Chocolate Cake](https://image.pbs.org/video-assets/5jJewwH-asset-mezzanine-16x9-esGHBDK.png?crop=700x200)

### _Focal crop_

Focal crop returns an image focused around a user-specified point in the original image of a user-specified size. To use this crop, utilize the `crop` keyword with **four** arguments split by x's:

> https://image.pbs.org/path/to/file.jpg?crop=WWxHHxXXxYY

Where:

- crop -- indicates that ITS should perform a crop
- WW -- a numerical pixel value representing the desired width of the output image
- HH -- a numerical pixel value representing the desired height of the output image
- XX -- the x axis of the focal point, represented as a percentage value of the **width** of the original picture
- YY -- the y axis of the focal point, represented as a percentage value of the **height** of the original picture

#### Example

Original Image:

> https://image.pbs.org/test/GmtpBa4-asset-mezzanine-16x9-Uu2CpNc.png

![A Key Lime Pie](https://image.pbs.org/test/GmtpBa4-asset-mezzanine-16x9-Uu2CpNc.png)

Applying `crop` with four parameters:

> https://image.pbs.org/test/GmtpBa4-asset-mezzanine-16x9-Uu2CpNc.png?crop=500x400x90x10

![A cropped Key Lime pie](https://image.pbs.org/test/GmtpBa4-asset-mezzanine-16x9-Uu2CpNc.png?crop=500x400x90x10)

### _Smart_

Smart crop returns an image focused around a user-specified point in the original image of a user-specified size. To use this crop, the input image _filename_ must end in `_foucs-XXxYY.ext`, and then you can use the `crop` keyword with **two** arguments split by x's:

> https://image.pbs.org/path/to/file_focus-XXxYY.ext?crop=WWxHH

Where:

- XX -- the x axis of the focal point, represented as a percentage value of the height of the original picture
- YY -- the y axis of the focal point, represented as a percentage value of the height of the original picture
- crop -- indicates that ITS should perform a crop
- WW -- a numerical pixel value representing the desired width of the output image
- HH -- a numerical pixel value representing the desired height of the output image

#### Example

Original Image:

> https://image.pbs.org/test/Sjk2Eqs-asset-mezzanine-16x9-0gsKw4z_focus-90x10.png

![A hand holding a knife that is cutting bread](https://image.pbs.org/test/Sjk2Eqs-asset-mezzanine-16x9-0gsKw4z_focus-90x10.png)

Applying `crop`:

> https://image.pbs.org/test/Sjk2Eqs-asset-mezzanine-16x9-0gsKw4z_focus-90x10.png?crop=300x400

![A hand holding a knife that is cutting bread](https://image.pbs.org/test/Sjk2Eqs-asset-mezzanine-16x9-0gsKw4z_focus-90x10.png?crop=300x400)

## Overlay

Overlay returns the input image with the specified overlay image placed on top of it. The overlay is placed according to the expected position of its top left corner as input by the user. To use overlay, use the `overlay` keyword:

> https://image.pbs.org/path/to/file.jpg?overlay=PXxPYx<overlay_img_path>

Where:

- overlay -- indicates that ITS should put an overlay on the input image
- overlay_img_path -- path to the overlay (optionally, can be a keyword a keyword in the OVERLAYS dictionary in settings)
- PX -- the x axis of the top left corner of the overlay image, represented as a percentage value of the height of the original picture (default is 50%)
- PY -- the y axis of the top left corner of the overlay image, represented as a percentage value of the height of the original picture (default is 50%)

#### Example

Original Image:

> https://image.pbs.org/test/QdTpmRS-asset-mezzanine-16x9-zaTWonY.png

![Sweet buns](https://image.pbs.org/test/QdTpmRS-asset-mezzanine-16x9-zaTWonY.png)

Original Overlay Image:

> https://image.pbs.org/test/rose-1385970_960_720.png

![Rose](https://image.pbs.org/test/rose-1385970_960_720.png)

Image Credit: https://pixabay.com/en/rose-orange-blossom-bloom-flower-1385970/

Result Image:

> https://image.pbs.org/test/QdTpmRS-asset-mezzanine-16x9-zaTWonY.png

![Citizen-Kane-Overlay-Rosebud](https://image.pbs.org/test/QdTpmRS-asset-mezzanine-16x9-zaTWonY.png?overlay=20x15/test/rose-1385970_960_720.png)

## Resize

Resize returns a resized version of the original image **without distortion of the aspect ratio**. To use it, use the `resize` keyword with **two** arguments split by x's:

> https://image.pbs.org/path/to/file.jpg?resize=WWxHH

Where:

- resize -- indicates that ITS should perform a resize transform
- WW -- a numerical pixel value representing the desired width of the output image
- HH -- a numerical pixel value representing the desired height of the output image

Note: Resizing to a larger size isn’t recommended, as it will compromise image quality.

Note: Inputing a single value (either an expected width size or an expected height size followed by an 'x') is also supported.

Example

Original Image:

> https://image.pbs.org/video-assets/GTdD9Rq-asset-mezzanine-16x9-d3h7qCm.jpg

![A flowery cake](https://image.pbs.org/test/GTdD9Rq-asset-mezzanine-16x9-d3h7qCm.jpg)

With `resize` applied:

> https://image.pbs.org/video-assets/GTdD9Rq-asset-mezzanine-16x9-d3h7qCm.jpg?resize=400x200

![A resized flowery cake](https://image.pbs.org/test/GTdD9Rq-asset-mezzanine-16x9-d3h7qCm.jpg?resize=400x200)

With `resize` applied and only a width supplied:

> https://image.pbs.org/video-assets/GTdD9Rq-asset-mezzanine-16x9-d3h7qCm.jpg?resize=400x

![A resized flowery cake](https://image.pbs.org/video-assets/GTdD9Rq-asset-mezzanine-16x9-d3h7qCm.jpg?resize=400x)

## Format

Format returns the input image in the specified type, rather than being left as the original image’s type. It currently supports conversion to JPG, PNG, and WEBP. To use it, use the `format` keyword with the file extension as an argument:

> https://image.pbs.org/path/to/file.jpg?format=ext&quality=<integer>

Where:

- format -- indicates that ITS should perform a format transform
- ext -- the requested output type. Can only be `jpg`, `png` or `webp`
- quality -- _optional_, allows user to specify the quality that they would like the output image to have. Currently, this parameter only works with the `jpg` format. Accepts a multiple 10 up to 100.

Example

Original Image: ![Citizen-Kane](http://i.imgur.com/pFndG84.jpg)
Image Credit: https://commons.wikimedia.org/wiki/File:Citizen-Kane-Welles-Coulouris.jpg

> API_URL/demo/citizen_kane.jpg?format=png&quality=10

Result Image: ![Citizen-Kane-PNG-10](http://i.imgur.com/CItOntv.jpg)

## Combination

All of the transforms described above can be combined into one query by separating them with `&`.

Example
The following query resizes the input JPG image, applies an overlay to it:

Original Image: ![Citizen-Kane](http://i.imgur.com/pFndG84.jpg)
Image Credit: https://commons.wikimedia.org/wiki/File:Citizen-Kane-Welles-Coulouris.jpg

Original Overlay Image: ![Rosebud-Sled](http://i.imgur.com/RZcKnYD.png)

Image Credit: https://pixabay.com/en/luge-sled-sledge-sleigh-sport-1295072/

> API_URL/demo/citizen_kane.jpg?resize=1200x1200&overlay=10x50ximages/sled.png

Result Image: ![Citizen-Kane-Combination](http://i.imgur.com/vmZuz7k.jpg)
