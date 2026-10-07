#!/usr/bin/env python3
"""Create an OOXML copy with identifying package metadata removed.

Usage: strip_ooxml_metadata.py INPUT OUTPUT
"""
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
import sys
from lxml import etree


def clean_xml(name: str, data: bytes) -> bytes:
    if not (name.endswith('.xml') or name.endswith('.rels')):
        return data
    try:
        root = etree.fromstring(data)
    except Exception:
        return data
    changed = False
    if name in {'docProps/core.xml', 'docProps/app.xml'}:
        for child in list(root):
            root.remove(child)
            changed = True
    for element in root.iter():
        for attr in list(element.attrib):
            if etree.QName(attr).localname.lower() in {
                'author', 'creator', 'lastmodifiedby'
            }:
                element.attrib[attr] = ''
                changed = True
    return (etree.tostring(root, xml_declaration=True, encoding='UTF-8',
                            standalone=True) if changed else data)


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit('usage: strip_ooxml_metadata.py INPUT OUTPUT')
    source, target = map(Path, sys.argv[1:])
    if source.resolve() == target.resolve():
        raise SystemExit('refusing to overwrite the source')
    with ZipFile(source, 'r') as source_zip, ZipFile(
        target, 'w', ZIP_DEFLATED, compresslevel=1
    ) as target_zip:
        for info in source_zip.infolist():
            if info.filename == 'docProps/custom.xml':
                continue
            target_zip.writestr(info, clean_xml(info.filename, source_zip.read(info.filename)))
    print(target)


if __name__ == '__main__':
    main()
