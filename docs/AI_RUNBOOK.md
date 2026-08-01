# AI 機械化操作手冊

只執行 `tasks/queue.json` 指定的 recipe。每一步都要留下可檢查的檔案或指令結果。

## 通用流程

```text
PRECHECK → READ OFFICIAL SOURCE → CLASSIFY STATUS → WRITE ONE OUTPUT
→ LINK → VERIFY → RECORD EVIDENCE → COMMIT → PUSH
```

### PRECHECK

```bash
python3 scripts/agent_preflight.py
python3 scripts/taskctl.py validate
python3 scripts/taskctl.py show <TASK_ID>
git status --short
python3 scripts/taskctl.py start <TASK_ID>
```

若 preflight 或 task 顯示 `BLOCKED`，停止。`start` 成功後 `tasks/queue.json` 會成為本 task 的第一個預期修改檔案。

### 官方來源順序

1. Federal Register：判斷 final／proposed、effective date、delayed instruction。
2. eCFR：取得目前編纂文字及 future amendment 標記。
3. FCC Order／Public Notice：理解命令理由、附件及執行細節。
4. 個別 license／waiver／enforcement order：只用於個案卡。
5. FCC Guide：只作操作導覽，不凌駕 CFR 或 Federal Register。

## Recipe：`STATUS_MATRIX`

用途：FCC 26-42 或其他命令逐 amendatory instruction 生效矩陣。

1. 開啟 task 的每一個 `sources` URL。
2. 從 Federal Register `DATES` 段逐字辨識一般生效日及延後 instruction 編號。
3. 從 amendatory text 記錄 instruction、section、paragraph、action。
4. 每列只能使用決策表允許的法律狀態。
5. 無法由來源確認的列填 `needs_human_review`，不得留白或猜測。
6. 使用 `templates/status-matrix.md` 的欄位。
7. 建立 Obsidian 卡後，建立公開 JSON／網站表格；兩者列數及 ID 必須一致。
8. 驗證每列都有官方 URL、FR citation、日期與 status reason。

完成條件：矩陣能機械回答「哪一條、哪一段、何時生效、證據在哪裡」。

## Recipe：`CFR_CARD`

用途：單一 CFR section 整理卡。一次只能處理一個 section。

1. 確認 mode 是 `full_vault`。
2. 從 `data/regulatory-status.json` 找到相同 `section`。
3. 開啟該筆 `official_url`，核對自動抓取文字與官方頁。
4. 若 `content_status` 不是 `current_text`，停止一般卡流程，改用 `STATUS_NOTE`。
5. 依序抽取：適用主體、觸發事件、必須動作、期限、例外、申報系統、設備、紀錄保存、其他 section 連結。
6. 每個數字都附 paragraph citation；沒有數字就寫 `未規定`，不要推算。
7. 使用 `templates/cfr-card.md`。
8. 連回 `00_Subpart_FF總索引`、主題卡、流程卡與設備卡。
9. 執行 full-vault 健檢。

完成條件：卡片不看摘要也能回查每項義務的 paragraph。

## Recipe：`STATUS_NOTE`

用途：Reserved、`xxx`、future placeholder、removed section。

1. 不整理 placeholder 文字成義務。
2. 記錄 eCFR 顯示狀態、Federal Register instruction、目前是否有 effective date。
3. 標示 `reserved`、`future_placeholder`、`delayed_indefinitely` 或 `superseded`。
4. 說明「目前不能用這個 section 做什麼」。
5. 提供下一次應監測的官方公告類型。

## Recipe：`EQUIPMENT_CARD`

1. 確認 mode 是 `full_vault`。
2. 使用 `templates/equipment-card.md`。
3. 從 CFR 只整理 licensing、ownership、operation、security、reporting、outage。
4. 技術性能如來自 ITU-T／IEC／Telcordia，放在「非 FCC 技術標準」，不得標成 FCC 強制值。
5. 列出設備出現的所有 CFR sections 及 paragraph。
6. 列出申請資料、保密性、持續義務及事件通報。
7. 連回 SLTE／系統邊界與生命週期卡。

## Recipe：`FILING_MATRIX`

1. 先定義事件：initial、modification、assignment、transfer、renewal、STA、termination。
2. 每個事件分開記錄 filing system、form、附件、公開／機密、fee、public notice、streamlining、deadline。
3. 沒有官方明文的欄位寫 `需查 Filing Manual`，不得類推。
4. Cable landing license 與 Section 214 分欄，不得合併。
5. 以 CFR 為義務法源、FCC Guide／Filing Manual 為操作來源。

## Recipe：`WEB_FEATURE`

1. 只能使用公開資料。
2. 先定義輸入 JSON schema，再改 HTML／JS／CSS。
3. 保留無 JavaScript 或 feed 失敗時的安全 fallback。
4. 不得在前端自動把 `review_required` 轉成 `current`。
5. 執行：

```bash
node --check assets/app.js
python3 scripts/verify_project.py
python3 -m http.server 4173
```

6. 驗證桌面、390px 手機、搜尋、篩選、dialog、外部連結。

## Recipe：`CHANGE_ALERT`

1. 只在 `review.status == review_required` 時建立／更新 Issue。
2. 使用固定 label 與固定搜尋條件避免重複 Issue。
3. Issue 必須包含 section changes、新 FR 文件、舊／新 hash、官方 URL、generated_at。
4. `current` 時不得建立新 Issue；可關閉已解決且人工確認的 Issue，但不能自動 accept baseline。
5. GITHUB_TOKEN 權限採最小化：`contents: write`、`issues: write`。

## Recipe：`CASE_CARD`

1. 只處理 task 明確指定的 FCC order／license／waiver。
2. 記錄 applicant、cable、file number、grant date、authority、特殊條件、有效期間。
3. 每一個特殊條件標示 `case_specific: true`。
4. 不得從單一案例推導通案義務。

## 驗證失敗處理

```text
可在單一 task 範圍內修正 → 修正後重跑全部驗證
需要擴大範圍 → BLOCKED，要求使用者授權
官方來源不明 → needs_human_review，停止法律結論
環境缺 full vault → BLOCKED，不建立假檔案
```
