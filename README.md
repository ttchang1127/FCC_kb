# FCC 海纜規範知識庫

以繁體中文整理 FCC 對海底電纜登陸許可、SLTE、通報與容量申報的公開靜態網站。

後續工作、跨電腦啟動方式及驗收標準請先讀 [`TODO.md`](TODO.md)。

## AI／代理接手

不論使用 Codex、Gemini 或其他模型，第一步固定執行：

```sh
python3 scripts/agent_preflight.py
python3 scripts/taskctl.py validate
python3 scripts/taskctl.py next --mode auto
```

代理必須依序閱讀 [`AGENTS.md`](AGENTS.md)、[`TODO.md`](TODO.md)、[`docs/AI_RUNBOOK.md`](docs/AI_RUNBOOK.md) 與 [`docs/LEGAL_STATUS_DECISION_TABLE.md`](docs/LEGAL_STATUS_DECISION_TABLE.md)。Gemini 另有自動入口 [`GEMINI.md`](GEMINI.md)。機器可讀任務與依賴位於 [`tasks/queue.json`](tasks/queue.json)。

- 法規資料截至：2026-07-30（eCFR Title 47）
- 人工查核日期：2026-08-01
- 網站：啟用 GitHub Pages 後可由 `https://ttchang1127.github.io/FCC_kb/` 瀏覽

## 公開範圍

此 repository 僅包含網頁、樣式與經整理的公開資料。Obsidian 原始筆記、官方 PDF、來源快照及同步腳本均由 `.gitignore` 排除，不會上傳。

## 本機預覽

```sh
python3 -m http.server 4173
```

開啟 `http://127.0.0.1:4173/`。

## 自動更新

GitHub Actions 每日約於台北時間 04:23 執行 `scripts/update_regulatory_data.py`：

- 從 eCFR API 抓取 Part 1 Subpart FF §§1.70000–1.70029、§4.15、§43.82 等監測條文全文。
- 從 FederalRegister.gov API 搜尋 FCC 海纜相關 final rule、proposed rule 與生效公告。
- 以 SHA-256 與人工審核基準比較；若來源內容改變，網站會顯示「待人工複核」。
- 自動來源資料寫入 `data/regulatory-status.json`，並由 GitHub Actions 提交至 `main`。
- 正式網站直接讀取 `main` 的最新公開 JSON，因此自動 commit 不需另外觸發 Pages rebuild。

可在 repository 的 Actions 頁面手動執行 **Update FCC regulatory sources**。只有完成法律內容複核後，才應以 `python3 scripts/update_regulatory_data.py --accept-current` 更新人工審核基準。

## 重要聲明

本網站是研究與合規導覽工具，不構成法律意見。正式申請、申報或作成合規判斷前，應回查 eCFR、Federal Register、FCC 命令、最新表單及個別 license conditions。
