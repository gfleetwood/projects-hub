# One Doc

## Overview

A proof of concept written in PyQt5 for a text only, lightweight, integrated version of Google Docs, Sheets, and Slides put together (or Microsoft Word, Excel, and Powerpoint, if you prefer). 

Two things have always bothered me about the docs-sheets-slides paradigm:

1. The bloat and opacity of having all three as separate programs disguised as hideous xml.

2. The unconnected nature of the three. Why can you only add a new sheet to Excel? Why not choose whether you want a document, sheet, or slides? This most comes to the fore when I see people shoving documentation into spreadsheets.

One Doc isn't a cure all but as a single markdown file it's flexible and transparent. Here's an example:

```
# Document

## Testing

Hello World.

# Spreadsheet

| Tables        | Are           | Cool  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | $1600 |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |

# Slides

## Title Slide

author: John Doe
date: February 7th, 2013

## Slide 1

- Bullet 1
- Bullet 2
- Bullet 3
```

The One Doc desktop app parses this into three tabs.

## Future

This may be enough to satisfy my curiosity, but if not, here are some things I need to do:

* Add editing

* Allow for an arbitrary number of docs, sheets, and slides.

* Add a table of contents for documents.

* Allow a table to be stored as a markdown table or csv.
