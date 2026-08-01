# FCC_kb 待辦與交接

> 最後人工更新：2026-08-01（Asia/Taipei）<br>
> 使用方式：每次開始工作先讀本檔，再查看 `data/regulatory-status.json` 與 GitHub Actions 最新執行結果；完成工作後同步更新本檔並推送。

> AI 注意：本檔是人類可讀 roadmap；真正的任務順序、依賴與狀態以 `tasks/queue.json` 為準。不得直接從本頁任選 checkbox。

## 0. 無腦接手指令

任何 AI 模型先執行：

```bash
python3 scripts/agent_preflight.py
python3 scripts/taskctl.py validate
python3 scripts/taskctl.py next --mode auto
```

只做 `next` 顯示的一個 task。完整規則見 `AGENTS.md`；Gemini 先讀 `GEMINI.md`；逐步配方見 `docs/AI_RUNBOOK.md`。

## 1. 專案目標

建立可追溯、可區分法律狀態且能自動監測官方來源的 FCC 海底電纜規範知識庫，涵蓋：

- Cable landing license 與 47 CFR Part 1 Subpart FF。
- 歷史 §§1.767、1.768 與現行條文對照。
- SLTE、PFE、landing station、NOC／SOC 等設備及設施。
- 國安、外資、Covered List、資安及實體安全。
- Outage、capacity、annual／one-time reporting。
- ICFS 申請、移轉、變更、續照及終止流程。
- 個別 license、waiver、特殊國安條件與 enforcement 案例。

本 repository 是公開網站與自動化層；本機 Obsidian 原始筆記、官方 PDF、XML 快照及同步工作檔不在 Git 中。

## 2. 目前可用成果

| 項目 | 狀態 | 說明 |
|---|---|---|
| 公開網站 | ✅ 已上線 | <https://ttchang1127.github.io/FCC_kb/> |
| GitHub repository | ✅ 已同步 | <https://github.com/ttchang1127/FCC_kb> |
| GitHub Pages | ✅ 已啟用 | `main`／root |
| 官方來源自動監測 | ✅ 每日執行 | 台北時間約 04:23 |
| eCFR 監測範圍 | ✅ 35 sections | 目前 28 個有現行文字；其餘為 reserved／future placeholder |
| Federal Register 監測 | ✅ 已啟用 | 搜尋 FCC 海纜直接相關文件 |
| 變更偵測 | ✅ 已啟用 | SHA-256 對照人工審核基準 |
| AI 機械化交接 | ✅ 已啟用 | 35 個任務、依賴、recipes、preflight 與驗證工具 |
| 中文整理卡 | 🟡 部分完成 | 網站 13 張公開卡；Obsidian 28 個 Markdown |
| 結構健檢 | ✅ 通過 | 重複 ID、YAML 錯誤、缺欄位、壞連結均為 0 |

目前人工法律基準：

- eCFR Title 47 資料截至 2026-07-30。
- 人工查核日期 2026-08-01。
- §§1.767、1.768 最後有效日為 2026-07-07，2026-07-08 移除。
- Subpart FF 是現行核心架構。
- FCC 26-42 一般規則預定 2026-09-25 生效；多項 amendatory instructions 仍無限期延後。

## 3. 在任何電腦開始工作

### 3.1 只處理公開網站與自動化

```bash
git clone git@github.com:ttchang1127/FCC_kb.git
cd FCC_kb
git pull --ff-only origin main
python3 scripts/update_regulatory_data.py
python3 -m http.server 4173
```

瀏覽器開啟 <http://127.0.0.1:4173/>。

若新電腦尚未設定 GitHub SSH 金鑰，可改用唯讀 HTTPS clone：

```bash
git clone https://github.com/ttchang1127/FCC_kb.git
```

要從該電腦 push，仍須另外完成 GitHub SSH 或 HTTPS token 認證。

開始修改前必查：

```bash
git status --short
git log --oneline -5
python3 -m py_compile scripts/update_regulatory_data.py
node --check assets/app.js
```

### 3.2 要處理完整 Obsidian 知識庫

完整 Obsidian vault 位於外接磁碟，不包含在 GitHub clone：

```text
/Volumes/Crucial X8/Jarvis Obsidian/FCC_kb
```

應先確認下列本機檔案存在：

```text
00_首頁/
01_規範總覽/
02_法源與原文索引/
03_主題整合/
04_合規流程映射/
05_跨版本與法律狀態比較/
06_案例命令與許可/
07_申報通報與期限/
08_設備與系統卡/
99_資料治理/
```

若在其他電腦沒有掛載該 vault，只能處理公開網站與自動化，不能假設完整 Obsidian 內容已隨 Git clone 取得。

## 4. 自動更新的實際邊界

自動流程：

1. `scripts/update_regulatory_data.py` 從 eCFR API 抓取現行英文條文。
2. 搜尋 FederalRegister.gov 的 FCC 海纜相關文件。
3. 寫入 `data/regulatory-status.json`。
4. 與 `data/review-baseline.json` 的人工審核雜湊比較。
5. 若資料變動，網站顯示「待人工複核」。
6. GitHub Actions 自動提交最新來源 JSON。

自動流程不會：

- 自動改寫中文法律摘要。
- 自動判定延後條文已生效。
- 自動把個案條件泛化成所有 licensee 的義務。
- 更新被 `.gitignore` 排除的本機 Obsidian 卡片、PDF 或 XML 快照。

只有完成法律內容複核後，才可執行：

```bash
python3 scripts/update_regulatory_data.py --accept-current
```

這會更新人工審核基準，不能只因 Action 顯示變動就直接執行。

## 5. P0：2026-09-25 前必做

### 5.1 FCC 26-42 生效矩陣

- [x] 建立逐 amendatory instruction 對照表。
- [x] 對每項標示 `effective`、`future_effective`、`delayed_indefinitely` 或 `proposed`。
- [x] 記錄 CFR section、段落、資訊蒐集／OMB 狀態、Federal Register 文件及日期。
- [x] 網站新增可篩選的 FCC 26-42 生效矩陣。
- [ ] 2026-09-25 前後各執行一次人工複核。

驗收標準：任何使用者都能回答「哪個段落在何時生效、哪個仍延後」，且每列可回到官方來源。

### 5.2 官方變動通知

- [x] 條文或新 Federal Register 文件出現時，自動建立或更新單一 GitHub Issue。
- [x] 避免每天建立重複 Issue。
- [x] Issue 列出 section、舊／新 SHA-256、官方 URL 與發現時間。
- [x] Action 失敗時提供明確通知入口。

驗收標準：不必每天打開網站，也能知道官方來源是否發生變動。

## 6. P1：補齊核心法規卡

已完成的 Subpart FF 詳細卡：

- [x] §1.70001 Definitions
- [x] §1.70003 Applicant/licensee requirements
- [x] §1.70005 Initial application
- [x] §1.70006 Certifications
- [x] §1.70007 Routine conditions

待建立的實質條文卡：

- [ ] §1.70000 Purpose
- [ ] §1.70002 General requirements
- [ ] §1.70004 Additional presumptive disqualifying conditions
- [ ] §1.70008 Special temporary authority
- [ ] §1.70009 Foreign carrier affiliation
- [ ] §1.70010 Amendment of applications
- [ ] §1.70011 Modification applications
- [ ] §1.70012 Substantial assignment／transfer of control
- [ ] §1.70013 Pro forma assignment／transfer notifications
- [ ] §1.70014 Processing of applications
- [ ] §1.70015 Quarterly reports
- [ ] §1.70016 Eligibility for streamlining
- [ ] §1.70017 Foreign adversary annual report
- [ ] §1.70020 Renewal and extension applications
- [ ] §1.70021 Electronic filing
- [ ] §1.70022 Revocation and termination
- [ ] §1.70023 Covered List certification
- [ ] §1.70024 One-time security certification

狀態監測但不當成完整現行條文：

- [ ] §1.70018 placeholder 狀態說明
- [ ] §1.70019 Reserved 狀態說明
- [ ] §§1.70025–1.70029 future placeholder／延後狀態說明

每張條文卡驗收標準：

- 有 `legal_status`、`source_checked_at`、`ecfr_up_to_date_as_of`。
- 有官方 URL、適用主體、觸發事件、期限、設備、申報系統與例外。
- 數字及日期可回查原文段落。
- 明確區分現行、未來、延後、提案與歷史內容。
- 通過 `fcc_kb_health.py`。

## 7. P1：周邊法源與程序

- [ ] 建立 47 CFR §1.40001 Executive Branch review 卡。
- [ ] 建立 47 CFR §63.18 International Section 214 卡。
- [ ] 建立 Part 1 Subpart DD／§1.50002 Covered List 卡。
- [ ] 建立 cable landing license 與 Section 214 authority 邊界比較。
- [ ] 建立 ICFS 申請類型矩陣。
- [ ] 建立初次申請、modification、assignment、transfer、renewal、STA、termination 流程。
- [ ] 補上 Filing Manual、ICFS、NORS 與 capacity reporting 最新入口。
- [ ] 建立申請附件、公開／機密資料及位置資訊處理矩陣。

驗收標準：從事件出發能找到正確 filing type、表單／系統、附件、期限及法源。

## 8. P2：設備與設施卡

- [x] SLTE
- [ ] Power Feed Equipment（PFE）
- [ ] Transponder
- [ ] Repeater
- [ ] Branching Unit
- [ ] Cable Landing Station
- [ ] Beach Manhole
- [ ] NOC／Backup NOC
- [ ] SOC／Backup SOC
- [ ] Wet Segment／Dry Segment

每張設備卡驗收標準：

- 說明系統功能與 FCC 法規中的角色。
- 列出申請、ownership／control、security、reporting 與 outage 關聯。
- 分開標示 FCC 義務及非 FCC 的 ITU-T／IEC／Telcordia 或業主技術規格。
- 不把 licensing 或 security 規則誤寫成產品性能強制值。

## 9. P2：跨主題合規整理

- [ ] Applicant、licensee、owner、operator、IRU holder、lessee 角色矩陣。
- [ ] Foreign ownership／foreign carrier affiliation 主題卡。
- [ ] Foreign adversary／Covered List／principal equipment 主題卡。
- [ ] Cybersecurity／physical security plan 實施與保存義務卡。
- [ ] Outage 判定樹與 NORS 提交流程。
- [ ] Annual capacity report 欄位及資料責任矩陣。
- [ ] 海纜生命週期：規劃、申請、施工、啟用、營運、變更、續照、終止。

## 10. P3：案例庫

- [ ] 建立個別 cable landing license grant 樣本及欄位模板。
- [ ] 蒐集含特殊國安／Team Telecom mitigation conditions 的案例。
- [ ] 蒐集 assignment、transfer、renewal 案例。
- [ ] 蒐集 waiver 准駁案例。
- [ ] 蒐集 enforcement、revocation、termination 案例。
- [ ] 每個案例區分個案條件與通案義務。

## 11. P3：網站與品質

- [ ] 建立完整 35-section 官方全文索引頁，不只依附在 13 張整理卡中。
- [x] 新增 FCC 26-42 生效矩陣頁。
- [ ] 新增 filing／deadline 可下載表格。
- [ ] 加入網站自動化測試：資料 schema、搜尋、篩選、dialog、手機無溢位。
- [ ] 加入無障礙檢查與外部連結檢查。
- [ ] 為來源更新失敗設計清楚的 stale-data 警示。

## 12. 每次工作的結束程序

### 公開 repository

```bash
node --check assets/app.js
python3 -m py_compile scripts/update_regulatory_data.py
python3 scripts/update_regulatory_data.py
git diff --check
git status --short
git add <明確檔案>
git commit -m "清楚說明本次成果"
git push origin main
git status --short
```

確認：

- [ ] `local HEAD` 與 `origin/main` 相同。
- [ ] GitHub Action 成功。
- [ ] 正式網站載入正常。
- [ ] 沒有 Obsidian 原始庫、PDF、XML snapshot 或敏感位置資料進入 staged files。
- [ ] 更新本 TODO 的完成狀態與「最後人工更新」日期。

### 完整 Obsidian vault

```bash
python3 99_資料治理/fcc_kb_sync.py
python3 99_資料治理/fcc_kb_health.py
```

確認：

- [ ] 重複 ID 為 0。
- [ ] YAML 錯誤為 0。
- [ ] 缺欄位為 0。
- [ ] 壞連結為 0。
- [ ] 新卡已連回總覽、主題及相關設備／流程卡。

## 13. 法律內容安全規則

- 先判斷法律狀態，再引用內容。
- eCFR future amendment 連結不等於已生效。
- Federal Register final rule、effective-date notice 與 proposed rule 必須分開。
- FCC Guide 若仍引用 §§1.767／1.768，須保留歷史引用並另列現行 Subpart FF 對應。
- 個別 license condition 不得直接當成所有 licensee 的通案義務。
- 精確 landing station、beach manhole、SLTE 或路由位置不得放入公開 repository。
- 自動抓取結果只代表來源內容變動，不代表已完成法律判讀。

## 14. 關鍵檔案

| 檔案 | 用途 |
|---|---|
| `README.md` | 公開專案說明與啟動入口 |
| `TODO.md` | 跨電腦工作交接及待辦單一入口 |
| `index.html` | 網站主頁 |
| `assets/app.js` | 規範卡、搜尋、篩選及自動狀態載入 |
| `assets/site.css` | 網站樣式與響應式版面 |
| `scripts/update_regulatory_data.py` | 官方來源抓取及差異判定 |
| `data/regulatory-status.json` | 最新自動來源資料 |
| `data/review-baseline.json` | 人工審核基準 |
| `.github/workflows/update-regulations.yml` | 每日自動更新排程 |
| `AGENTS.md` | 所有 AI 的強制工作規則 |
| `GEMINI.md` | Gemini 的最小啟動入口 |
| `tasks/queue.json` | 機器可讀任務順序、依賴及驗收 |
| `scripts/agent_preflight.py` | 環境、Git、來源及下一任務檢查 |
| `scripts/taskctl.py` | 任務查詢、開始、完成及阻擋控制 |
| `scripts/verify_project.py` | 公開邊界、資料 schema 與程式驗證 |

## 15. 下一個工作階段建議

優先執行：**FCC 26-42 逐 amendatory instruction 生效矩陣**。

原因：距離 2026-09-25 一般生效日最近，且目前最大的法律風險是把未來生效、延後及提案內容混入現行義務。完成後再依序補齊 Subpart FF 條文卡、§1.40001／§63.18 及 ICFS 流程矩陣。
