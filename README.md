![NcduColors preview](assets/images/colorful_preview.png "Preview of Ncdu fully Red, Green, Yellow, Blue, Magenta, Cyan")

![Dependencies: 0](https://img.shields.io/badge/dependencies-0-green?style=flat-square&logo=PyPi&logoColor=green)
![License: MIT](https://img.shields.io/github/license/Midblyte/NcduColors?style=flat-square&logo=Unlicense&color=blue&logoColor=blue)

# Table of content

> - [What is it?](#what-is-it)
>   - [Why?](#why)
>   - [Why not just contributing to Ncdu or forking it?](#why-not-just-contributing-to-ncdu-or-forking-it)
>   - [What about changing the default color palette?](#what-about-changing-the-default-color-palette)
> - [**How to use**](#how-to-use)
>   - [0. If you want to patch a _copy_ of Ncdu](#0-if-you-want-to-patch-a-copy-of-ncdu)
>   - [1. Extract the default configuration](#1-extract-the-default-configuration)
>     - [1.1 Make a backup](#11-make-a-backup)
>   - [2. Edit the configuration file](#2-edit-the-configuration-file)
>   - [3. Apply the new configuration](#3-apply-the-new-configuration)
>   - [4. Done](#4-done)
>   - [Reverting and recovering from errors](#reverting-and-recovering-from-errors)
> - [Table of reference](#table-of-reference)
>   - [Config object](#config-object)
>   - [Theme object](#theme-object)
>     - [Key object](#key-object)
>       - [Color object](#color-object)
>       - [Attribute object](#attribute-object)
> - [What has changed?](#what-has-changed)
> - [Disclaimer](#disclaimer)
> - [Future improvements](#future-improvements)
> - [License](#license)


## What is it?

NcduColors is a Python zero-dependency, pre-2.0 Ncdu themes patcher.

[Ncdu](https://dev.yorhel.nl/ncdu) (NCurses Disk Usage) is a text-user interface disk usage analyzer. It relies on the Ncurses library.


### Why?

> _"I really don't see why anyone would spend time theming a disk usage analyzer they (probably) won't use every day, so I'm hesitant to bloat ncdu with even more config options."_ - Ncdu developer

Software accessibility is a great issue. Ncdu users know it, too.

The [3-bit and 4-bit](https://en.wikipedia.org/wiki/ANSI_escape_code#3-bit_and_4-bit) basic terminal color palette is almost unusable. Every terminal software uses its own palette. No standard seems to be followed at all.

Because of this, the two colorful themes, `dark` and `darkbg`, are hardly usable for many.

![Example of the mess of 3-bit and 4-bit colors compatibility has caused](assets/images/broken_dark.png "Ncdu 1.15.1 dark theme on Konsole")

<sup>_Something is definitely off_</sup></div>

Many users ([first](https://code.blicky.net/yorhel/ncdu/issues/191),
[second](https://code.blicky.net/yorhel/ncdu/issues/202),
[third](https://code.blicky.net/yorhel/ncdu/issues/203), and so on) complained about color issues. I thought it'd be nice to find a solution which could work for the many, not only for me. Also, I use Ncdu a lot, so this definitely was not a waste of time (at the very least, it was a fun learning experience!).


### Why not just contributing to Ncdu or forking it?

Contributing or forking Ncdu was an option.

However, there are a few issues with this approach:

- The Ncdu developer [said](https://code.blicky.net/yorhel/ncdu/issues/191) he's quite hesitant to add more themes support to Ncdu.

- Even if the needed changes were to be made *now*, many users on LTS distributions couldn't benefit for months or even **years**. Think of Debian and Ubuntu-based distributions.

- Forks are harder to compile, to use, to install and to update for regular users. Also let's not fool ourselves, **Linux package management is a mess**.

- Forks rely on developers who fork the original project and are more prone to become [abandonware](https://en.wikipedia.org/wiki/Abandonware) due to their nature, rightfully expected to be "secondary" compared to the mainline project.

Instead, NcduColors's approach allows you to change colors **now** and **how** you want, while still retaining the possibility to update Ncdu officially, using your package  manager, whenever new versions are available (though you will have to re-patch it).

And: you can uninstall NcduColors while preserving your customised Ncdu.


### What about changing the default color palette?

This approach was considered on Ncdu's side, but I think that there will always be someone who doesn't like it. You can't always satisfy everyone when it comes to accessibility issues.

Thus, allowing everybody to painlessy (more or less) patch their own copy of Ncdu seemed the right choice to me.

Also: not everyone loves the black and white (`off`) theme.


## How to use

You have two choices:

- You can patch a **copy** of Ncdu (you won't - usually - need root permissions) 
  - start from [step 0](#0-if-you-want-to-patch-a-copy-of-ncdu)

- You can patch Ncdu in-place (you'll - most likely - need root permissions)
  - skip to [step 1](#1-extract-the-default-configuration)


### 0. If you want to patch a _copy_ of Ncdu

You need to _copy_ `ncdu` - namely `$(command -v ncdu)` - into another `$PATH` directory.

A safe choice could be `/usr/local/bin` - you can view all of them running `tr : '\n' <<< "$PATH"` (beware of the order of priority)

> Actually, you can copy Ncdu wherever you want.
> 
> A `$PATH` directory is needed just to be able to run Ncdu from anywhere.

> _From now on, all the steps are in common._
> _**Don't forget** to specify `--ncdu <PATH_TO_NCDU>` in the arguments._


### 1. Extract the default configuration

Run:

```bash
ncducolors extract-default-config ncdu-config.json
```

> In case of failure, please open an issue.

#### 1.1 Make a backup

It's a good practice to always make backups, even if not strictly needed.

```bash
cp ncdu-config.json ncdu-defaults.json
```

### 2. Edit the configuration file

Use your editor of choice to edit the values.
<u>_Don't_</u> edit the `offset`: it could corrupt the binary.

```bash
xdg-open ncdu-config.json
```

> Have a look to the [table of reference](#table-of-reference) for some help.

Once finished, **save** and go ahead.

### 3. Apply the new configuration

This is the first and only "dangerous" step - well, not really, since you can always [fix Ncdu](#reverting-and-recovering-from-errors).

Close Ncdu before applying the new configuration, or it won't work.

```bash
ncducolors apply-config ncdu-config.json
```

> If you are editing Ncdu in-place, you may need to run NcduColors as **root** (and, if you
installed NcduColors as an unprivileged user, this fixes the "command not found" error).
>
> ```bash
> sudo -E env "PATH=$PATH" ncducolors apply-config ncdu-config.json
> ```


### 4. Done

That's all. You can now run `ncdu` (or `./path/to/your/copy/of/ncdu`).

You can now either:
- Continue to improve your theme jumping back to [step 2](#2-edit-the-configuration-file).
- [Revert](#reverting-and-recovering-from-errors) to your default installation.
- Uninstall NcduColors.


### Reverting and recovering from errors

In case something goes wrong, or you just want the plain old Ncdu, don't worry. You can fix it quite easily.

1. Try to apply the default config using `ncducolors apply-config ./ncdu-defaults.json`
2. Try to revert using `ncducolors revert --config ./ncdu-config.json` (the config
   is needed just to obtain the offset - in fact, you can use `ncducolors revert --offset N` too)
3. If you did a [backup](#11-make-a-backup), use `cp backup-of-ncdu "$(command -v ncdu)"` (you may need to be `root`).
4. Reinstall Ncdu using your package manager of choice.


## Table of reference

### Config object

| key    | typed                                                              | notes                                                   |
|--------|--------------------------------------------------------------------|---------------------------------------------------------|
| ncdu   | [Path](https://docs.python.org/3/library/pathlib.html) (as string) | Overridden by `--ncdu`; autoresolved if `null`          |
| offset | Integer                                                            | Depends on the binary                                   |
| off    | [Theme](#theme-object)                                             | Black and white theme                                   |
| dark   | [Theme](#theme-object)                                             | Dark, colorful theme                                    |
| darkbg | [Theme](#theme-object) (if available)                              | Like `darkbg` with forced black background (Ncdu 1.17+) |


### Theme object

| key       | notes                                                                                                                                                                                             |
|-----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| default   | Used for most of the UI:<br/> - file names (unselected)<br/>- help pages                                                                                                                          |
| box_title | Used for windows titles:</br>- "ncdu help"</br>- "Item info"</br> - "Confirm delete"                                                                                                              |
| hd        | - Header base text<br/>- Footer base text</br>- Help page title (selected)                                                                                                                        |
| sel       | File row (selected)                                                                                                                                                                               |
| num       | Numbers only, without unit:<br/> - file size (unselected)</br>- size in percentage (unselected)</br>- child items count (unselected)</br>- disk usage (Item view)</br>- apparent size (Item view) |
| num_hd    | Numbers only, without unit (footer)                                                                                                                                                               |
| num_sel   | Numbers only, without unit:<br/> - file size (selected)</br>- size in percentage (selected)                                                                                                       |
| key       | Highlighted keys ("Item info", "ncdu help")                                                                                                                                                       |
| key_hd    | - "?" (header)</br>- "1", "2", "3" ("ncdu help"; selected)                                                                                                                                        |
| dir       | - File name (directories; unselected)<br/>- Current directory (under the header)                                                                                                                  |
| dir_sel   | File name (directories; selected)                                                                                                                                                                 |
| flag      | - File rows's leftmost character (unselected)<br/>- Flags ("ncdu help" -> "2:Format")                                                                                                             |
| flag_sel  | File rows's leftmost character (selected)                                                                                                                                                         |
| graph     | Graphical size percentage (unselected)                                                                                                                                                            |
| graph_sel | Graphical size percentage (selected)                                                                                                                                                              |

### Key object

| key | type                           | notes            |
|-----|--------------------------------|------------------|
| fg  | [Color](#color-object)         | Foreground color |
| bg  | [Color](#color-object)         | Background color |
| a   | [Attribute](#attribute-object) | Attribute flags  |


### Color object

#### 3-bit colors

Have a look [here](https://en.wikipedia.org/wiki/ANSI_escape_code#3-bit_and_4-bit) - the 3-bit colors are terminal-dependent.

| name    | bit value |
|---------|-----------|
| Black   | 0         |
| Red     | 1         |
| Green   | 2         |
| Yellow  | 3         |
| Blue    | 4         |
| Magenta | 5         |
| Cyan    | 6         |
| White   | 7         |


### Attribute object

| name       | bit value      | [notes](https://tldp.org/HOWTO/NCURSES-Programming-HOWTO/attrib.html) | does it work?            |
|------------|----------------|-----------------------------------------------------------------------|--------------------------|
| Standout   | 2<sup>16</sup> | Best highlighting mode of the terminal                                | yes                      |
| Underline  | 2<sup>17</sup> | Underlining                                                           | yes                      |
| Reverse    | 2<sup>18</sup> | Reverse video                                                         | yes                      |
| Blink      | 2<sup>19</sup> | Blinking                                                              | yes                      |
| Dim        | 2<sup>20</sup> | Half bright                                                           | yes                      |
| Bold       | 2<sup>21</sup> | Extra bright or bold                                                  | yes                      |
| Altcharset | 2<sup>22</sup> | Alternate character set                                               | theoretical support only |
| Invisible  | 2<sup>23</sup> | Invisible or blank mode                                               | yes                      |
| Protect    | 2<sup>24</sup> | Protected mode ("_selective erase_")                                  | theoretical support only |
| Horizontal | 2<sup>25</sup> |                                                                       | theoretical support only |
| Left       | 2<sup>26</sup> |                                                                       | theoretical support only |
| Low        | 2<sup>27</sup> |                                                                       | theoretical support only |
| Right      | 2<sup>28</sup> |                                                                       | theoretical support only |
| Top        | 2<sup>29</sup> |                                                                       | theoretical support only |
| Vertical   | 2<sup>30</sup> |                                                                       | theoretical support only |

Internally, the attributes are expressed as the sum of each single flag, stored in a 4-bit long unsigned integer.

When serialized as a string, the object is expressed as each attribute's name concatenated by the plus ('+') character.

A value of `null` resets all attributes.

> Note: some texts might appear to be dimmed, but since their attributes are hardencoded elsewhere, they can't be edited via NcduColors.

> Remember: not every terminal supports all the available attributes, and sometimes they might deliberately decide to ignore them (e.g. `Blink`), while others may support it but with different behavior.


## What has changed?

Using the [colordiff](https://command-not-found.com/colordiff) and [xxd](https://command-not-found.com/xxd) packages, you can compare your patched Ncdu binary with the old one.

```bash
export NC_LENGTH=360       # or 240, for older versions of Ncdu (pre-1.7)
export NC_THEMES_NUMBER=3  # or 2, for older versions of Ncdu (pre-1.7)
export NC_OFFSET=$(printf '0x%x' 123456)  # offset
export NC_BACKUP="/path/to/unpatched/ncdu"
export NC_CURRENT="$(command -v ncdu)"

colordiff -y \
  <(xxd -c $NC_THEMES_NUMBER -s $NC_OFFSET -l $NC_LENGTH $NC_BACKUP) \
  <(xxd -c $NC_THEMES_NUMBER -s $NC_OFFSET -l $NC_LENGTH $NC_CURRENT)
```

This will output a 15-rows long hex dump, wide 2 or 3 columns (in groups of 2x4 bytes).

![Colordiff used to compare two binary sequences](assets/images/colordiff.png "Ncdu 1.15.1 defaults compared to a custom theme")

<sup>_Example - Ncdu 1.15.1 defaults compared to a custom theme_</sup>


## Disclaimer

This software was created in just a couple of days of work.

It may contain bugs or could not work at all (in these cases, please open an issue).

Of course, don't expect any sort of legal warranty at all.


## Future improvements

- Add support for 4-bit and 8-bit colors.
- Add support for Big Endian binaries.
- Add support for Ncdu2 (the newer Zig version).
- Add tests


## License

[MIT License](LICENSE.txt).

This means you can use it everywhere, in both private and commercial contexts, for every possible purpose (you can even re-distribute it), as long as you preserve copyright and license notices.
