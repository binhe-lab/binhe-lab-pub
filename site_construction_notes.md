---
title: notes of my modification to the website as inherited from Rasi
author: Bin He
date: 23 oct 2017
---

This is not a complete list of notes. I didn't start taking notes until quite late in the process. The early edits are mainly on the styling of the site, including changing the navbar elements and using inverse colors, etc.

## [26 nov 2017] Clean up the CSS

- went through the css `style.less` file and moved stuff to a file named `not-in-use`, while watching the Jekyll generator's error report (`bundle exec jekyll serve` run in a separate window).

## [25 nov 2017] Adjust footer

### Goal

Add a footer to contain "about this site" and social contact information (email etc.)

### Notes

- Followed [bootstrap tutorial](https://v4-alpha.getbootstrap.com/examples/sticky-footer-navbar/) to create a sticky footer using the following code

    ```html
    <footer class="footer">
    <div class="container">
    <span class="text-muted">Place sticky footer content here.</span>
    </div>
    </footer>
    ```

    And the css code

    ```css
    <footer class="footer">
    <div class="container">
    <span class="text-muted">Place sticky footer content here.</span>
    </div>
    </footer>
    ```

## [24 nov 2017] Change homepage and other style changes

- After several attempts, and taking advice from tuzi, I settled on a version largely based on the Hugo-Academic profile, except the personal experiences are removed.
- I changed the `container` class to increase the padding on both sides, which effectively sets the margin. Before that, Rasi's implementation uses small padding (25), coupled with `col-md-` settings to adjust the width of the content.
- After changing the padding, I found the auto-collapse of the navbar encountered some problem. In particular, when the screen size is small, the padding used for the full desktop screen is obviously not suitable. So defined the corresponding `container` class under the two resolution-responsive css set.

## [22 nov 2017] plan on changing the homepage

Tuzi suggestion: make the homepage about the lab, not myself. Make it forward looking. Plan to use Bedford's Team template. Change the homepage to a paragraph accompanying a cartoon.
## [12 nov 2017] duplicate the respoitory to clear way for making the lab website public

_Goal_

- Because the initial repo was forked from Rasi's, which means it contains not only all information in Rasi's private repo, but also all the commit record. I decide that it is not a good idea to make this repo public by duplicating the whole repo. Instead, I want to leave a private repo in my own account, preserving the initial commit history, i.e. my modification to the website based on Rasi's and Bedford.io's design. Once I'm reasonably confident that the repo no longer contains any of Rasi's information, I'll make a "bare clone" and push it to a public repo on binhe-lab organization account page, and then use Netlify to publish that.

_Notes_

1. I followed the [instruction here](https://help.github.com/articles/duplicating-a-repository/) and made a (private) duplicate of `binhe-lab.git` in my own GitHub account.
1. I then repointed my local working copy's remote to the new repo.

    ```bash
    $git remote -v
    origin  https://github.com/hezhaobin/binhe-lab.git (fetch)
    origin  https://github.com/hezhaobin/binhe-lab.git (push)
    ```

## [2 nov 2017] move to GitHub for deployment

I want to...

1. Clean up the repo to remove potentially confidential information related to rasilab.
1. Make a bare clone of the repo, remove the history, and commit to a **public** GitHub repo.
1. Test upgrading the jekyll version to the current one, switching to Kramdown instead of Red Carpet.

## [29 oct 2017] about

modified the navbar menus -- replaced "Code" with "About". Changed the `_layout/misc.html`, which is used for `/about/index.html`. Wrote a simple description of how this website came about.

## [27 oct 2017] fonts & papers

- I tried to copy over Hugo-Academics fonts -- the latest version of the theme stores the fonts setting in a separate `fonts` folder, which contains three themes. The default is now sans-serif for both heading and body. I stick to the "Merriweather" for body and "Lato" for heading.
- Also modified the papers template, and added the pdf and github link for He-eLife-2017

## [24 oct 2017] navbar & selected-publications

_Goal_

- Make the navbar collapse earlier (at wider screen size)
- Separate the publications into selected and all categories

_Reference_

https://stackoverflow.com/questions/21076922/bootstrap-how-to-collapse-navbar-earlier

_Notes_

- added the following snippets to `css/style.less`. also reorganized the file by moving the navbar and profile related elements above the "other" section
- adjusted `navbar-brand-centered` section, which is used to position the "navbar-brand-text" at smaller screen size.
- also got "selected-papers" to work
    1. each post in `papers/_post/` get the default category "papers"
    1. by adding a `category: selected-papers` into the YAML header of my selected papers, I can override the default and thus display these in a front section, by looping over this newly created category.

## [23 oct 2017] papers

- adjust css, blend in bedford.io design

## [20 oct 2017] academicons

- I basically hacked the "about.md" section from hugo-academic theme to the Jekyll site. However, I couldn't get Academicons to work (for Google-Scholar)

- tried to mess with style.css and index.md, no luck

- got it to work by adding the following to `_layout/default.html`

    ```css
    <!-- Academicons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/academicons/1.8.1/css/academicons.min.css" media="screen"/>
    ```

- changed `<i class="fa fa-twitter big-icon"></i>` to `<i class="fa fa-twitter fa-2x"></i>` because `Academicons 1.8.1` appears to not support the `big-icon` property. `2x` is exactly the same in size
