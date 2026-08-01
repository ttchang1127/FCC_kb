# CFR Card Template

複製下列 fenced block 到 full vault 的目標檔案，逐一替換所有 `REPLACE_*`。任何未確認欄位使用 `needs_human_review`，不得刪除欄位掩飾缺漏。

```markdown
---
id: REPLACE_FILENAME_STEM
type: 法規原文卡
title: 47 CFR §REPLACE_SECTION REPLACE_OFFICIAL_TITLE
content_status: verified
legal_status: REPLACE_EFFECTIVE_OR_OTHER_STATUS
created: REPLACE_YYYY-MM-DD
updated: REPLACE_YYYY-MM-DD
authority_level: CFR
agency: FCC
jurisdiction: US
cfr_title: 47
cfr_part: REPLACE_PART
cfr_subpart: REPLACE_SUBPART_OR_REMOVE
section: "REPLACE_SECTION"
effective_on: REPLACE_DATE_OR_NEEDS_HUMAN_REVIEW
ecfr_up_to_date_as_of: REPLACE_DATE
source_checked_at: REPLACE_ISO_DATETIME
official_url: https://www.ecfr.gov/current/title-47/section-REPLACE_SECTION
related: []
tags: [FCC, 47CFR, 海纜]
---

# 47 CFR §REPLACE_SECTION — REPLACE_OFFICIAL_TITLE

## 法律狀態

- 狀態：`REPLACE_STATUS`
- 判定理由：REPLACE_STATUS_REASON
- 資料截至：REPLACE_DATE

## 適用主體

- REPLACE_OR_WRITE_NOT_SPECIFIED

## 觸發事件

- REPLACE_OR_WRITE_NOT_SPECIFIED

## 必須動作

| 動作 | 主體 | 期限 | Paragraph | 申報系統 |
|---|---|---|---|---|
| REPLACE | REPLACE | REPLACE_OR_NOT_SPECIFIED | §REPLACE | REPLACE_OR_NOT_SPECIFIED |

## 例外與限制

- REPLACE_OR_WRITE_NONE_IDENTIFIED

## 設備／設施關聯

- REPLACE_OR_WRITE_NONE_IDENTIFIED

## 紀錄保存

- REPLACE_OR_WRITE_NOT_SPECIFIED

## 未生效／待複核內容

- REPLACE_OR_WRITE_NONE

## 官方來源

- [eCFR §REPLACE_SECTION](https://www.ecfr.gov/current/title-47/section-REPLACE_SECTION)
- REPLACE_RELEVANT_FEDERAL_REGISTER

## 交叉連結

- [[00_Subpart_FF總索引]]
- REPLACE_RELATED_CARDS
```

完成前搜尋：

```bash
rg -n "REPLACE_|needs_human_review" "目標檔案.md"
```
