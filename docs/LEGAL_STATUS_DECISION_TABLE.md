# 法律狀態決策表

AI 只能依下表分類。找不到相符證據時使用 `needs_human_review`。

| 狀態 | 必要官方證據 | 可以寫 | 禁止寫 |
|---|---|---|---|
| `effective` | CFR 現行文字，且相關生效條件已滿足 | 現行義務、生效日、適用範圍 | 不能把 future amendment 一併視為有效 |
| `future_effective` | Final rule 已發布且有明確未來生效日 | 預定生效日、未來要求 | 不能寫成目前必須遵守 |
| `delayed_indefinitely` | Federal Register 明列 instruction 延後 | 延後範圍、等待後續公告 | 不能自行推算生效日 |
| `proposed` | NPRM／FNPRM／proposed rule | 提案內容、comment deadline | 不能稱 final rule 或現行義務 |
| `superseded` | Section 被移除／取代且有官方 amendment record | 最後有效日、歷史用途、現行對應 | 不能繼續作為現行主依據 |
| `reserved` | eCFR 顯示 `[Reserved]` | 保留狀態 | 不能填入推測內容 |
| `future_placeholder` | eCFR 顯示 `xxx`、空段落或 future marker | placeholder 與等待事項 | 不能整理成完整條文 |
| `needs_human_review` | 官方資料衝突、不完整或無法確定 | 缺少證據、待確認問題 | 不能選最可能答案 |

## 固定判定順序

```text
1. 文件是 proposed 還是 final？
2. Final rule 的 DATES 段說什麼？
3. 該 amendatory instruction 是否被 delayed？
4. 是否另有 effective-date／OMB notice？
5. eCFR 目前文字是否已編入？
6. 個別 paragraph 是否仍有 placeholder？
7. 結論與資料日期一起記錄。
```

## 衝突處理

- FCC 新聞稿與 Federal Register 衝突：採 Federal Register／正式命令，標示需複核。
- FCC Guide 仍引用舊條號：保留歷史引用，另查現行 CFR。
- eCFR 已顯示 future amendment，但 FR 說 delayed：狀態為 `delayed_indefinitely`。
- Order 描述預期義務，但 CFR 未生效：不得標 `effective`。
- 自動 feed hash 改變：只代表文字變動，狀態先設 `needs_human_review`。

## 每個法律結論的最低證據欄位

```text
source_type
official_url
citation
document_number_or_section
publication_or_as_of_date
effective_date_or_delay_text
paragraph_or_instruction
checked_at
status
status_reason
```
