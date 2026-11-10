"""Builds the calculator pages (one folder per page) and the sitemap.

Run from the repo root:  python3 tools/build_pages.py
"""
import json
import os
from html import escape

SITE = 'https://mitchmoneyy.github.io/profit-pricing-simulator/'
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600&family=DM+Serif+Display&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">')


def field(label, key, value, pre='', suf='', step='any'):
    return (f'<label class="f"><span>{label}</span><span class="in">{f"<span class=u>{pre}</span>" if pre else ""}'
            f'<input type="number" inputmode="decimal" data-k="{key}" id="k-{key}" value="{value}" step="{step}" min="0">'
            f'{f"<span class=u>{suf}</span>" if suf else ""}</span></label>')


def out(label, oid, main=False):
    return f'<div class="o{" main" if main else ""}"><div class="l">{label}</div><div class="v" id="{oid}">—</div></div>'


PAGES = []


def page(slug, title, h1, desc, lead, fields, outs, script, body, faqs, base='ecommerce', cta='Open in the full simulator'):
    PAGES.append(dict(slug=slug, title=title, h1=h1, desc=desc, lead=lead, fields=fields, outs=outs,
                      script=script, body=body, faqs=faqs, base=base, cta=cta))


# 1. Break-even calculator ------------------------------------------------------
page('break-even-calculator',
     'Break-Even Calculator for Online Businesses',
     'Break-even calculator for online businesses',
     'Work out how many sales, what price and what conversion rate you need to break even each month, after refunds, payment fees, delivery costs and ad spend.',
     'How many sales do you need each month to cover ad spend and fixed costs? What price gets you there with the customers you have today? Enter your numbers.',
     [field('Price per sale', 'price', 68, '$'), field('Delivery cost per sale', 'delivery', 22, '$'),
      field('Payment fee', 'feePct', 2.9, '', '%'), field('Refund rate', 'refund', 6, '', '%'),
      field('Monthly visitors', 'visitors', 42000, step='1'), field('Conversion rate', 'conv', 2.1, '', '%'),
      field('Monthly ad spend', 'ad', 14000, '$'), field('Monthly fixed costs', 'fixed', 9000, '$')],
     [out('Sales needed per month', 'oSales', True), out('You make now', 'oNow'), out('Break-even price', 'oPrice'),
      out('Break-even conversion', 'oConv'), out('Monthly profit today', 'oProfit')],
     """Calc.start(s => { s.model = 'onetime'; const m = Calc.compute(s);
  oSales.textContent = Calc.num(Math.ceil(m.beSales)); oNow.textContent = Calc.num(m.newCust) + ' sales';
  oPrice.textContent = Calc.money(m.bePrice); oConv.textContent = isFinite(m.beSales) && s.visitors > 0 ? Calc.pct(m.beSales / s.visitors * 100, 2) : '—';
  oProfit.textContent = Calc.money(m.monthly, 0); });""",
     """<h2>How the break-even point is calculated</h2>
<p>Each sale contributes what's left after refunds, delivery and payment fees. Break-even is the number of sales whose combined contribution covers your monthly ad spend and fixed costs.</p>
<div class="formula">Fee per sale = price × fee% + $0.30<br>Contribution per sale = price × (1 − refund rate) − delivery cost − fee<br>Break-even sales = (ad spend + fixed costs) ÷ contribution per sale<br>Break-even conversion = break-even sales ÷ monthly visitors</div>
<h2>Worked example</h2>
<p>An online store sells at $68 with $22 of product and shipping cost, a 2.9% + $0.30 card fee and 6% refunds. Each sale contributes $68 × 0.94 − $22 − $2.27 = <strong>$39.65</strong>. With $14,000 of ads and $9,000 of fixed costs, it needs $23,000 ÷ $39.65 = <strong>581 sales</strong> a month to break even. At 42,000 visitors that's a 1.38% conversion rate, so at 2.1% the store clears break-even comfortably.</p>
<h2>Three ways to lower your break-even point</h2>
<h3>Raise contribution per sale</h3><p>A price rise, a cheaper supplier or fewer refunds all lower the number of sales you need. Contribution is the denominator, so small changes move break-even a lot when margins are thin.</p>
<h3>Cut fixed costs</h3><p>Software, salaries and rent are paid whether you sell or not. Every $1,000 of monthly fixed cost removed lowers break-even by $1,000 ÷ contribution sales.</p>
<h3>Spend ad money more efficiently</h3><p>Ad spend sits in the numerator. If the same customers can be won for less, break-even drops without touching price.</p>""",
     [('What is a break-even point?', 'The level of sales at which revenue after variable costs exactly covers fixed costs and ad spend, so monthly profit is zero. Above it you make money; below it you lose money.'),
      ('Should ad spend count as a fixed cost?', 'For a monthly break-even, yes: it is a budget you commit to each month. The full simulator also shows break-even per sale, where ad spend becomes customer acquisition cost.'),
      ('Why is the $0.30 fee included?', 'Most card processors charge a percentage plus a fixed amount per transaction, commonly 2.9% + $0.30. On low prices the fixed part is a large share of the sale.'),
      ('How is break-even price different from break-even sales?', 'Break-even sales holds your price fixed and asks how many customers you need. Break-even price holds your customer count fixed and asks what price makes the month profitable.')])

# 2. LTV:CAC calculator ---------------------------------------------------------
page('ltv-cac-calculator',
     'LTV:CAC Calculator – Customer Lifetime Value vs Acquisition Cost',
     'LTV:CAC ratio calculator',
     'Calculate customer lifetime value, customer acquisition cost and the LTV:CAC ratio for one-time purchase or subscription businesses, with payback time.',
     'Is each customer worth more than it costs to win them? Enter your numbers to get lifetime value, acquisition cost, the ratio between them and how long payback takes.',
     ['<label class="f"><span>Revenue model</span><span class="in"><select data-k="model" id="k-model"><option value="onetime">One-time</option><option value="subscription">Subscription</option></select></span></label>',
      field('Price per sale or month', 'price', 68, '$'), field('Delivery cost per sale', 'delivery', 22, '$'),
      field('Payment fee', 'feePct', 2.9, '', '%'), field('Refund rate', 'refund', 6, '', '%'),
      field('Orders per customer', 'orders', 1.8, '', '×'), field('Monthly churn', 'churn', 5, '', '%'),
      field('Monthly ad spend', 'ad', 14000, '$'), field('New customers per month', 'cust', 882, step='1')],
     [out('LTV:CAC', 'oRatio', True), out('Lifetime value (LTV)', 'oLtv'), out('Acquisition cost (CAC)', 'oCac'),
      out('Payback', 'oPay'), out('Verdict', 'oVerdict')],
     """Calc.start(s => { const sub = s.model === 'subscription';
  document.getElementById('k-orders').closest('.f').style.opacity = sub ? .4 : 1; document.getElementById('k-churn').closest('.f').style.opacity = sub ? 1 : .4;
  s.cacDirect = s.cust > 0 ? s.ad / s.cust : Infinity; const m = Calc.compute(s);
  oRatio.textContent = Calc.x(m.ratio); oLtv.textContent = Calc.money(m.ltv); oCac.textContent = Calc.money(m.cac);
  const pay = m.contribution > 0 ? m.cac / m.contribution : Infinity;
  oPay.textContent = isFinite(pay) ? (pay <= 1 ? 'First ' + (sub ? 'month' : 'order') : Calc.num(pay, 1) + (sub ? ' months' : ' orders')) : 'Never';
  oVerdict.textContent = m.ratio < 1 ? 'Losing money per customer' : m.ratio < 3 ? 'Below the 3× rule of thumb' : m.ratio <= 6 ? 'Healthy' : 'Room to spend more on growth';
  return {state: {visitors: 42000, conv: s.cust / 420}}; });""",
     """<h2>How LTV and CAC are calculated</h2>
<div class="formula">Contribution per sale = price × (1 − refund rate) − delivery cost − (price × fee% + $0.30)<br>LTV (one-time) = contribution × orders per customer<br>LTV (subscription) = contribution × 1 ÷ monthly churn, capped at 60 months<br>CAC = monthly ad spend ÷ new customers per month<br>LTV:CAC = LTV ÷ CAC</div>
<p>LTV here is based on contribution, not revenue. Revenue-based LTV flatters the ratio because it ignores what each sale costs you to deliver.</p>
<h2>What is a good LTV:CAC ratio?</h2>
<div class="tw"><table><tr><th>Ratio</th><th>What it means</th></tr>
<tr><td class="n">Below 1×</td><td>Each customer loses money over their lifetime. Growth makes it worse.</td></tr>
<tr><td class="n">1–3×</td><td>Profitable on paper, with little room for rising ad costs or refunds.</td></tr>
<tr><td class="n">3–5×</td><td>The usual target. Acquisition pays for itself with margin to spare.</td></tr>
<tr><td class="n">Above 5×</td><td>Often a sign you could spend more to grow faster.</td></tr></table></div>
<h2>Worked example</h2>
<p>A subscription at $79 a month with $9 of delivery cost, 2.9% + $0.30 fees and 2% refunds contributes about $66 a month. At 4% monthly churn, customers stay 25 months on average, so LTV is about $1,646. If $16,000 of ads wins 540 customers, CAC is $29.63 and LTV:CAC is about 56×, a strong signal to spend more on acquisition.</p>""",
     [('Should LTV use revenue or profit?', 'Profit, specifically contribution after refunds, delivery and fees. Using revenue overstates lifetime value, sometimes by several times for physical products.'),
      ('Why cap subscription lifetime at 60 months?', 'Very low churn gives unrealistic lifetimes (0.5% churn implies 16 years). Capping at five years keeps the estimate conservative.'),
      ('What is payback period?', 'How many orders or months of contribution it takes to earn back what you spent to acquire the customer. Shorter payback means growth needs less cash.'),
      ('How do I improve LTV:CAC?', 'Raise contribution per sale (price, delivery cost, refunds), increase repeat orders or reduce churn, or lower CAC by improving conversion on the traffic you already pay for.')])

# 3. Profit per sale / margin calculator ----------------------------------------
page('profit-margin-calculator',
     'Profit Per Sale & Contribution Margin Calculator',
     'Profit per sale and margin calculator',
     'See exactly how much you keep from each sale after refunds, delivery costs, payment fees and the cost to acquire the customer. Contribution margin and profit per sale.',
     'Gross margin hides the costs that eat online businesses: refunds, card fees and ads. Enter a sale to see what you actually keep.',
     [field('Price per sale', 'price', 68, '$'), field('Delivery cost (COGS, shipping)', 'delivery', 22, '$'),
      field('Payment fee', 'feePct', 2.9, '', '%'), field('Refund rate', 'refund', 6, '', '%'),
      field('Cost to acquire a customer', 'cacDirect', 15.87, '$')],
     [out('Profit per sale', 'oPps', True), out('Contribution per sale', 'oContrib'), out('Contribution margin', 'oMargin'),
      out('Payment fee per sale', 'oFee'), out('Refund cost per sale', 'oRef')],
     """Calc.start(s => { s.model = 'onetime'; const m = Calc.compute(s);
  oPps.textContent = Calc.money(m.pps); oContrib.textContent = Calc.money(m.contribution); oMargin.textContent = Calc.pct(m.margin);
  oFee.textContent = Calc.money(m.fee); oRef.textContent = Calc.money(s.price * m.r);
  return {state: {ad: s.cacDirect * 882, visitors: 42000, conv: 2.1}}; });""",
     """<h2>The formula</h2>
<div class="formula">Fee per sale = price × fee% + $0.30<br>Refund cost = price × refund rate<br>Contribution = price − refund cost − delivery cost − fee<br>Contribution margin = contribution ÷ price<br>Profit per sale = contribution − customer acquisition cost</div>
<h2>Gross margin vs contribution margin vs profit per sale</h2>
<div class="tw"><table><tr><th>Measure</th><th>Subtracts</th><th>Example ($68 sale)</th></tr>
<tr><td>Gross margin</td><td>Product and delivery cost</td><td class="n">$46.00 (68%)</td></tr>
<tr><td>Contribution margin</td><td>+ refunds and payment fees</td><td class="n">$39.65 (58%)</td></tr>
<tr><td>Profit per sale</td><td>+ cost to acquire the customer</td><td class="n">$23.78 (35%)</td></tr></table></div>
<p>The gap between the first and last line is why stores with healthy-looking gross margins can still lose money: refunds, fees and ads are paid on every order.</p>
<h2>Typical contribution margins by business model</h2>
<p>Rough ranges for an average business: e-commerce around 35%, agencies around 35%, creators and memberships around 65%, SaaS around 70%, online courses around 75%. Top performers run 15–20 points higher.</p>""",
     [('What is a good profit margin for an online store?', 'It depends on the category, but a contribution margin of 40–55% before ads gives most stores enough room to pay for acquisition and still profit on the first order.'),
      ('Do I include shipping in delivery cost?', 'Include whatever you pay to fulfil an order: product cost, packaging, shipping you pay for, and per-order platform or app fees.'),
      ('Is profit per sale negative a problem?', 'Not always. If customers buy again or subscribe, lifetime value can cover the loss on the first order. Use the LTV:CAC calculator to check.'),
      ('Where do I find my customer acquisition cost?', 'Divide last month\'s ad spend by the number of new customers it brought in. Many ad dashboards show this as cost per purchase or cost per acquisition.')])

# 4. Pricing calculator ---------------------------------------------------------
page('pricing-calculator',
     'Pricing Calculator – Find Your Profit-Maximising Price',
     'Pricing calculator: find the price that maximises profit',
     'Find the price that maximises monthly profit, accounting for the conversions you lose when you raise prices. Uses price elasticity, refunds, fees and ad spend.',
     'Raising prices loses some buyers. Lowering them wins some back. This calculator finds the price where monthly profit peaks, using a price elasticity you can adjust.',
     [field('Current price', 'price', 68, '$'), field('Delivery cost per sale', 'delivery', 22, '$'),
      field('Payment fee', 'feePct', 2.9, '', '%'), field('Refund rate', 'refund', 6, '', '%'),
      field('Monthly visitors', 'visitors', 42000, step='1'), field('Conversion rate', 'conv', 2.1, '', '%'),
      field('Monthly ad spend', 'ad', 14000, '$'), field('Monthly fixed costs', 'fixed', 9000, '$'),
      field('Price elasticity', 'elast', 1.4, '', 'e', '0.1')],
     [out('Profit-maximising price', 'oBest', True), out('Monthly profit at that price', 'oBestP'), out('Monthly profit today', 'oNowP'),
      out('Conversion at best price', 'oBestC')],
     """Calc.start(s => { s.model = 'onetime'; const p0 = s.price || 1; let best = null, rows = [];
  for (let i = 0; i <= 360; i++){ const p = p0 * (0.4 + i * 0.005), cv = Math.min(100, s.conv * Math.pow(p / p0, -s.elast));
    const m = Calc.compute(Object.assign({}, s, {price: p, conv: cv})); if (!best || m.monthly > best.y) best = {p, y: m.monthly, cv}; }
  const now = Calc.compute(s);
  oBest.textContent = Calc.money(best.p); oBestP.textContent = Calc.money(best.y, 0); oNowP.textContent = Calc.money(now.monthly, 0); oBestC.textContent = Calc.pct(best.cv, 2);
  const tb = document.getElementById('ptable'); tb.innerHTML = [0.8, 0.9, 1, 1.1, 1.25, 1.5].map(k => { const p = p0 * k, cv = Math.min(100, s.conv * Math.pow(k, -s.elast)), m = Calc.compute(Object.assign({}, s, {price: p, conv: cv}));
    return `<tr><td class="n">${Calc.money(p)}</td><td class="n">${Calc.pct(cv, 2)}</td><td class="n">${Calc.num(m.newCust)}</td><td class="n">${Calc.money(m.monthly, 0)}</td></tr>`; }).join(''); });""",
     """<h2>Your prices compared</h2>
<div class="tw"><table><thead><tr><th>Price</th><th>Conversion</th><th>Sales / month</th><th>Monthly profit</th></tr></thead><tbody id="ptable"></tbody></table></div>
<h2>What price elasticity means</h2>
<p>Elasticity describes how strongly conversion reacts to price. At an elasticity of 1.0, a 10% price rise loses about 10% of conversions. Below 1, customers barely notice price changes, which is typical of niche tools, B2B software and trusted brands. Above 1.5, buyers compare prices closely, as with commodity products and impulse buys.</p>
<div class="formula">Conversion at new price = current conversion × (new price ÷ current price) ^ −elasticity<br>Monthly profit = new customers × contribution − ad spend − fixed costs</div>
<h2>How to estimate your elasticity</h2>
<p>The best estimate comes from your own history: compare conversion before and after a past price change, holding traffic quality steady. Without data, start at 1.0 for most consumer products and 0.6–0.8 for B2B or specialist products, then test a price change on new visitors and update the number.</p>
<h2>Why the best price is often higher than you think</h2>
<p>Every sale carries fixed costs: delivery, the $0.30 fee and the ad spend that brought the buyer in. A higher price spreads those over fewer, more profitable sales. Unless your market is very price-sensitive, the profit-maximising price usually sits above where founders start.</p>""",
     [('Is the profit-maximising price the right price?', 'It is the price that maximises this month\'s profit under your elasticity estimate. You may choose a lower price to grow faster or win market share; the calculator shows what that choice costs.'),
      ('Does raising prices increase refunds?', 'It can. If you expect higher refunds at a higher price, raise the refund rate when testing that price.'),
      ('What if I sell a subscription?', 'The same logic applies to the monthly price. In the full simulator, switch to the subscription model to also see how churn changes lifetime value.'),
      ('How accurate is this?', 'As accurate as the elasticity estimate. Treat the result as a direction and a size of opportunity, then confirm it with a real price test.')])

# 5. SaaS churn / LTV calculator ------------------------------------------------
page('saas-churn-ltv-calculator',
     'SaaS LTV & Churn Calculator – Customer Lifetime and Payback',
     'SaaS churn and LTV calculator',
     'Calculate SaaS customer lifetime value from monthly churn, see average customer lifetime, CAC payback months and how many customers remain after 12 months.',
     'Monthly churn decides how long customers stay and what they are worth. Enter your plan price, costs and churn to see lifetime value, payback and retention.',
     [field('Monthly plan price', 'price', 79, '$'), field('Cost to serve per month', 'delivery', 9, '$'),
      field('Payment fee', 'feePct', 2.9, '', '%'), field('Refund rate', 'refund', 2, '', '%'),
      field('Monthly churn', 'churn', 4, '', '%'), field('Customer acquisition cost', 'cacDirect', 29.63, '$')],
     [out('Lifetime value (LTV)', 'oLtv', True), out('Average customer lifetime', 'oLife'), out('LTV:CAC', 'oRatio'),
      out('CAC payback', 'oPay'), out('Still subscribed after 12 months', 'oRet')],
     """Calc.start(s => { s.model = 'subscription'; const m = Calc.compute(s), c = s.churn / 100;
  oLtv.textContent = Calc.money(m.ltv); oLife.textContent = Calc.num(m.life, 1) + ' months'; oRatio.textContent = Calc.x(m.ratio);
  let pay = null, tot = 0; for (let k = 0; k < 120; k++){ tot += m.contribution * Math.pow(1 - c, k); if (tot >= m.cac){ pay = k + 1; break; } }
  oPay.textContent = pay ? 'Month ' + pay : 'More than 10 years'; oRet.textContent = Calc.pct(Math.pow(1 - c, 12) * 100, 0);
  return {state: {ad: s.cacDirect * 540, visitors: 30000, conv: 1.8}}; }, 'saas');""",
     """<h2>The formulas</h2>
<div class="formula">Contribution per month = price × (1 − refund rate) − cost to serve − (price × fee% + $0.30)<br>Average lifetime (months) = 1 ÷ monthly churn, capped at 60<br>LTV = contribution per month × average lifetime<br>Retention after n months = (1 − monthly churn) ^ n</div>
<h2>How churn compounds</h2>
<div class="tw"><table><tr><th>Monthly churn</th><th>Average lifetime</th><th>Left after 12 months</th></tr>
<tr><td class="n">1.5%</td><td class="n">67 months (capped at 60)</td><td class="n">83%</td></tr>
<tr><td class="n">3%</td><td class="n">33 months</td><td class="n">69%</td></tr>
<tr><td class="n">5%</td><td class="n">20 months</td><td class="n">54%</td></tr>
<tr><td class="n">8%</td><td class="n">12.5 months</td><td class="n">37%</td></tr></table></div>
<p>Halving churn doubles lifetime value. For most subscription businesses that is worth more than any price change.</p>
<h2>Typical monthly churn</h2>
<p>Rough tiers for small and mid-sized SaaS: around 5% a month is average, 3% is top-quartile and 1.5% or less is top-10%. Memberships and creator subscriptions usually run higher, around 6–9%.</p>""",
     [('What is a good churn rate for SaaS?', 'For small-business SaaS, 3–5% monthly is common and under 2% is excellent. Enterprise products often see well under 1% monthly.'),
      ('Why does LTV use contribution instead of revenue?', 'Hosting, support and payment fees are paid every month the customer stays. Revenue-based LTV ignores them and overstates what a customer is worth.'),
      ('What is CAC payback?', 'The month in which a customer\'s cumulative contribution, after churn, first exceeds what you paid to acquire them. Under 12 months is a common target.'),
      ('Is monthly or annual churn better to track?', 'Track monthly for decisions, since it reacts faster. Annual retention equals (1 − monthly churn)^12.')],
     base='saas')

NAV_ORDER = [p['slug'] for p in PAGES]
NAMES = {
    'break-even-calculator': 'Break-even calculator',
    'ltv-cac-calculator': 'LTV:CAC calculator',
    'profit-margin-calculator': 'Profit margin calculator',
    'pricing-calculator': 'Pricing calculator',
    'saas-churn-ltv-calculator': 'SaaS churn & LTV calculator',
}


def render(p):
    url = SITE + p['slug'] + '/'
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p['faqs']]}
    app_ld = {"@context": "https://schema.org", "@type": "WebApplication", "name": p['h1'][0].upper() + p['h1'][1:], "url": url,
              "applicationCategory": "BusinessApplication", "operatingSystem": "Any (web browser)", "isAccessibleForFree": True,
              "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}
    crumbs_ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Profit & Pricing Simulator", "item": SITE},
        {"@type": "ListItem", "position": 2, "name": NAMES[p['slug']], "item": url}]}
    related = ''.join(f'<a href="../{s}/">{NAMES[s]}</a>' for s in NAV_ORDER if s != p['slug'])
    faqs = ''.join(f'<details><summary>{escape(q)}</summary><p>{escape(a)}</p></details>' for q, a in p['faqs'])
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{escape(p['title'])} | Free</title>
<meta name="description" content="{escape(p['desc'])}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0a0a0a">
<meta property="og:type" content="website"><meta property="og:url" content="{url}">
<meta property="og:title" content="{escape(p['title'])}"><meta property="og:description" content="{escape(p['desc'])}">
<meta property="og:image" content="{SITE}og-image.png"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{SITE}og-image.png">
<link rel="icon" href="../icon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="../apple-touch-icon.png"><link rel="manifest" href="../manifest.webmanifest">
{FONTS}
<link rel="stylesheet" href="../assets/pages.css">
<script type="application/ld+json">{json.dumps(app_ld)}</script>
<script type="application/ld+json">{json.dumps(faq_ld)}</script>
<script type="application/ld+json">{json.dumps(crumbs_ld)}</script>
</head>
<body>
<header><div class="wrap"><a class="brand" href="../"><span class="mark">%</span>Profit &amp; Pricing</a><a class="btn" href="../#app">Full simulator</a></div></header>
<main class="wrap">
<div class="crumb"><a href="../">Profit &amp; Pricing Simulator</a> / {NAMES[p['slug']]}</div>
<h1>{escape(p['h1'][0].upper() + p['h1'][1:])}</h1>
<p class="lead">{p['lead']}</p>
<section class="calc" aria-label="Calculator">
<div class="fields">{''.join(p['fields'])}</div>
<div class="out" aria-live="polite">{''.join(p['outs'])}<a class="btn" id="openFull" href="../#app">{p['cta']}</a><p class="note">Free, no sign-up. Results stay in your browser.</p></div>
</section>
{p['body']}
<h2>Frequently asked questions</h2>
{faqs}
<section class="cta"><h2>See the whole picture</h2><p>The full simulator adds a health score, five ranked levers, benchmarks, cohort LTV, cash runway and monthly history. Import a dashboard screenshot to fill it in.</p><a class="btn" href="../#app">Open the simulator</a></section>
<h2>More calculators</h2>
<div class="related">{related}</div>
</main>
<footer><div class="wrap">Profit &amp; Pricing Simulator · Fee per sale = price × fee% + $0.30 · All calculations run in your browser.</div></footer>
<script src="../assets/pages.js"></script>
<script>{p['script']}</script>
</body>
</html>
'''


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for p in PAGES:
        d = os.path.join(root, p['slug'])
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, 'index.html'), 'w') as f:
            f.write(render(p))
    urls = [SITE] + [SITE + s + '/' for s in NAV_ORDER]
    with open(os.path.join(root, 'sitemap.xml'), 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for u in urls:
            f.write(f'  <url><loc>{u}</loc></url>\n')
        f.write('</urlset>\n')
    with open(os.path.join(root, 'tools', 'urls.txt'), 'w') as f:
        f.write('\n'.join(urls) + '\n')
    print('built', len(PAGES), 'pages')


if __name__ == '__main__':
    main()
