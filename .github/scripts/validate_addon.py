#!/usr/bin/env python3
"""Static validation for the Mail Bot OdooClaw addon without requiring an Odoo DB."""

from pathlib import Path
import ast
import csv
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
ADDON = ROOT / 'mail_bot_odooclaw'


def check_python():
    for path in ADDON.rglob('*.py'):
        ast.parse(path.read_text(), filename=str(path))


def check_xml():
    for path in ADDON.rglob('*.xml'):
        ET.parse(path)


def check_access_csv():
    path = ADDON / 'security' / 'ir.model.access.csv'
    with path.open(newline='') as csvfile:
        rows = list(csv.DictReader(csvfile))
    required = {
        'id', 'name', 'model_id:id', 'group_id:id',
        'perm_read', 'perm_write', 'perm_create', 'perm_unlink',
    }
    missing = required - set(rows[0])
    if missing:
        raise AssertionError(f'{path} missing columns: {sorted(missing)}')
    for row in rows:
        for column in ('perm_read', 'perm_write', 'perm_create', 'perm_unlink'):
            if row[column] not in {'0', '1'}:
                raise AssertionError(f'{path}: {row["id"]} has invalid {column}={row[column]}')


def check_i18n_files():
    i18n_dir = ADDON / 'i18n'
    if not i18n_dir.exists():
        return
    for path in i18n_dir.glob('*.po'):
        content = path.read_text()
        if 'msgid ""\nmsgstr ""' not in content:
            raise AssertionError(f'{path} is missing a gettext header')
        msgids = content.count('\nmsgid ')
        msgstrs = content.count('\nmsgstr ')
        if msgids != msgstrs:
            raise AssertionError(f'{path} has {msgids} msgid entries and {msgstrs} msgstr entries')


def main():
    check_python()
    check_xml()
    check_access_csv()
    check_i18n_files()
    print('mail_bot_odooclaw static validation passed')


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f'validation failed: {exc}', file=sys.stderr)
        raise
