# Gene Regulatory Evolution Lab (PI: Bin He) website

This website is based on <http://bedford.io> ([GitHub repo](https://github.com/blab/blotter)) with modifications made by [Rasi Subramanium](http://rasilab.org). I further customized the site by incorporating elements from the [hugo-academic theme](https://themes.gohugo.io/academic/).

## Setup the system (Mac OS)
- Ruby version is specified in the `.ruby-version` file and the gems versions in the `Gemfile.lock`.
- Don't use the system ruby. I used to use `rbenv` to manage different ruby versions. Here 
## Build site

To build the website locally, clone the repo with:

```
git clone https://github.com/binhe-lab/binhe-lab-pub.git
```

Then install necessary Ruby dependencies by running `bundle install` from within the `binhe-lab` directory.  After this, the site can be be built with:

```
bundle exec jekyll build
```

To view the site, run `bundle exec jekyll serve` and point a browser to `http://localhost:4000/`.  More information on Jekyll can be found [here](http://jekyllrb.com/).

For more information on the design of this site, see Trevor Bedford's [original repo](https://github.com/blab/blotter)
## License

Below is the original license information from [](bedford.io). This site assumes the same MIT license as the original template.

> All source code in this repository, consisting of files with extensions `.html`, `.css`, `.less`, `.rb` or `.js`, is freely available under an MIT license, unless otherwise noted within a file. You're welcome to borrow / repurpose code to build your own site, but I would very much appreciate attribution and a link back to [bedford.io](http://bedford.io) from your `about` page.

**The MIT License (MIT)**

Copyright (c) 2013-2015 Trevor Bedford

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
