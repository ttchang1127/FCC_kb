# FCC_kb AI 操作規則

本檔是所有 AI／coding agent 的最高優先專案操作入口。不要憑記憶接手，也不要先修改檔案。

## 強制啟動程序

依序執行，不得跳步：

```bash
python3 scripts/agent_preflight.py
python3 scripts/taskctl.py validate
python3 scripts/taskctl.py next --mode auto
```

接著：

1. 讀取 `TODO.md`。
2. 讀取 `docs/AI_RUNBOOK.md`。
3. 讀取 `docs/LEGAL_STATUS_DECISION_TABLE.md`。
4. 只領取 `taskctl.py next` 顯示的一個任務。
5. 執行 `python3 scripts/taskctl.py show <TASK_ID>`。
6. 確認工作樹乾淨後，執行 `python3 scripts/taskctl.py start <TASK_ID>`。
7. 完整照該任務指定的 recipe 操作。
8. 執行 `python3 scripts/verify_project.py`；完整 vault 模式再加 `--full-vault`。
9. 驗收全部通過後才更新任務狀態、commit、push。

## 兩種環境模式

`agent_preflight.py` 會自動判定：

- `public`：一般 GitHub clone。只能改公開網站、自動化、文件及 `tasks/queue.json`。
- `full_vault`：同時存在 `00_首頁/` 與 `99_資料治理/`。可改完整 Obsidian 知識庫，也可做 public 任務。

若任務要求 `full_vault`，但 preflight 顯示 `public`：立即停止，不得自行建立假的 vault 目錄。

## 單一任務規則

- 一次只做一個 task ID。
- 不得順便做 queue 中其他任務。
- 不得修改 task 的驗收標準來讓自己通過。
- 任務有 dependency 未完成時不得開始。
- 任務狀態不是 `ready` 時不得開始，除非使用者明確指定恢復 `in_progress` 任務。
- 所有成果必須能對應到 task 的 `targets` 與 `acceptance`。

## 法律內容硬限制

- 只以 eCFR、Federal Register、FCC、Congress／U.S. Code、White House／Executive Order、govinfo 等第一方來源作法律結論。
- 先判斷 `effective`、`future_effective`、`delayed_indefinitely`、`proposed`、`superseded`，再整理內容。
- eCFR future amendment、placeholder 或 `xxx` 不等於現行有效條文。
- Proposed rule／FNPRM 不得寫成現行義務。
- FCC Order 的發布不等於所有 amendatory instructions 已生效。
- 個別 license condition 不得泛化成所有 licensee 的通案義務。
- 不確定時標示 `needs_human_review`，不得猜測。
- 未完成人工逐項複核，禁止執行 `update_regulatory_data.py --accept-current`。

## 公開資料硬限制

禁止提交：

- `00_首頁/` 至 `08_設備與系統卡/` 的完整本機 Obsidian 內容。
- `99_資料治理/`、來源快照、PDF、XML 原始檔。
- 精確 landing station、beach manhole、SLTE、PFE、NOC／SOC 或 route position 位置。
- token、密碼、SSH key、cookie、個人資料或未公開申請資料。

不得為了方便而放寬 `.gitignore`。提交前必須執行：

```bash
git diff --cached --name-only
python3 scripts/verify_project.py
```

## 停止條件

遇到任何一項，立即停止並回報，不得自行跨越：

- `data/regulatory-status.json` 的 `review.status` 是 `review_required`，但任務不是來源變動複核。
- Git 工作樹有無法辨識或可能屬於使用者的既有修改。
- 官方來源互相矛盾，或找不到生效公告。
- 任務要求 full vault，但目前只有 public clone。
- 任務要求個案資料，但來源未明確指定。
- 驗證指令失敗且無法在該 task 範圍內修正。
- 需要改變公開／私人資料邊界。
- 需要 token、管理員設定或新的外部權限。

## 固定結束程序

```bash
python3 scripts/verify_project.py
git diff --check
git status --short
git diff --cached --name-only
```

若 task 驗收完成：

```bash
python3 scripts/taskctl.py complete <TASK_ID> --evidence "完成檔案與驗證摘要"
git add tasks/queue.json <本次明確檔案>
git commit -m "<類型>：<單一任務成果>"
git push origin main
git status --short
```

最後回報固定包含：task ID、修改檔案、官方來源、驗證結果、commit、remote 同步狀態、仍需人工處理事項。
