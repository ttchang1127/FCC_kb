# Legal Status Matrix Template

每一個 amendatory instruction 一列；同一 instruction 修改多個 paragraph 時拆列。

| row_id | order | FR citation | instruction | section | paragraph | action | status | date | delay／effective evidence | official_url | checked_at |
|---|---|---|---:|---|---|---|---|---|---|---|---|
| REPLACE_STABLE_ID | FCC REPLACE | REPLACE FR REPLACE | REPLACE | §REPLACE | REPLACE | add／revise／remove | REPLACE_ALLOWED_STATUS | REPLACE_OR_NULL | REPLACE_EXACT_PARAPHRASE | REPLACE_URL | REPLACE_ISO |

允許的 `status`：

```text
effective
future_effective
delayed_indefinitely
proposed
superseded
reserved
future_placeholder
needs_human_review
```

驗證規則：

- `row_id` 永久穩定，不以日期作唯一識別。
- `status` 必須在允許清單。
- `effective`／`future_effective` 必須有日期。
- `delayed_indefinitely` 的日期必須是 `null`。
- `proposed` 不得出現在現行義務表。
- 每列必須有可直接開啟的官方 URL。
