# img
automatically download a collection of images

## installation

### with `git clone`

```bash
$ git clone https://github.com/PlayerG9/img.git
```
`~/.bash_aliases`
```bash
source '/path/to/img/scripts/bashrc'
```

### with release
- go to [releases](https://github.com/PlayerG9/img/releases/latest)
- Download latest `img` file
- `chmod u+x img`
- and place it in `~/.local/bin/`

## usage
```bash
$ img get "https://github.com/PlayerG9/img/blob/main/example/001.png?raw=true"
$ ls
001.png
002.png
003.png
$ rm 001.png 002.png 003.png
$ img scrape "https://raw.githubusercontent.com/PlayerG9/img/main/example/gallery.html"
$ ls
001.png
002.ong
003.png
```
