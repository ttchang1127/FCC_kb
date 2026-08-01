# Gemini 必讀：不要猜，照程序執行

你正在處理 FCC 法律／合規知識庫。錯誤地把未生效條文寫成現行義務，風險高於沒有完成任務。

第一步只執行以下指令：

```bash
python3 scripts/agent_preflight.py
python3 scripts/taskctl.py validate
python3 scripts/taskctl.py next --mode auto
```

然後依序完整閱讀：

1. `AGENTS.md`
2. `TODO.md`
3. `docs/AI_RUNBOOK.md`
4. `docs/LEGAL_STATUS_DECISION_TABLE.md`
5. `tasks/queue.json` 中被選中的單一 task

禁止事項：

- 禁止自行選一批任務一起做。
- 禁止憑摘要或搜尋結果判定法律狀態。
- 禁止把 FCC Order、FNPRM、future amendment 當成已生效 CFR。
- 禁止執行 `--accept-current`，除非 task 明確要求且有人工逐項核准。
- 禁止提交 Obsidian vault、PDF、XML snapshot 或敏感位置。
- 禁止在沒有 full vault 時假造其目錄或卡片。
- 禁止在驗證失敗時宣稱完成。

如果任何資料不明確，輸出 `BLOCKED`、列出缺少的官方證據並停止。完整規則以 `AGENTS.md` 為準。
