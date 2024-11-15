+++
title = 'Manga on Kindle'
date = 2024-11-13T09:18:01+03:00
draft = false
+++

Up until now I had usually read manga on my phone. However, I wanted to read it on my Kindle instead, for two reasons:
- Firstly, I read 75% of the books I read on my Kindle
- And secondly, I don't like looking at my phone right before bed
However, I had procrastinated on figuring out the process of transferring manga to my Kindle because it appeared to be one of those daunting tasks that take hours and many attempts to figure out. Thankfully, when I actually tried to yesterday, I lucked out and found an easy method of doing it.

### `mangal`
Firstly I downloaded [`mangal`](https://github.com/metafates/mangal), which is:

> A fancy CLI app written in Go which scrapes, downloads and packs manga into different formats

And used that to download manga — in my case [*'Tis Time For "Torture," Princess*](https://myanimelist.net/manga/119375/Himesama_Goumon_no_Jikan_desu) — as PDF files. Each chapter downloaded with mangal is an individual PDF.

If the sources that mangal has by default don't have the manga you want, you can add more. See the mangal-scrapers [repository](https://github.com/metafates/mangal-scrapers).

### `ghostscript`
If you download a manga with 251 chapters, that's 251 different PDFs, which will be ridiculously messy and annoying to deal with on the Kindle. So the next step is to merge all the PDFs into one singular PDF. I got ChatGPT to generate me a [ghostscript](https://www.ghostscript.com) command to do this:

`gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=merged_manga.pdf *`

Ran in the folder in which my manga was stored. Note that the asterisk at the end can be replaced with with individual paths to PDF files, like this:

`gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=merged_manga.pdf /home/orangc/docs/manga/Charlotte/01.pdf /home/orangc/docs/manga/Charlotte/02.pdf`

And so on.

### Calibre
[Calibre](https://calibre-ebook.com/) is an e-book management software which is very useful for a variety of things; in this situation, sending our final PDF to the Kindle.
I plugged my Kindle into my PC with a USB A to C cable.

1. In the top left, click the **Add Books** button, and select the merged_manga.pdf file from earlier.
2. Next, click the **Convert Books** button and convert the PDF now in your Calibre library to a `.MOBI` file. Note that you should fix up the metadata and select a cover image while doing so; the cover image can be found in the same directory that the merged_manga.pdf was originally in; the filename should be something like `cover.png`.
3. Ensure your Kindle is plugged into your PC/laptop with a cable and then click the **Send to Device** button.

And now you can read your manga in peace. 'Tis easy.