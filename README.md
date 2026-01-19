# bgboxmaker

A tool to generate tuck boxes for board game storage.

# Installation
```
pip install bgboxmaker
```

# Usage
```
> bgboxmaker filename.yaml
```
To generate a tuck box you will need to create a YAML file with configuration information. The ***YAML Configuration*** section of this page will provide the details. A very basic tuck box can be generated with only the box dimensions being provided, but additional information allows for better looking and more customized boxes.

Running the above command will generate an image preview of your created box. Simply save this preview with whatever name you want, or print it directly from the preview.

**IMPORTANT**: When printing the generated image, you will want to specify that you want to print without print margins, or fill the entire paper. Safe print margins are built into the image, if the image is resized to not fill the entire page your box will be too small for your cards.

# YAML Configuration
## Required
A basic tuck box of the requested size can be generated with only these sections in the YAML file.
### Dimensions
```
dimensions:
  height: 3.5
  width: 2.5
  depth: 0.75
```
The dimension block specifies the dimensions of your finished tuck box. The height and width refer to the height and width of an individual card, this will be the size of the front of the box. Depth refers to the side of the box, and should be large enough to include the number of cards you are storing.

Values should be close to the height and width of the cards you want to store, to ensure a good fit, but it can be helpful to make the box very slightly bigger, especially in height and width, to keep things from being too snug. You should also include extra room if you intend to use card sleeves.

The module assumes measurements are in inches. If you want to use another unit to specify the dimensions you will also need to add an appropriate 'page' section (as described in the optional configuration section below) that specifies the resolution and page size in those units.

## Optional
Optional configuration allows you to further customize and improve the look of your tuck box.

### Page
```
page:
  height: 8.5
  width: 11
  resolution: 300
  margin: 0.25
  thickness: 4
```
The **page** block allows you to specify an alternate expected paper size, resolution, and print margin, with the defaults as listed.

Specifying a different resolution and page size will also allow you to assume different units of measurement. Defaults to the settings above, assuming inches.

Thickness is provided in pixels, and controls how much the tabs are inset. This thickness will be shaved from the sides of all tabs to help them fit better inside the box. If you are using thicker paper and having difficulty closing the box this number can be increased to make the tabs slightly smaller.

### Font
```
font:
  name: Ariel.ttf
  size: 90
  color: black
  stroke: white
  width: 1
```
Sets the font to use for text elements across the box. Can be overridden, fully or partially, for individual text elements defined in **Features** below.

#### Name
The full file name of the font. Can include the path to the font file, but it will look through installed fonts if you only provide the filename.

#### Size
The font size to use for text elements. Defaults to 90. The font size will automatically be scaled down as required to make the text element fit within the margins of the section it appears in.

#### Color
The color of text to use. Defaults to black.

#### Stroke
The color to use for text. Defaults to white.

#### Width
The stroke width for text. Defaults to 1 pixel.

### Image Source
```
image_source: ./images/
```
If your images are not in the same folder as your YAML file, you can use the **image_source** configuration to provide a short path. Will automatically be added to the front of any image references.

### Background
```
background:
  color: red
  image: myimage.png
```
Changes the background of the entire box. You can specify either color or an image file.

Colors can be specified by name, many common names will work, or you can specify a hexadecimal value for your color. If you use hexadecimal be sure to include the leading # and use quotation marks.
```
background:
  color: "#FF0000"
```
If you choose an image background you must specify the path to the image, unless you have also set up an image_source option. The chosen image will be resized to fit the height or width of the unfolded box, whichever allows the image to cover the full area. Some portions of the image will be lost in the negative space when you cut out the box. Low resolution images may look very bad when scaled up, so choose accordingly. Can accept any image format readable by the python Pillow module.

If both image and color are specified, only the image will be seen.

### Margin
```
margin: 0.1
```
Specifies a margin (in units defined by the **page** block resolution) to use when placing box features (text, images). This ensures a small set amount of space around text or image elements for the entire box. Can be overridden for specific sides in the **detail** section below. Defaults to 30 pixels (one tenth of an inch in the default resolution).

If a particular section of the box, usually the sides, is small enough that the margin takes up most or all of the space for that section the margin will automatically shrink in response.

Not to be confused with the print margin specified in the **page** block.

### Title
```
title: Game's Title
```
If the game's title is provided it will appear by default on the front of the box, and on the sides and ends. It will also appear as information on your final box image.

To override the default behaviors, see the "features" option under "detail".

### Subtitle
```
subtitle: Subtitle
```
If a subtitle is provided along with a title, it will appear by default underneath the title on the front of the box, and combined with a colon on the sides and ends. This can be useful for designating expansions for games.

To override the default behaviors, see the "features" option under "detail".

### Extra
```
extra: 1/2
```
If extra text is provided, it will appear by default at the bottom of the front of the box. This can be used to convey additional information about what the box contains. It can be used to designate that a box is number 1 of 2 if a single box can't be big enough to contain all of your cards, or it can be used to designate that the box contains a particular type of card for a certain game, if the game contains different decks. Anything that you would like to use to keep organized.

To override the default behaviors, see the "features" option under "detail".

### Detail
```
detail:
  ...
```
Fine grain control over the details of individual sections of the box. See the **Details and Features** section below for more information.

# Detail
```
detail:
  Front:
    background:
      color: FFFFFF
      image: myimage.jpg
    rotated: true
    orientation: landscape
    margin: 30
    grid: [2, 2]
    features:
      ...
```

The top level **background**, **title**, **subtitle**, and **extra** options are meant to provide a decent looking box with minimal configuration. If you want more direct control over the look of your box, you will need to start specifying additional detail options here.

All of the sub configurations are still entirely optional.

The first level of configuration under detail should be the name of the box side that you want to customize.

Available options are:
- Front
- Back
- Left
- Right
- Top
- Bottom
- TopTab
- BottomTab
- Sides
- Ends

Names are case sensitive.

Sides will apply to both Left and Right.

Ends will apply to both Top and Bottom.

If you do add both Sides and Left or Right, or Ends and Top or Bottom, the Sides or Ends details will be overwritten by the more specific configuration.

## Detail Options
### Background
Same as the Background option for the main box, the detail background option lets you change the background color or image for a single section.

Either can be specified, if both are present, the image will be used.

### Rotated
Set to "true" or "false". Allows the sides to be rotated.

The default is for the left, right, top, and bottom sides to be readable right-side up when the front of the box is facing upward. Changing this value will rotate a side 180 degrees, for situations where that is preferable.

Left, Top, and TopTab have rotated default to true. All other sides default to false.

### Orientation
Can only be set to "portrait" or "landscape". Sets the orientation of the other features (background, text, images, etc) on that side.

Front and Back default to portrait orientation, the sides, top and bottom default to landscape.

### Margin
See description of **margin** option for the box above. Allows you to override the set margin for this section.

### Grid
This option allows you to set up a location grid for use with the **features** option below. If it is omitted the grid will default to [2, 2].

For more detailed information on grid placement, see the *Grid Placement* documentation below.

### Features
Provide an optional list of additional features you want on this section of the box. Features should be provided as a YAML list of dictionaries, the format will look something like the following:
```
detail:
  Front:
    features:
      - option1: setting
        option2: setting
      - option1: setting
        option2: setting
        option3: setting
      - option1: setting
        option2: setting
```
This would configure three different features, each new feature needs to begin with a hyphen, and all of the options for that feature should be on the line with the hyphen and the following lines, matching alignment.

Features are rendered in order, allowing a later feature to overlap an earlier one.

# Features
Using features gives you the most fine grained control over the look of your box.

Providing a list of features for the Front, Sides, or Ends will overwrite the default features that add text for the **title**, **subtitle**, and **extra** options.

## Common Feature Options
```
detail:
  Front:
    features:
      - type: Panel
        width: 3
        height: 2
        place: [1, 1]
        anchor: [1, 1]
```

### Type
Every feature must have a specified type. Available types and additional options allowed with that type are described below in the ***Feature Types*** section.

### Place
This option works with the ***grid*** option above, along with the ***anchor*** and ***align*** options to allow for very specific placement of this feature on the box section.

Place expects two numbers, given as [x, y]. The x is the point along the width of the grid, and the y is the point along the height of the grid.

For more detailed information, see the *Grid Placement* documentation below.

### Anchor
This allows you to specify where an image or piece of text is placed in relation to it's specified **place**. It is given as [x, y], where x is its horizontal placement (left: 0, center: 1, or right: 2), and y is its vertical placement (top: 0, center: 1, bottom: 2).

An anchor of [1, 1] will center the text or image directly at its **place**. An anchor of [0, 0] will put the upper left of the text or image at **place**, and [2, 2] will put the lower right of the text or image at **place**.

For example, if you want an item placed in the lower left of your section, an anchor of [0, 2] will make sure that the full text or image is visible.

### Width and Height
Allows you to set a specific width and / or height, in the units of the page (see the **page** description above.)

If neither is present, the feature will be rendered at its natural size.

If only one is requested, the feature will maintain its natural aspect ratio if it has one.

If both are requested, the feature will squish or stretch as needed to reach the new aspect ratio.

In any case, if either the height or width requested is larger than the available space on this section, the feature will be reduced in size until it fits.

Some feature types will react slightly differently to width and height requests, these changes will be described with each feature type.

## Feature Types
Each feature must specify one of the following types.

### Text
```
detail:
  Front:
    features:
      - type: Text
        text: Game Title
        font:
          name: Garamond.tf
          size: 40
```

```
detail:
  Front:
    features:
      - type: Text
        text:
          - This is a block
          - of multiline text
          - that will be able to
          - be placed in your section.
        align: center
```
You can use a text feature to display text information anywhere on your box.

If width and / or height are specified along with a text feature, they will provide a maximum size, but will not resize the text larger to fit, and will not alter the aspect ratio of the text.

#### Text
The text used is defined by the text option, as seen above. This can be given as a single text string, as in the first example, or as a multi-line string, separated by hyphens as shown in the second example. If text is not provided nothing will appear on the box.

#### Align
Define the text alignment: left, centered, right, justified. Only really applies with multi-line text.

#### Font
Takes the same options as the **font** option for the main box. Overrides the font settings used for this piece of text.

Any missing options will use whatever setting is defined for the box font.

### Image
```
detail:
  Front:
    features:
      - type: Image
        image: image.png
```
Allows you to place an image on this section.

#### Image
Name of the image to use. Must include the path if the **image_source** option has not been defined.

### Panel
```
detail:
  Front:
    features:
      - type: Panel
        color: gray
        width: 2
        height: 3
        border:
          color: black
          width: 5
```
Renders a simple panel image. Requires that **color**, **width**, and **height** be defined.

#### Color
The backing color of the panel.

#### Border
If given, will render a border around the panel in the requested color. If border is present, its color must be set.

Border width defaults to 5 if not provided.

# Grid Placement
The grid placement system is used with a detail feature to precisely specify a location to place a feature without the need to get into direct measurement.

To understand the use of **grid** and **place**, picture one section of your box, let's say the front, as a simple rectangle. A grid is defined by two numbers: [x, y] where the x is the number of equal divisions of that box along its width, and y is the same for the height. The grid itself is made up of the intersections of the lines that surround those sections.

A grid of [1, 1] doesn't divide the box at all, since the whole rectangle is used both horizontally and vertically. This will create four grid points, one in each of the corners.

A grid of [1, 2] divides the box into two vertical sections, so now you will have six grid points: the original four corners, and the two new points along the left and right side along the dividing line.

A grid of [2, 2] divides the box into two vertical sections and two horizontal sections. Now you have grid lines along both sides, the top and bottom, and two additional lines through the center of the rectangle. That gives you nine different grid points across the corners, the centers of the outside lines, and the center of the rectangle.

This division process can continue for as many sections and grid lines as you need to get the placement you want.

With whatever grid size you choose, each feature can specify a specific **place** on that grid, again with an [x, y] specification. The x is the grid line (0 to grid size) along the width, and the y is the grid line (0 to grid size) along the height.

So, if you want to just center an item you can specify a grid size of [2, 2], and give the item a place of [1, 1]. If you want to center something in the top half of a box you can use a grid size of [2, 4], and a place of [1, 1]. The vertical center would be place [1, 2], and the center of the bottom half would be [1, 3].

For any grid [0, 0] will always be the upper left, and [x, y] will be the lower right, where x and y are the size of the grid.

For even further control over location you can combine the **grid** and **place** options with **anchor** and **align**.


# TODO
- Finish implementing BoxConfig
- implement width and height for images
- implement width and height for text
- implement panel feature type
- change feature implementation to include type as described
- update font option to match new description, implement font option for text features
- add fold lines
- remove "sample" option, make filename a required argument
- Include try logic and exceptions for all file loads (YAML, images, fonts)



When the feature render image comes back we know it will fit within the hard boundary of the section, because we already adjusted the requested bounds down to fit within it regardless of the case. We would then need to adjust the final position of the feature as needed to try to honor the anchor request, and if that puts portions of the feature image out of bounds we just pull it back in.

I think that means that the only remaining question is how to do feature rotation. It would be a nice feature to have. I think it's not too bad for images, we can just have the user supply a rotation degree and perform that rotation before we do our resizing to make sure the image fits within the bounds. It may produce some odd results if we are also adjusting the image aspect ratio. There it seems like the logical thing to do would be to do the aspect ratio adjustment before the rotation, and then resize again if needed to make it fit the bounds. That will likely be the result most expected by the end user. If they take a rectangular image, ask for it to be squished square and rotated, they will expect a rotated square. If we rotate first and then do the aspect ratio change we would end up with a weird parallelogram or something.

Ok, yes, so for images we allow rotation as an option, we load the image, change the aspect ratio if needed, do the rotation, and then do a final bounds recheck. Normally the aspect ratio change would also resize it to fit within the bounds, but the rotation could change that. If there is no rotation the check will pass and it won't need to be resized again.

Text feels like it will be a lot harder, since we generate it based on changing the font size and ensuring it fits within the bounds. We don't have a way to check to see if it fits in the bounds after an arbitrary rotation. The math gets wickedly complicated really fast. We would need to essentially rotate the bounding box, and then create a new bounding box within the rotated bounding box to make sure that the text didn't cross any of the lines, and honestly I'm not at all sure how to approach that.

So instead, maybe we allow limited rotation for text. The user can specify a rotation, but it has to be cardinal. -90, 90, or 180 only. In those cases the bounding box is clear, it's the same for 180 as it would be normally, and the width and height are inverted for the other two. That would allow the user to override the orientation and direction for a single feature on a section without needing to impact all of them.

Panels would probably be the same as images, since they would work essentially the same way. We create the panel with the requested width and height, setting the aspect ratio appropriately, rotate, and then resize as needed to fit within the bounds.

I guess we could allow the user to rotate the text, just doing so after the text image is generated, with the caveat that rotation will cause a resize after the render.

With that approach we can move the rotation and post rotation resize logic to the common feature renderer, and treat all features the same in this regard. The requested height and width of the feature element would then be correct pre-rotation, only scaled down if it no longer fits within the bounds. An appropriately sized and placed text image should be unmodified and work just fine, the user will only see issues if it doesn't fit post rotation, since the relative size of the stroke would shrink as well. Being careful with their design should mitigate that, and they get full functionality.

Ok, that works. Rotation, in degrees, becomes a common feature setting and is applied to the rendered feature before it is finally placed. And we reduce code duplication by no longer needing to perform the rotation logic in both the image and panel features, or any additional features we add later. And text becomes fully rotatable with only a slight warning about the resizing in the documentation.