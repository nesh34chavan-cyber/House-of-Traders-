(() => {
  const API =
    new URLSearchParams(location.search).get("api") ||
    localStorage.getItem("HOT_API_URL") ||
    "https://traders-inc-api.onrender.com/api/v1";

  const symbols = [
    "XAUUSD", "XAGUSD", "EURUSD",
    "GBPUSD", "USDJPY", "DXY", "BTCUSD"
  ];

  const $ = id => document.getElementById(id);

  const fmt = v =>
    Number.isFinite(v)
      ? v.toLocaleString(undefined, {
          minimumFractionDigits: 2,
          maximumFractionDigits: 2
        })
      : "—";

  function renderWatchlist(active = "XAUUSD") {
    $("watchlist").innerHTML = symbols.map(s =>
      `<div class="${s === active ? "active" : ""}" data-symbol="${s}">
        ${s}
      </div>`
    ).join("");

    document.querySelectorAll("#watchlist div").forEach(el => {
      el.onclick = () => load(el.dataset.symbol);
    });
  }

  async function get(path) {
    const r = await fetch(
      API.replace(/\/$/, "") + path,
      { headers: { Accept: "application/json" } }
    );

    if (!r.ok) throw new Error(r.status);
    return r.json();
  }

  function fallback(symbol) {
    const base = {
      XAUUSD: 3650.00,
      XAGUSD: 42.10,
      EURUSD: 1.1700,
      GBPUSD: 1.3500,
      USDJPY: 147.20,
      DXY: 97.40,
      BTCUSD: 115000
    };

    return {
      symbol,
      price: base[symbol] ?? 0,
      provider: "DEMO / NO API",
      bias: "NEUTRAL",
      confidence: 0,
      regime: "WAITING"
    };
  }

  async function load(symbol = "XAUUSD") {
    renderWatchlist(symbol);

    let m = fallback(symbol);
    let a = {};

    try {
      if (API) {
        m = {
          ...m,
          ...await get("/market/" + encodeURIComponent(symbol))
        };

        a = await get(
          "/analysis/" + encodeURIComponent(symbol)
        );

        $("api").textContent = "ONLINE";
        $("api").style.color = "#9fd3a8";
      } else {
        $("api").textContent = "STATIC";
      }
    } catch (e) {
      $("api").textContent = "OFFLINE";
      $("api").style.color = "#f2b84b";
    }

    $("price").textContent =
      fmt(Number(m.price ?? m.last ?? m.close));

    $("provider").textContent =
      (m.provider || "MARKET DATA").toUpperCase();

    $("bias").textContent =
      (a.bias || m.bias || "NEUTRAL").toUpperCase();

    const c = Number(
      a.confidence ?? m.confidence ?? 0
    );

    $("conf").textContent =
      (c <= 1 ? c * 100 : c).toFixed(0) + "%";

    $("regime").textContent =
      (a.regime || m.regime || "WAITING").toUpperCase();

    draw();
  }

  function draw() {
    const c = $("canvas");
    const box = c.getBoundingClientRect();
    const d = devicePixelRatio || 1;

    c.width = box.width * d;
    c.height = box.height * d;

    const x = c.getContext("2d");
    x.scale(d, d);

    x.strokeStyle = "#182330";
    x.lineWidth = 1;

    for (let i = 1; i < 8; i++) {
      const y = box.height * i / 8;

      x.beginPath();
      x.moveTo(0, y);
      x.lineTo(box.width, y);
      x.stroke();
    }

    for (let i = 1; i < 12; i++) {
      const xx = box.width * i / 12;

      x.beginPath();
      x.moveTo(xx, 0);
      x.lineTo(xx, box.height);
      x.stroke();
    }

    x.strokeStyle = "#66b3ff";
    x.lineWidth = 2;

    x.beginPath();

    for (let i = 0; i <= 60; i++) {
      const xx = box.width * i / 60;
      const yy =
        box.height * 0.52 -
        Math.sin(i * 0.23) * 35 -
        i * 0.7;

      i ? x.lineTo(xx, yy) : x.moveTo(xx, yy);
    }

    x.stroke();
  }

  function clock() {
    $("clock").textContent =
      new Date().toLocaleString(undefined, {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit"
      });
  }

  window.HouseOfTraders = {
    setApi: url => {
      localStorage.setItem("HOT_API_URL", url);
      location.reload();
    },

    clearApi: () => {
      localStorage.removeItem("HOT_API_URL");
      location.reload();
    }
  };

  renderWatchlist();
  load();
  clock();

  setInterval(clock, 1000);

  setInterval(() => {
    const active =
      document.querySelector("#watchlist .active")
        ?.dataset.symbol || "XAUUSD";

    load(active);
  }, 10000);

  addEventListener("resize", draw);
})();
