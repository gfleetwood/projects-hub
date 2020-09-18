# Audiobook Maker

## Overview

A command line pipeline to go from a pdf to an mp3 via Google's Text To Speech API. There is support for a partial pipeline where a web article is the mp3 source.

## Usage

Ensure that you're located in this directory. The full pipeline leans on pyinvoke:

* invoke txt_build --file PATH/FILE.pdf invoke mp3_build --file PATH/FILE.txt

The first call (build1) writes to PATH/FILE.txt.

The web article to mp3 pipeline:

* python txt-to-mp3.py --txt_from_web=0 --source=FILE.txt

* python txt-to-mp3.py --txt_from_web=1 --source=URL

For completeness, if you only want to do TTS:

* Rscript pdf_ex.R --file FILE.pdf

## Future

If I return to this project I'd build a desktop or web app which allows for url pasting or file uploading.