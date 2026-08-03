const tg = window.Telegram?.WebApp;
tg?.ready();
tg?.expand();

// Должно совпадать с items.py на бэкенде — здесь используется только
// для "прокрутки" ленты и таблицы шансов. Итог всегда решает сервер.
// weight — в сотых долях процента (4500 = 45.00%), как и на бэкенде.
const ITEMS = [
  { name: "Обычный болтик",      value: 10,    rarity: "common",    weight: 4500 },
  { name: "Стальной ключ",       value: 25,    rarity: "uncommon",  weight: 2500 },
  { name: "Серебряный жетон",    value: 60,    rarity: "rare",      weight: 1500 },
  { name: "Золотая монета",      value: 150,   rarity: "epic",      weight: 800  },
  { name: "Бриллиант",           value: 400,   rarity: "legendary", weight: 500  },
  { name: "Мифический артефакт", value: 1500,  rarity: "mythic",    weight: 200  },
  { name: "Джекпот",             value: 50000, rarity: "jackpot",   weight: 1    },
];

const RARITY_COLOR_VAR = {
  common: "--common",
  uncommon: "--uncommon",
  rare: "--rare",
  epic: "--epic",
  legendary: "--legendary",
  mythic: "--mythic",
  jackpot: "--jackpot",
};

const ITEM_WIDTH = 120; // reel-item width (100) + margins (10+10)
const REEL_LENGTH = 40;
const WINNING_INDEX = 30;

const balanceEl = document.getElementById("balance");
const costEl = document.getElementById("cost");
const openBtn = document.getElementById("openBtn");
const reelEl = document.getElementById("reel");
const resultEl = document.getElementById("result");
const oddsToggle = document.getElementById("oddsToggle");
const oddsPanel = document.getElementById("oddsPanel");

let spinCost = 0;
let spinning = false;

function rarityColor(rarity) {
  const varName = RARITY_COLOR_VAR[rarity] || "--common";
  return getComputedStyle(document.documentElement).getPropertyValue(varName).trim();
}

function initData() {
  return tg?.initData || "";
}

function randomItem() {
  return ITEMS[Math.floor(Math.random() * ITEMS.length)];
}

function renderReelItem(item) {
  const color = rarityColor(item.rarity);
  const div = document.createElement("div");
  div.className = "reel-item";
  div.dataset.rarity = item.rarity;
  div.style.borderColor = color;
  div.innerHTML = `
    <div class="reel-item-icon" style="background:${color}33"></div>
    <div class="reel-item-name">${item.name}</div>
    <div class="reel-item-value">${item.value} 💰</div>
  `;
  return div;
}

function buildReel(prizeItem) {
  reelEl.innerHTML = "";
  reelEl.style.transition = "none";
  reelEl.style.transform = "translateX(0px)";

  for (let i = 0; i < REEL_LENGTH; i++) {
    const item = i === WINNING_INDEX ? prizeItem : randomItem();
    reelEl.appendChild(renderReelItem(item));
  }
}

function renderOdds() {
  oddsPanel.innerHTML = ITEMS
    .map((item) => {
      const color = rarityColor(item.rarity);
      return `
        <div class="odds-row">
          <span class="odds-name">
            <span class="odds-dot" style="background:${color}"></span>${item.name}
          </span>
          <span class="odds-chance">${item.weight}% · ${item.value} 💰</span>
        </div>
      `;
    })
    .join("");
}

oddsToggle.addEventListener("click", () => {
  oddsPanel.classList.toggle("open");
});

async function loadMe() {
  try {
    const res = await fetch("/api/me", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ initData: initData() }),
    });
    const data = await res.json();
    if (data.error) {
      resultEl.textContent = "Открой мини-апп через кнопку в боте — так работает авторизация.";
      return;
    }
    spinCost = data.spin_cost;
    balanceEl.textContent = data.balance;
    costEl.textContent = spinCost;
    openBtn.disabled = false;
  } catch (e) {
    resultEl.textContent = "Не удалось связаться с сервером.";
  }
}

async function spin() {
  if (spinning) return;
  spinning = true;
  openBtn.disabled = true;
  resultEl.textContent = "";

  let data;
  try {
    const res = await fetch("/api/spin", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ initData: initData() }),
    });
    data = await res.json();
  } catch (e) {
    resultEl.textContent = "Ошибка сети, попробуй ещё раз.";
    spinning = false;
    openBtn.disabled = false;
    return;
  }

  if (data.error) {
    resultEl.textContent =
      data.error === "not enough coins" ? "Недостаточно монет 😢" : "Что-то пошло не так, попробуй ещё раз.";
    spinning = false;
    openBtn.disabled = false;
    return;
  }

  buildReel(data.prize);

  const wrapWidth = reelEl.parentElement.offsetWidth;
  const centerOffset = wrapWidth / 2 - ITEM_WIDTH / 2;
  const jitter = Math.random() * 30 - 15;
  const targetX = -(WINNING_INDEX * ITEM_WIDTH) + centerOffset + jitter;

  requestAnimationFrame(() => {
    reelEl.style.transition = "transform 4.2s cubic-bezier(0.1, 0.7, 0.15, 1)";
    reelEl.style.transform = `translateX(${targetX}px)`;
  });

  setTimeout(() => {
    balanceEl.textContent = data.balance;
    const net = data.prize.value - spinCost;
    resultEl.innerHTML = `Выпало: <b>${data.prize.name}</b> · ${data.prize.value} 💰 ${net >= 0 ? "🎉" : ""}`;
    tg?.HapticFeedback?.notificationOccurred(net >= 0 ? "success" : "warning");
    spinning = false;
    openBtn.disabled = false;
  }, 4400);
}

openBtn.addEventListener("click", spin);
renderOdds();
loadMe();
