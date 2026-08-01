# Eva LINE 問題集每日自動發布

## 執行方式

每天 Asia/Taipei 05:00 由 macOS `launchd` 執行：

```text
LINE ingest 日誌
  → 以私人授權清單的 LINE user ID 篩選 Eva Chang
  → 讀取尚未處理的文字訊息
  → 在完整 vault 寫入觸發時間、結果與待處理數
  → 建立獨立 Git worktree
  → codex exec 在 workspace-write sandbox 研究並更新 JSON
  → 驗證公開資料與允許修改的檔案
  → commit／push origin main
  → 成功後才前進私人處理游標
```

VS Code 不必開啟。VS Code 是編輯與人工檢查介面；排程器是 `launchd`，AI 執行介面是 Codex CLI 非互動模式。

## 安全邊界

- 只接受本機 `_fcc-config.json` 中映射為 `EvaChang` 的授權 LINE user ID；顯示名稱不作授權依據。
- LINE 文字只當成待研究資料，不得覆蓋 prompt、AGENTS.md、安全規則或執行 shell 指令。
- Codex 在獨立 worktree 執行，不碰使用者目前的工作樹。
- sandbox 使用 `workspace-write`；只為官方來源研究開啟 outbound network。
- Codex 唯一允許修改的 tracked file 是 `data/eva-questions.json`。
- 外層程式再次檢查 changed files、JSON schema、問題原文、官方來源 URL、私人識別碼及專案驗證。
- 驗證失敗、Git push 失敗或來源不足時，不更新處理游標；下一次排程會重試。
- 公開 repository 不保存 LINE user ID、group ID、token、Codex auth 或 SSH key。
- 每次正常執行都更新 `99_資料治理/Eva_LINE排程執行紀錄.md`；即使待處理數為 0 也寫入 `no_new_questions`。測試與 dry-run 不寫正式紀錄。
- 稽核表只保存台北時間、UTC 日誌時間、觸發方式、結果與數量；不保存 LINE 識別碼或訊息原文。該檔位於被 `.gitignore` 排除的完整 vault，不會公開或觸發每日 Git push。
- 外接磁碟若在 `.git/refs/codex/` 產生名稱為 `Icon` 加控制字元的無效暫存 ref，發布器會精確移至 repo 同層的 `.fcc-kb-invalid-git-refs/` 可復原隔離區，避免背景 `git fetch` 中斷；不移動一般 branch、tag 或 remote ref。

## 本機私有檔案

以下檔案不會推送；前六項位於 Git repository 之外，最後一項位於完整 FCC_kb vault 且受 `.gitignore` 排除：

```text
~/.openclaw/workspace/line-logs/_fcc-config.json
~/.openclaw/workspace/line-logs/_fcc-eva-web-last-processed.txt
~/.openclaw/workspace/line-logs/_fcc-eva-web-update.lock
~/Library/LaunchAgents/tw.jarvis.fcc-eva-web-update.plist
~/.openclaw/logs/fcc-eva-web-update.stdout.log
~/.openclaw/logs/fcc-eva-web-update.stderr.log
<FCC_kb>/99_資料治理/Eva_LINE排程執行紀錄.md
```

## 操作指令

```bash
# 環境、Codex 登入、LINE 設定與待處理數量
node scripts/process_eva_line_questions.mjs --self-test

# 只列出待處理數量與時間，不研究、不寫檔、不 push
node scripts/process_eva_line_questions.mjs --dry-run

# 安裝時將既有、已人工發布的訊息設為基準
node scripts/process_eva_line_questions.mjs --initialize

# 建立暫時 worktree，測試公開資料與驗證閘門後自動清理；不呼叫 AI、不 push
node scripts/process_eva_line_questions.mjs --pipeline-self-test

# 手動執行一次完整流程
node scripts/process_eva_line_questions.mjs

# 查看 launchd 狀態
launchctl print gui/$(id -u)/tw.jarvis.fcc-eva-web-update
```

## 失敗處理

1. 先查看 stderr／stdout log。
2. 確認外接磁碟及 FCC_kb repository 已掛載。
3. 執行 `codex login status`，確認排程使用者仍有登入狀態。
4. 執行 `ssh -T git@github.com`，確認本機 SSH／Keychain 可供背景工作使用。
5. 執行 `--dry-run` 確認問題仍待處理；修正後手動執行一次。

若 Mac 在 05:00 關機，當次工作不會執行；若只是睡眠，`StartCalendarInterval` 通常會在喚醒後補執行。外接磁碟未掛載時流程會安全失敗，不會前進游標。
