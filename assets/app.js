const regulations = [
  {
    id: "subpart-ff",
    citation: "47 CFR PART 1 · SUBPART FF",
    title: "Cable Landing Licenses",
    summary: "海纜登陸許可的現行核心架構，涵蓋申請、認證、例行條件、變更、移轉、續照與終止。",
    topic: ["license"],
    status: "effective",
    date: "Effective · 2026.07.08",
    authority: "47 CFR §§1.70000–1.70024",
    checked: "eCFR 截至 2026.07.30",
    tags: ["47 CFR", "Subpart FF", "許可"],
    points: [
      "2026 年 7 月 8 日起取代舊 §§1.767、1.768，成為 FCC 海纜登陸許可的現行核心規則。",
      "各義務拆分至 §§1.70000–1.70024；引用時應落到具體 section。",
      "eCFR 顯示的 future amendments 不代表相關 FCC 26-42 修正都已生效。"
    ],
    url: "https://www.ecfr.gov/current/title-47/chapter-I/subchapter-A/part-1/subpart-FF"
  },
  {
    id: "definitions",
    citation: "47 CFR §1.70001",
    title: "Definitions",
    summary: "界定 submarine cable system、SLTE 與相關設備的法規邊界，是判讀後續申請與條件的起點。",
    topic: ["license", "equipment"],
    status: "effective",
    date: "Current · 2026.07.30",
    authority: "47 CFR §1.70001",
    checked: "eCFR 截至 2026.07.30",
    tags: ["定義", "SLTE", "system boundary"],
    points: [
      "Submarine cable system 的端到端邊界延伸到一個或多個 SLTE，並包括相關 transponders。",
      "設備、segment、控制關係與持有權的用語應優先採本節定義。",
      "FCC 的 licensing 定義不等同於光學、電氣或可靠度的產品型式規格。"
    ],
    url: "https://www.ecfr.gov/current/title-47/section-1.70001"
  },
  {
    id: "applicant-licensee",
    citation: "47 CFR §1.70003",
    title: "Applicant / licensee requirements",
    summary: "辨識必須列為申請人或 licensee 的實體，核心包含 landing station 控制與 5% 權益門檻。",
    topic: ["license"],
    status: "effective",
    date: "Effective · 2026.07.08",
    authority: "47 CFR §1.70003",
    checked: "eCFR 截至 2026.07.30",
    tags: ["applicant", "licensee", "5%"],
    points: [
      "控制美國 cable landing station 的任何實體，原則上須列為 applicant／licensee。",
      "其他擁有或控制 cable system 5% 以上權益，且使用該系統美國端點的實體亦在核心範圍。",
      "FCC 仍可依個案要求其他實體成為 applicant／licensee。"
    ],
    url: "https://www.ecfr.gov/current/title-47/section-1.70003"
  },
  {
    id: "initial-application",
    citation: "47 CFR §1.70005",
    title: "Initial application",
    summary: "規範初次許可申請的系統、位置、所有權、控制關係及 SLTE／PFE／NOC 等資訊。",
    topic: ["license", "equipment"],
    status: "effective",
    date: "Effective · 2026.07.08",
    authority: "47 CFR §1.70005",
    checked: "eCFR 截至 2026.07.30",
    tags: ["ICFS", "SLTE", "位置資料"],
    points: [
      "申請內容包括 segments、landing points、fiber pairs、design capacity、所有權及控制關係。",
      "須整理 landing station、beach manhole、NOC／SOC、PFE 與 SLTE 的位置及操作資訊。",
      "若未隨初次申請提交精確位置，最遲應於施工前 90 日補交；FCC 原則上有 60 日提出相反通知。"
    ],
    url: "https://www.ecfr.gov/current/title-47/section-1.70005"
  },
  {
    id: "certifications",
    citation: "47 CFR §1.70006",
    title: "Certifications",
    summary: "整合 character、資安、實體安全、Covered List 與例行條件等認證要求。",
    topic: ["license", "security"],
    status: "effective",
    date: "Effective · 2026.07.08",
    authority: "47 CFR §1.70006",
    checked: "eCFR 截至 2026.07.30",
    tags: ["認證", "cybersecurity", "physical security"],
    points: [
      "風險管理計畫應涵蓋機密性、完整性、可用性、存取控制與供應鏈風險。",
      "應由 CEO、CFO、CTO、CISO 或相當資安治理高階主管簽署。",
      "相關實施證明資料自認證提交日起保存 2 年。"
    ],
    url: "https://www.ecfr.gov/current/title-47/section-1.70006"
  },
  {
    id: "routine-conditions",
    citation: "47 CFR §1.70007",
    title: "Routine conditions",
    summary: "許可期限、開始服務、通知、資安與實體安全計畫、Covered List、IRU／lease 等持續義務。",
    topic: ["license", "security", "equipment"],
    status: "effective",
    date: "Effective · 2026.07.08",
    authority: "47 CFR §1.70007",
    checked: "eCFR 截至 2026.07.30",
    tags: ["routine conditions", "25 年", "IRU"],
    points: [
      "License 期限自 in-service date 起 25 年；應在 grant 後 3 年內開始服務。",
      "啟用後 30 日內提交 in-service notification 與安全計畫認證，相關紀錄保存 2 年。",
      "特定安排不得讓 foreign-adversary-controlled entity 安裝、擁有或管理美國登陸海纜的 SLTE，除非獲准。"
    ],
    url: "https://www.ecfr.gov/current/title-47/section-1.70007"
  },
  {
    id: "outage",
    citation: "47 CFR §4.15",
    title: "Submarine cable outage reporting",
    summary: "界定 reportable outage 的 30 分鐘／4 小時門檻，以及 Notification、Interim、Final Report 時限。",
    topic: ["reporting", "equipment"],
    status: "effective",
    date: "Current · 2026.07.30",
    authority: "47 CFR §4.15",
    checked: "eCFR 截至 2026.07.30",
    tags: ["NORS", "outage", "4 小時"],
    points: [
      "SLTE-to-SLTE 間的 failure 或 significant degradation 持續 30 分鐘以上，可能構成 reportable outage。",
      "任一 fiber pair（包括 terminal equipment 所致）在 cable segment 中斷 4 小時以上亦達門檻。",
      "Notification 應於判定後 4 小時內；Interim Report 於收到 repair Plan of Work 後 24 小時內；Final Report 於修復後 7 日內。"
    ],
    url: "https://www.ecfr.gov/current/title-47/section-4.15"
  },
  {
    id: "capacity",
    citation: "47 CFR §43.82",
    title: "Circuit capacity reports",
    summary: "年度 Capacity Holder Report 的對象、資料基準日、提交方式及執法風險。",
    topic: ["reporting", "equipment"],
    status: "effective",
    date: "Annual · MAR 31",
    authority: "47 CFR §43.82",
    checked: "eCFR 截至 2026.07.30",
    tags: ["容量", "annual report", "March 31"],
    points: [
      "Cable landing licensee 與規則所述 common carrier 應於每年 3 月 31 日前提交。",
      "資料基準日為前一曆年 12 月 31 日，並應依 Filing Manual 電子提交。",
      "2026 年已取消重複的 Cable Operator Report，整併至 Capacity Holder Report。"
    ],
    url: "https://www.ecfr.gov/current/title-47/section-43.82"
  },
  {
    id: "slte",
    citation: "EQUIPMENT · SLTE",
    title: "Submarine Line Terminal Equipment",
    summary: "串接海底傳輸與陸上通信網路的終端設備；同時涉及系統定義、申請、outage、容量與國安條件。",
    topic: ["equipment", "security"],
    status: "effective",
    date: "Current framework",
    authority: "§§1.70001, 1.70005, 1.70007, 4.15, 43.82",
    checked: "查核日期 2026.08.01",
    tags: ["SLTE", "terminal equipment", "設備"],
    points: [
      "SLTE 位於海纜系統兩端，負責光訊號與電訊號轉換，使海底傳輸連接陸上通信網路。",
      "現行義務散見系統定義、申請資料、IRU／lease 限制、outage 與容量申報。",
      "FCC 規則未因此自動建立 SLTE 光學、電氣或可靠度的產品性能規格。"
    ],
    url: "https://www.ecfr.gov/current/title-47/section-1.70001"
  },
  {
    id: "fcc-25-49",
    citation: "FCC 25-49 · 90 FR 48648",
    title: "2025 Cable Licensing Modernization",
    summary: "建立 Subpart FF 的海纜規則現代化命令；延後部分自 2026 年 7 月 8 日生效。",
    topic: ["license", "security"],
    status: "effective",
    date: "Current framework",
    authority: "FCC 25-49 / 90 FR 48648",
    checked: "查核日期 2026.08.01",
    tags: ["FCC Order", "modernization", "Subpart FF"],
    points: [
      "將舊制內容重整為 Part 1 Subpart FF 的專門架構。",
      "強化持續監督、國安、資安與實體安全等要求。",
      "最終執行仍應以已生效的 eCFR 條文及 Federal Register 公告為準。"
    ],
    url: "https://docs.fcc.gov/public/attachments/FCC-25-49A1.pdf"
  },
  {
    id: "fcc-26-42",
    citation: "FCC 26-42 · 91 FR 46844",
    title: "SLTE licensing framework",
    summary: "新增 SLTE owners/operators licensing framework；一般規則預定 2026.09.25 生效，多項修正仍無限期延後。",
    topic: ["license", "equipment", "security", "reporting"],
    status: "future",
    date: "General effective · 2026.09.25",
    authority: "FCC 26-42 / FR Doc. 2026-15123",
    checked: "截至 2026.08.01 尚未生效",
    tags: ["FCC 26-42", "SLTE", "delayed"],
    points: [
      "建立 SLTE owner/operator licensing framework 與符合條件者的 blanket license。",
      "未列為延後的 final rules 預定於 2026 年 9 月 25 日生效。",
      "指定 amendatory instructions 因資訊蒐集等程序 delayed indefinitely，必須等待 FCC 另行公告。"
    ],
    url: "https://www.federalregister.gov/d/2026-15123"
  },
  {
    id: "section-1767",
    citation: "HISTORICAL · 47 CFR §1.767",
    title: "Cable landing licenses",
    summary: "2026 年 7 月 8 日前的舊制核心條文；現僅供舊案件、FCC Guide 與 license grant 追溯。",
    topic: ["history", "license"],
    status: "historical",
    date: "Removed · 2026.07.08",
    authority: "Historical 47 CFR §1.767",
    checked: "最後有效日 2026.07.07",
    tags: ["1.767", "歷史", "superseded"],
    points: [
      "2026 年 7 月 8 日自 eCFR 現行架構移除。",
      "原有功能已拆分至 Subpart FF 多個 sections，不能以單一新條號靜默取代。",
      "引用舊案件時應同時記錄適用日期與現行對應條文。"
    ],
    url: "https://www.ecfr.gov/current/title-47/chapter-I/subchapter-A/part-1/subpart-FF"
  },
  {
    id: "section-1768",
    citation: "HISTORICAL · 47 CFR §1.768",
    title: "Foreign carrier affiliation",
    summary: "舊制外國業者關聯條文，2026 年 7 月 8 日移除；現行主要對應 §1.70009。",
    topic: ["history", "license"],
    status: "historical",
    date: "Removed · 2026.07.08",
    authority: "Historical 47 CFR §1.768",
    checked: "最後有效日 2026.07.07",
    tags: ["1.768", "foreign carrier", "superseded"],
    points: [
      "2026 年 7 月 8 日自 eCFR 現行架構移除。",
      "外國業者關聯的現行主要位置為 §1.70009，仍須依具體交易與關聯型態判讀。",
      "舊 FCC Guide 或 grant 的 §1.768 引用應保留作歷史追溯。"
    ],
    url: "https://www.ecfr.gov/current/title-47/section-1.70009"
  }
];

const deadlines = [
  ["精確位置資料未隨申請提交", "施工前至少 90 日", "§§1.70005, 1.70007(h)"],
  ["FCC 對補交位置提出相反通知", "收件後 60 日內", "§1.70005(f)(1)"],
  ["開始服務", "License grant 後 3 年內", "§1.70007(p)"],
  ["In-service notification", "啟用後 30 日內", "§1.70007(p)(1)"],
  ["安全計畫認證", "啟用後 30 日內", "§1.70007(q)(1)"],
  ["Outage Interim Report", "Plan of Work 後 24 小時內", "§4.15(b)(2)(iii)"],
  ["Final Outage Report", "修復後 7 日內", "§4.15(b)(2)(iv)"],
  ["Annual Capacity Holder Report", "每年 3 月 31 日前", "§43.82"]
];

const statusLabels = {
  effective: "現行有效",
  future: "未來／混合",
  historical: "歷史規範",
  proposed: "提案中"
};

const state = {
  query: "",
  topic: "all",
  status: "all"
};

let liveSourceMap = new Map();
let fcc26Rows = [];

const grid = document.querySelector("#regulation-grid");
const resultCount = document.querySelector("#result-count");
const emptyState = document.querySelector("#empty-state");
const searchInput = document.querySelector("#search-input");
const statusFilter = document.querySelector("#status-filter");
const dialog = document.querySelector("#detail-dialog");
const dialogContent = document.querySelector("#dialog-content");

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function normalize(value) {
  return String(value)
    .toLocaleLowerCase("zh-Hant")
    .normalize("NFKC")
    .replaceAll("§", "")
    .replace(/\s+/g, " ")
    .trim();
}

function cardColor(item) {
  if (item.status === "future") return "#f3b44b";
  if (item.status === "historical") return "#839197";
  if (item.topic.includes("security")) return "#78aee8";
  if (item.topic.includes("reporting")) return "#b7e14a";
  return "#00b49d";
}

function matches(item) {
  const haystack = normalize([
    item.citation,
    item.title,
    item.summary,
    item.authority,
    ...item.tags,
    ...item.points
  ].join(" "));
  const queryMatch = !state.query || haystack.includes(normalize(state.query));
  const topicMatch = state.topic === "all" || item.topic.includes(state.topic);
  const statusMatch = state.status === "all" || item.status === state.status;
  return queryMatch && topicMatch && statusMatch;
}

function cardTemplate(item) {
  return [
    '<article class="reg-card" style="--card-color:', cardColor(item), '">',
    '<div class="card-topline"><span class="card-citation">', escapeHtml(item.citation),
    '</span><span class="status-badge ', escapeHtml(item.status), '">',
    escapeHtml(statusLabels[item.status]), '</span></div>',
    '<h3>', escapeHtml(item.title), '</h3><p>', escapeHtml(item.summary), '</p>',
    '<div class="card-tags">',
    item.tags.slice(0, 3).map(tag => '<span>' + escapeHtml(tag) + '</span>').join(""),
    '</div><div class="card-footer"><span class="card-date">', escapeHtml(item.date),
    '</span><button class="card-open" type="button" data-id="', escapeHtml(item.id),
    '">查看重點 →</button></div></article>'
  ].join("");
}

function renderCards() {
  const items = regulations.filter(matches);
  grid.innerHTML = items.map(cardTemplate).join("");
  resultCount.textContent = String(items.length).padStart(2, "0");
  emptyState.hidden = items.length !== 0;
}

function renderDeadlines() {
  document.querySelector("#deadline-body").innerHTML = deadlines
    .map(row => "<tr>" + row.map(cell => "<td>" + escapeHtml(cell) + "</td>").join("") + "</tr>")
    .join("");
}

const fcc26StatusLabels = {
  future_effective: "2026.09.25 預定生效",
  delayed_indefinitely: "無限期延後"
};

function renderFcc26Matrix() {
  const body = document.querySelector("#fcc26-body");
  const query = normalize(document.querySelector("#fcc26-search").value);
  const status = document.querySelector("#fcc26-status-filter").value;
  const rows = fcc26Rows.filter(row => {
    const text = normalize([row.row_id, "instruction " + row.instruction, row.section, row.paragraph, row.action].join(" "));
    return (!query || text.includes(query)) && (status === "all" || row.status === status);
  });
  body.innerHTML = rows.length ? rows.map(row => [
    "<tr><td><strong>", escapeHtml(row.instruction), "</strong><small>", escapeHtml(row.row_id), "</small></td>",
    "<td>", escapeHtml(row.section), " <code>", escapeHtml(row.paragraph), "</code></td>",
    "<td><code>", escapeHtml(row.action), "</code></td>",
    '<td><span class="matrix-status ', escapeHtml(row.status), '">', escapeHtml(fcc26StatusLabels[row.status] || row.status),
    "</span><small>", escapeHtml(row.date || "等待後續公告"), "</small></td>",
    '<td><a href="', escapeHtml(row.official_url), '" target="_blank" rel="noreferrer">', escapeHtml(row.fr_citation), " ↗</a></td></tr>"
  ].join("")).join("") : '<tr><td colspan="5">沒有符合目前條件的 rows。</td></tr>';
  document.querySelector("#fcc26-result").textContent = "顯示 " + rows.length + "／" + fcc26Rows.length + " rows";
}

async function loadFcc26Matrix() {
  try {
    const response = await fetch("data/fcc26-status.json", { cache: "no-store" });
    if (!response.ok) throw new Error("HTTP " + response.status);
    const feed = await response.json();
    fcc26Rows = feed.rows;
    document.querySelector("#fcc26-future-count").textContent = String(fcc26Rows.filter(row => row.status === "future_effective").length);
    document.querySelector("#fcc26-delayed-count").textContent = String(fcc26Rows.filter(row => row.status === "delayed_indefinitely").length);
    renderFcc26Matrix();
  } catch (error) {
    document.querySelector("#fcc26-body").innerHTML = '<tr><td colspan="5">逐項資料暫時無法載入。請使用 91 FR 46844 官方連結核對。</td></tr>';
    document.querySelector("#fcc26-result").textContent = "資料載入失敗";
    console.warn("FCC 26-42 matrix unavailable:", error);
  }
}

function citedSection(item) {
  const match = item.citation.match(/§(\d+\.\d+)/);
  return match ? match[1] : null;
}

function officialTextTemplate(item) {
  const section = citedSection(item);
  const source = section ? liveSourceMap.get(section) : null;
  if (!source || source.content_status !== "current_text" || !source.paragraphs?.length) {
    return "";
  }
  return [
    '<details class="official-text"><summary>檢視自動抓取的官方現行條文 · §',
    escapeHtml(section), '（截至 ', escapeHtml(source.as_of), '）</summary>',
    '<div class="official-text-body"><p class="official-text-note">此處為官方英文來源的自動鏡像；法律狀態仍應搭配 Federal Register 與上方人工整理內容判讀。</p>',
    source.paragraphs.map(paragraph => "<p>" + escapeHtml(paragraph) + "</p>").join(""),
    '</div></details>'
  ].join("");
}

function openDetail(item) {
  const officialText = officialTextTemplate(item);
  dialogContent.innerHTML = [
    '<div class="dialog-inner"><span class="status-badge ', escapeHtml(item.status), '">',
    escapeHtml(statusLabels[item.status]), '</span><p class="dialog-citation">',
    escapeHtml(item.citation), '</p><h2 id="dialog-title">', escapeHtml(item.title),
    '</h2><p class="dialog-summary">', escapeHtml(item.summary),
    '</p><div class="detail-block"><h3>合規重點</h3><ul>',
    item.points.map(point => "<li>" + escapeHtml(point) + "</li>").join(""),
    '</ul></div><div class="detail-meta"><div><span>AUTHORITY</span><strong>',
    escapeHtml(item.authority), '</strong></div><div><span>SOURCE STATUS</span><strong>',
    escapeHtml(item.checked), '</strong></div></div>', officialText,
    '<a class="official-link" href="',
    escapeHtml(item.url), '" target="_blank" rel="noreferrer">開啟官方來源 <span aria-hidden="true">↗</span></a></div>'
  ].join("");
  dialog.showModal();
}

function compactDate(value) {
  return value ? String(value).replaceAll("-", ".") : "—";
}

function localTimestamp(value) {
  if (!value) return "—";
  return new Intl.DateTimeFormat("zh-TW", {
    timeZone: "Asia/Taipei",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    hour12: false
  }).format(new Date(value));
}

async function loadRegulatoryStatus() {
  const panel = document.querySelector("#automation-panel");
  const badge = document.querySelector("#sync-badge");
  try {
    const isGitHubPages = window.location.hostname === "ttchang1127.github.io";
    const feedUrl = isGitHubPages
      ? "https://raw.githubusercontent.com/ttchang1127/FCC_kb/main/data/regulatory-status.json"
      : "data/regulatory-status.json";
    const cacheKey = Math.floor(Date.now() / 300000);
    const response = await fetch(feedUrl + "?v=" + cacheKey, { cache: "no-store" });
    if (!response.ok) throw new Error("HTTP " + response.status);
    const feed = await response.json();
    liveSourceMap = new Map(feed.ecfr.sections.map(section => [section.section, section]));

    const sectionChanges = feed.review.section_changes.length;
    const documentChanges = feed.review.new_federal_register_documents.length;
    const changeCount = sectionChanges + documentChanges;
    const reviewRequired = feed.review.status === "review_required";
    const checkedAt = localTimestamp(feed.generated_at);

    panel.dataset.state = feed.review.status;
    badge.textContent = reviewRequired ? "REVIEW" : "AUTOMATED";
    badge.classList.toggle("review", reviewRequired);
    badge.classList.remove("offline");
    document.querySelector("#live-ecfr-date").textContent = compactDate(feed.ecfr.up_to_date_as_of);
    document.querySelector("#last-auto-check").textContent = "自動檢核 " + checkedAt + " · UTC+8";
    document.querySelector("#automation-ecfr").textContent = feed.ecfr.up_to_date_as_of;
    document.querySelector("#automation-sections").textContent = String(feed.ecfr.current_text_section_count);
    document.querySelector("#automation-fr").textContent = feed.federal_register.latest_publication_date || "—";
    document.querySelector("#automation-changes").textContent = String(changeCount);
    document.querySelector("#footer-check-status").textContent = "Official sources checked " + checkedAt + " · Human review baseline " + (feed.review.ecfr_reviewed_as_of || "—");

    if (reviewRequired) {
      document.querySelector("#automation-title").textContent = "官方來源有變動，待人工複核";
      document.querySelector("#automation-message").textContent = "偵測到 " + sectionChanges + " 個條文變動與 " + documentChanges + " 份新 Federal Register 文件；中文摘要尚未自動改寫。";
    } else {
      document.querySelector("#automation-title").textContent = "官方來源已自動檢核";
      document.querySelector("#automation-message").textContent = "目前來源雜湊與人工審核基準一致；官方條文全文每日自動更新。";
    }
  } catch (error) {
    panel.dataset.state = "error";
    badge.textContent = "OFFLINE";
    badge.classList.add("offline");
    document.querySelector("#automation-title").textContent = "無法讀取自動檢核資料";
    document.querySelector("#automation-message").textContent = "請直接查閱 eCFR，或查看 GitHub Actions 執行紀錄。";
    document.querySelector("#last-auto-check").textContent = "自動來源資料暫時無法載入";
    console.warn("Regulatory status feed unavailable:", error);
  }
}

function clearFilters() {
  state.query = "";
  state.topic = "all";
  state.status = "all";
  searchInput.value = "";
  statusFilter.value = "all";
  document.querySelectorAll("[data-filter='topic']").forEach(button => {
    button.classList.toggle("active", button.dataset.value === "all");
  });
  renderCards();
}

searchInput.addEventListener("input", event => {
  state.query = event.target.value;
  renderCards();
});

statusFilter.addEventListener("change", event => {
  state.status = event.target.value;
  renderCards();
});

document.querySelectorAll("[data-filter='topic']").forEach(button => {
  button.addEventListener("click", () => {
    state.topic = button.dataset.value;
    document.querySelectorAll("[data-filter='topic']").forEach(item => {
      item.classList.toggle("active", item === button);
    });
    renderCards();
  });
});

grid.addEventListener("click", event => {
  const button = event.target.closest("[data-id]");
  if (!button) return;
  const item = regulations.find(regulation => regulation.id === button.dataset.id);
  if (item) openDetail(item);
});

document.querySelector("#clear-filters").addEventListener("click", clearFilters);
document.querySelector("#fcc26-search").addEventListener("input", renderFcc26Matrix);
document.querySelector("#fcc26-status-filter").addEventListener("change", renderFcc26Matrix);
document.querySelector("[data-open-status]").addEventListener("click", () => {
  document.querySelector("#transition").scrollIntoView({ behavior: "smooth" });
});

document.querySelector(".dialog-close").addEventListener("click", () => dialog.close());
dialog.addEventListener("click", event => {
  if (event.target === dialog) dialog.close();
});

document.addEventListener("keydown", event => {
  if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
    event.preventDefault();
    searchInput.focus();
  }
});

renderDeadlines();
renderCards();
loadFcc26Matrix();
loadRegulatoryStatus();
