# Profit & Pricing Simulator

A free, single-file profit calculator for online businesses: profit per sale, CAC, LTV:CAC, break-evens, price sensitivity, cohort LTV and cash runway. Everything runs in the browser; there is no backend and nothing is uploaded.

Open `index.html` in a browser, or serve this folder with GitHub Pages (Settings → Pages → Deploy from a branch → this branch, `/ (root)`).

## Search engines

- **Bing, DuckDuckGo, Yahoo, Yandex:** the `Notify search engines` workflow submits the page through IndexNow after every change to `index.html` or `sitemap.xml`. The key file is `f8bdc82f197f06dc855b2f529aa37987.txt`; keep it in the repo root.
- **Google Search Console verification:** add a URL-prefix property for `https://mitchmoneyy.github.io/profit-pricing-simulator/`, choose the HTML tag method, then run the `Add search engine verification` workflow from the Actions tab and paste the tag. Also works for Bing Webmaster Tools tags.
