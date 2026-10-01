# Gradfolio

responsive, dark-mode ready Jekyll theme designed for use as a personal website and portfolio. [Here's a live demo](https://jitinnair1.github.io/gradfolio/)

![Gradfolio Template Homepage](https://user-images.githubusercontent.com/2485715/110634179-acaa7e00-81cf-11eb-8846-062ecf961d1e.png)

## Develop

Open the folder in the dev container (VS Code: *Reopen in Container*); it runs
`bundle install` for you. Otherwise, with Ruby 3.3:

```bash
bundle install
bundle exec jekyll serve --livereload
```

## Deploy

`.github/workflows/pages.yml` builds the site with Jekyll 4 and deploys it to
GitHub Pages on every push to `master`, every Monday, and on demand from the
Actions tab. In the repository settings, *Pages → Build and deployment →
Source* must be set to **GitHub Actions**.

## Publications

The publications page is generated from `_data/scholar.json`, scraped from the
Google Scholar profile set by `scholar:` in `_config.yml`. Each deploy refreshes
it first and commits any changes; if Scholar blocks the request, the committed
copy is used. To refresh locally:

```bash
python3 scripts/fetch_scholar.py
```

## Features
- Responsive
- Respects Dark Mode preference set by user
- Projects Page to showcase your work/side projects
- Easily link to your profiles on ResearchGate and ORCID

## Installation
* Click on `Use this template`
* Your new site should be ready at https://username.github.io/gradfolio/
* You can now modify the contents and personalise the template

Alternatively, you can [download the source files](https://github.com/jitinnair1/gradfolio/archive/master.zip) and make changes locally.

To test these changes, open a terminal inside the source folder and use `jekyll serve --incremental --trace` to make it available on a local server (typically http://localhost:4000/)

The `--incremental` flag ensures that any changes you make are reflected in your browser in real time and the `--trace` option might be useful for debugging if things break while you are changing the source files.

Once you have personalised and tested the site, you can create a new repo, upload these files and host your website from the repo.

## Based on
- [hagura](https://github.com/sharu725/hagura)
- [al-folio](https://github.com/alshedivat/al-folio)
- [noir](https://github.com/essentialenemy/noir)
- [jekyll-TeXt-theme](https://github.com/kitian616/jekyll-TeXt-theme)
- [LatexJekyll](https://github.com/Hammie217/LatexJekyll) (typography and Computer Modern fonts)

## License
MIT License

[![JekyllThemes](https://img.shields.io/badge/featured%20on-JekyllThemes-red.svg)](https://jekyll-themes.com)
