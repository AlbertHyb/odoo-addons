#!/usr/bin/env python3
"""Static validation for the Odoo Agent addon without requiring an Odoo DB."""

from pathlib import Path
import ast
import csv
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
ADDON = ROOT / 'odoo_agent'


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
    pot = i18n_dir / 'odoo_agent.pot'
    if pot.exists() and 'Project-Id-Version: odoo_agent 18.0' not in pot.read_text():
        raise AssertionError(f'{pot} does not look like the addon template')


def check_no_forbidden_branding():
    forbidden = ''.join(('O', 'C', 'A'))
    for path in ADDON.rglob('*'):
        if path.is_file() and path.suffix in {'.py', '.xml', '.csv', '.md', '.txt'}:
            if forbidden in path.read_text(errors='ignore'):
                raise AssertionError(f'Forbidden external branding found in {path}')


def main():
    check_python()
    check_xml()
    check_access_csv()
    check_i18n_files()
    check_no_forbidden_branding()
    print('odoo_agent static validation passed')


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f'validation failed: {exc}', file=sys.stderr)
        raise
