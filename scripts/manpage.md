img(1) -- like wget but for many images at once
=============================================

## SYNOPSIS

- `img [-h] [-v] {update,grab,get,scrape} ...`
- `img grab [-h] [-S SKIPS] [-H | --history | --no-history] url`
- `img scrape [-h] [-A] [-W] [-H] url`

## DESCRIPTION

automatically download many images at once or scrape a website.

## OPTIONS

### grab/get

* url:
the starting url which is extended.
note: use {num} manually in case multiple numbers are increasing.
(eg: img get https://images.com/img_{01}_{90274}.png)

* -H, --history, --no-history:
whether to append the last attempted url to the command-history or not.
  (currently not working)

* -S, --skips:
how many urls/images are allowed to be missing before stopping

### scrape

* url:
the url of the website to scrape for images

* -W, --min-width:
minimum width of images to scrape them

* -H, --min-height:
minimum height of images to scrape them

* -A, --all-links:
without, scrape only downloads `<img src="...">` links.
With the `-A` option it also attempts to download the `<a href="..."><img/></a>`

### general options

* -h, --help:
show the help message and exit

* -v, --version:
show program's version number and exit

## EXAMPLES

    $ img get "https://raw.githubusercontent.com/PlayerG9/img/example/001.png"

    $ img scrape "https://raw.githubusercontent.com/PlayerG9/img/main/example/gallery.html"

<!--
## SYNTAX

## ENVIRONMENT

## RETURN VALUES

## STANDARDS

## SECURITY CONSIDERATIONS

## BUGS
-->

## HISTORY

This Project was renamed and extended from the `img-get` command to the nowadays more versatile `img` command

## AUTHOR

PlayerG9 - https://github.com/PlayerG9/

## COPYRIGHT

Copyright © 2023 PlayerG9.

## SEE ALSO

### Repository

https://github.com/PlayerG9/img

### Releases

https://github.com/PlayerG9/img/releases
