// Shared helpers for the calculator pages. Same formulas as the full simulator.
(function(){
  const PRESETS = {
    ecommerce:{model:'onetime',biz:'ecommerce',price:68,delivery:22,feePct:2.9,refund:6,visitors:42000,conv:2.1,ad:14000,fixed:9000,orders:1.8,churn:6,cash:60000,invBuy:25000,invMonth:3,elast:1.4,target:20000},
    saas:{model:'subscription',biz:'saas',price:79,delivery:9,feePct:2.9,refund:2,visitors:30000,conv:1.8,ad:16000,fixed:12000,orders:1,churn:4,cash:150000,invBuy:0,invMonth:1,elast:0.9,target:15000}
  };
  const BIZ = ['ecommerce','saas','course','agency','creator'];
  const NUM = ['price','delivery','feePct','refund','visitors','conv','ad','fixed','orders','churn','cash','invBuy','invMonth','elast','target'];
  function compute(s){
    const price = Math.max(0, +s.price || 0), r = Math.min(1, Math.max(0, (+s.refund || 0) / 100)), f = Math.max(0, (+s.feePct || 0) / 100);
    const fee = price * f + 0.30, contribution = price * (1 - r) - (+s.delivery || 0) - fee;
    const newCust = (+s.visitors || 0) * (+s.conv || 0) / 100;
    const ad = +s.ad || 0, fixed = +s.fixed || 0;
    const cac = s.cacDirect != null ? +s.cacDirect : (newCust > 0 ? ad / newCust : (ad > 0 ? Infinity : 0));
    const churn = Math.min(1, Math.max(0, (+s.churn || 0) / 100));
    const life = s.model === 'subscription' ? (churn > 0 ? Math.min(1 / churn, 60) : 60) : null;
    const ltv = s.model === 'subscription' ? contribution * life : contribution * Math.max(1, +s.orders || 1);
    return {price, r, f, fee, contribution, newCust, cac, pps: contribution - cac, monthly: newCust * contribution - ad - fixed,
      margin: price > 0 ? contribution / price * 100 : 0, life, ltv, ratio: cac > 0 && isFinite(cac) ? ltv / cac : (cac === 0 && ltv > 0 ? Infinity : 0),
      beSales: contribution > 0 ? (ad + fixed) / contribution : Infinity,
      bePrice: newCust > 0 && 1 - r - f > 0 ? ((ad + fixed) / newCust + (+s.delivery || 0) + 0.30) / (1 - r - f) : Infinity};
  }
  const M = '−';
  const money = (v, dp) => { if (!isFinite(v)) return v > 0 ? '∞' : '—'; const a = Math.abs(v); if (dp == null) dp = a >= 1000 ? 0 : 2; return (v < 0 ? M : '') + '$' + a.toLocaleString('en-US', {minimumFractionDigits: dp, maximumFractionDigits: dp}); };
  const num = (v, dp = 0) => isFinite(v) ? (v < 0 ? M : '') + Math.abs(v).toLocaleString('en-US', {minimumFractionDigits: dp, maximumFractionDigits: dp}) : '—';
  const pct = (v, dp = 1) => isFinite(v) ? (v < 0 ? M : '') + Math.abs(v).toFixed(dp) + '%' : '—';
  const x = v => v === Infinity ? '∞' : isFinite(v) ? v.toFixed(v >= 10 ? 0 : 1) + '×' : '—';
  function encode(s){
    const arr = [1, s.model === 'subscription' ? 1 : 0, Math.max(0, BIZ.indexOf(s.biz))].concat(NUM.map(k => +(+s[k]).toFixed(4)));
    return btoa(JSON.stringify(arr)).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
  }
  function read(){
    const o = {};
    document.querySelectorAll('[data-k]').forEach(el => { o[el.dataset.k] = el.tagName === 'SELECT' ? el.value : parseFloat(el.value); if (el.tagName !== 'SELECT' && !isFinite(o[el.dataset.k])) o[el.dataset.k] = 0; });
    return o;
  }
  window.Calc = {compute, money, num, pct, x, encode, read, PRESETS,
    start(update, base){
      const run = () => {
        const inp = read(), res = update(inp);
        const full = Object.assign({}, PRESETS[base || 'ecommerce'], inp, res && res.state || {});
        delete full.cacDirect;
        const link = document.getElementById('openFull');
        if (link) link.href = '../#s=' + encode(full);
      };
      document.querySelectorAll('[data-k]').forEach(el => el.addEventListener('input', run));
      run();
    }};
  try { const t = localStorage.getItem('pps.theme'); if (t) document.documentElement.setAttribute('data-theme', t); } catch(e){}
})();
