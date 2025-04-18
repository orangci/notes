+++
title="This Website"
date="17.04.2025"
short_desc="How I built my websites."
+++

To be clear, I'm covering both websites, this one (notes.orangc.net) and my main webpage (orangc.net).

## orangc.net
Currently it's on version four (version three is at https://orangc.net/v3). This time around I rewrote it using [FlyonUI](https://flyonui.com), a TailwindCSS library, instead of directly using Tailwind. Version 3 wasn't bad looking at all on desktop, but it was cramped on mobile. I had also been wanting to add some new features, so in v4:

- I finally made my website themable with a fun little toggle menu.
- I separated major sections into tabs in a navbar.
- I made it actually look somewhat decent on mobile.

You might notice a `package.json` in the source code. That's for getting Tailwind, FlyonUI, and the icon libraries (from iconify, mostly Tabler) to build during development. The site is still a static site in HTML.

## notes.orangc.net
This is version two of this webpage. Version one was built with Hugo, and a messily edited Hugo theme, [Archie](https://github.com/athul/archie). Everything was very much a mess because of the way I screwed around with things, so I decided to do something simple this time.

Instead of using a framework like Hugo, I'd write a small Python script. I thought this would be difficult, but it turned out to be an overwhelming success, primarily because I didn't have to write a markdown parser myself — I used the [mistune](https://mistune.lepture.com/) library.

The script is exactly 100 lines and runs..., well, take a look:

```
❯ time python3 main.py

real	0m0.308s
user	0m0.254s
sys	    0m0.037s
```

Which is fairly impressive, in my opinion. I'll break it down:

- The script goes through all the entries in the posts list in the main page and deletes them.
- It iterates over every note (located within `/src`) and adds it to the posts list in the main page.
- It then copies `/template.html` for each post within `/src` and inserts the post content, title, date, and short description (used for metadata) into the correct places.

### Conclusion

I rewrote both websites in the span of a day, which felt good.

- Both websites' **source code** are licensed under [GNU AGPLv3](https://choosealicense.com/licenses/agpl-3.0/).
- Both websites' **contents** are licensed under [CC BY-SA 4.0](https://choosealicense.com/licenses/cc-by-sa-4.0/).