Go to **Accounting > Configuration > Account Dynamic Rules** to manage your rules.

Example: map the account for a specific supplier automatically
=============================================================

1. Create a rule: **Partner** = `Electricidad El Sol S.L.`
2. Set **Account** = `6280 (Electricity)`
3. Sequence = `10`

Every vendor bill line from that partner will automatically use account
`6280`, no matter what account the import/OCR layer put there.

Example: force taxes by product category
========================================

1. Create a rule: **Product** = the fuel product (empty partner = global)
2. Set **Taxes** = the applicable tax record
3. Sequence = `20`

Lines containing that product get their taxes replaced by the configured
ones — useful when the OCR pipeline reports a tax percentage but you want
the canonical Odoo tax record for that product.

Example: fiscal position by partner
===================================

1. Create a rule: **Partner** = the partner, **Description Match** = `IGIC`
2. Set **Fiscal Position** = `IGIC General (Canarias)`
3. Sequence = `30`

Moves from that partner with "IGIC" in any line description get the
Canary Islands fiscal position applied automatically.
