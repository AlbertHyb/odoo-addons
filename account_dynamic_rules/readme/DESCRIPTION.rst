=====================
Account Dynamic Rules
=====================

Automatic, configurable mapping rules for vendor bills (purchase invoices).
When a bill line is created, the module evaluates a set of admin-defined
rules and applies account, analytic account, product, payment term, taxes
or fiscal position automatically — no code changes, no hardcoded values.

The module is designed to be the **decision layer** for AI/OCR invoice
pipelines: the vision/LLM layer only *reads* the invoice ("there is a 7%
tax called IGIC"), and this module decides what account/product/tax to use
based on the business configuration.

Installation
============

Add the module to your addons path and install it in the Odoo UI
(Apps > Update Apps List > Install "Account Dynamic Rules").

Configuration
=============

Go to **Accounting > Configuration > Account Dynamic Rules** to manage rules.

Each rule has:

Match criteria (when it applies)
-------------------------------

* **Partner** — rule applies to this partner only (empty = global)
* **Product** — rule applies to lines with this product only (empty = global)
* **Payment Mode** — rule applies to moves using this payment mode (empty = global)
* **Description Match** — line description must *contain* this text
  (case-insensitive; empty = any description)

Actions (what it changes)
-------------------------

* **Account** — force the accounting account on the line
* **Analytic Account** — force the analytic account on the line
* **Force Product** — replace the product on the line
* **Payment Term** — set the payment term on the parent move
* **Taxes** — replace the line taxes (many2many)
* **Fiscal Position** — set the fiscal position on the parent move

Rules are ordered by **sequence**; the first matching rule wins
(highest priority = lowest sequence).

Usage
=====

1. Define your rules in Accounting > Configuration > Account Dynamic Rules.
2. Create or import a vendor bill (manually, via API/n8n, or via the
   OdooClaw OCR pipeline).
3. On every line creation, the module:
   a. Skips lines that are not part of purchase invoices/refunds
      (sales, receipts, sections/notes, generated tax lines, AP/AR lines).
   b. Searches rules matching the line's partner + product + payment mode
      (+ description if set), ordered by sequence.
   c. Applies the first matching rule's actions and stops.

The module also completes vendor bill headers on creation (API/import
path): partner payment term, supplier payment mode and vendor bank account
— so imported bills arrive fully configured without manual editing.

Integration with OdooClaw OCR pipeline
======================================

The 4-layer invoice pipeline (vision -> fiscal -> header -> validation)
extracts: ``partner``, ``invoice_date``, ``ref``, ``amount_total``,
``amount_tax`` and per-tax-rate lines (``base``, ``tax_percentage``,
``tax_amount``). It deliberately does **not** hardcode accounts or taxes:
the fiscal layer only reads "7% tax called IGIC" from the document.

Then the bill is created in Odoo and **this module decides**:

* Which account/product to use per line (rule by partner/product/description)
* Which taxes to force (rule.tax_ids)
* Which fiscal position applies to the move (rule.fiscal_position_id)

This keeps the AI model-agnostic (any vision model works) and the
accounting logic configurable by the admin without code.

Known limitations
=================

* Rules apply only on **line creation** (account.move.line.create). Lines
  modified afterwards are not re-evaluated.
* First-match-wins: if several rules match, only the one with lowest
  sequence is applied.
* Generated tax lines and AP/AR (payable/receivable) lines are never
  touched — tax repartition accounts always win there.

Bug Tracker
===========

Bugs are tracked on GitHub Issues. In case of trouble, please check there
if your issue has already been reported.

Credits
=======

Author: Nicolás Ramos <contacto@nicolasramos.es>

License
=======

AGPL-3.0 or later.
