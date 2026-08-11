# Dynamic Rules for Account

This module provides dynamic rules for mapping accounts, products, payment terms, taxes and fiscal positions on vendor bills.

## Description

Dynamic rules are "invisible" rules for `account.move.line`: they assign accounting account, analytic account, product and payment terms based on configurable rules (partner, product, description with wildcards). Now also supports taxes and fiscal positions.

## Usage

1. Go to Accounting > Configuration > Account Dynamic Rules
2. Create a new rule with match criteria (partner, product, description)
3. Set the desired actions (account, analytic account, product, payment term, taxes, fiscal position)
4. Rules are evaluated by Sequence (lowest first). The first matching rule is applied.
