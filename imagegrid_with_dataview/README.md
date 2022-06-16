# Imagegrid with Dataview

If you save one image per day, like me, it can be a nice feat to display all of your week's images in a grid on your weekly note - all you need is a dataview query and a bit of css. You can use that, of course, for other use cases as well.

![Imagegrid with Dataview Example](Imagegrid%20with%20Dataview.png)

_Thanks to Unsplash for the images!_

## Prerequisites

- Dataview in it's newest version (0.5.x)
- A metadata field with a embedded image file

## How to

Currently, it's necessary to use a dataviewjs block for that, in order to annotate the container with a css class to apply our styling. As soon as Issue [#675](https://github.com/blacksmithgu/obsidian-dataview/issues/675) is implemented, this'll be possible with a dataview query.

````javascript
```dataviewjs
const pages = dv.pages('"pathToYourImageFiles"')

dv.container.className += ' imagegrid'
dv.list(pages.image)
```
````

You can, of course, also search for a tag or filter your pages in whatever way you want to. If you want to use this for a weekly image grid and your weekly Notes are named like `2022-W23`, this should work:

````javascript
```dataviewjs
const yearAndWeek = dv.current().file.name.split('-W')
const pages = dv.pages('"pathToYourDailyNotes"').where(p => p.date && p.date.year == yearAndWeek[0] && p.date.weekNumber == yearAndWeek[1])

dv.container.className += ' imagegrid'
dv.list(pages.foto)
```
````

Now you'll have a list of your embedded images. A bit of css (and this is improvable) makes it look like above:

```css
.imagegrid ul {
  display: flex;
  flex-wrap: wrap;
  flex-direction: row;
}
.imagegrid ul li {
  display: flex;
  flex-direction: column;
}
.imagegrid ul li::marker {
  content: "";
}
/* I wanted to ignore the width on the images and set a fixed one for them.
Remove if you want to preserve the width configured on the image link itself. */
.imagegrid ul li img, .markdown-rendered img:not([width]) {
  max-width: 200px;
}
```

## Step-by-Step

1. Place this dataview block in your weekly note:

````javascript
```dataviewjs
const yearAndWeek = dv.current().file.name.split('-W')
const pages = dv.pages('"pathToYourDailyNotes"').where(p => p.date && p.date.year == yearAndWeek[0] && p.date.weekNumber == yearAndWeek[1])

dv.container.className += ' imagegrid'
dv.list(pages.foto)
```
````

2. Insert the right folder name respective the right filter criteria. If everything is alright, you should have a bullet point list with rendered images
3. Download "dataview-imagegrid.css" and put it into your [CSS Snippets folder](https://help.obsidian.md/How+to/Add+custom+styles)
4. Activate it in the settings under "Appearance" -> "CSS Snippets"
5. Done!
