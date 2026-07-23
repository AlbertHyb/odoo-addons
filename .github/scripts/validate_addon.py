#!/usr/bin/env python3
"""Static validation for Odoo addons without requiring an Odoo DB."""

from pathlib import Path
import ast
import csv
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]


def discover_addons():
    """Discover Odoo addon directories by looking for __manifest__.py."""
    addons = []
    for entry in ROOT.iterdir():
        if entry.is_dir() and (entry / '__manifest__.py').exists():
            addons.append(entry)
    return sorted(addons)


def check_python(addon):
    """Check Python files parse correctly."""
    for path in addon.rglob('*.py'):
        ast.parse(path.read_text(), filename=str(path))


def check_xml(addon):
    """Check XML files parse correctly."""
    for path in addon.rglob('*.xml'):
        ET.parse(path)


def check_access_csv(addon):
    """Check that ir.model.access.csv has all required columns and valid permissions."""
    path = addon / 'security' / 'ir.model.access.csv'
    if not path.exists():
        return
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
                raise AssertionError(
                    f'{path}: {row["id"]} has invalid {column}={row[column]}'
                )


def check_i18n_files(addon):
    """Check i18n PO/POT files are well-formed."""
    i18n_dir = addon / 'i18n'
    if not i18n_dir.exists():
        return
    for path in i18n_dir.glob('*.po'):
        content = path.read_text()
        if 'msgid ""\nmsgstr ""' not in content:
            raise AssertionError(f'{path} is missing a gettext header')
        msgids = content.count('\nmsgid ')
        msgstrs = content.count('\nmsgstr ')
        if msgids != msgstrs:
            raise AssertionError(
                f'{path} has {msgids} msgid entries and {msgstrs} msgstr entries'
            )
    pot = i18n_dir / f'{addon.name}.pot'
    if pot.exists():
        if f'Project-Id-Version: {addon.name}' not in pot.read_text():
            raise AssertionError(f'{pot} does not look like the addon template')


def check_no_forbidden_branding(addon):
    """Check that OCA branding is not present in addon files."""
    forbidden = ''.join(('O', 'C', 'A'))
    for path in addon.rglob('*'):
        if path.is_file() and path.suffix in {'.py', '.xml', '.csv', '.md', '.txt'}:
            if forbidden in path.read_text(errors='ignore'):
                raise AssertionError(
                    f'Forbidden external branding found in {path}'
                )


def main():
    addons = discover_addons()
    if not addons:
        print('No Odoo addons discovered')
        return

    for addon in addons:
        check_python(addon)
        check_xml(addon)
        check_access_csv(addon)
        check_i18n_files(addon)
        check_no_forbidden_branding(addon)
        print(f'{addon.name} static validation passed')


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f'validation failed: {exc}', file=sys.stderr)
        raise
