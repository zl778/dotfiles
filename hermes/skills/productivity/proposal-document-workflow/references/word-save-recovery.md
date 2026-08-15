# Word save-disappearance recovery notes

## Verified macOS/OneDrive sequence

1. Search the project tree for the original filename, `副本`, `副本2`, `~$*`, `~WRF*`, and `~WRS*`; sort by mtime and size.
2. Reopen each `.docx` with `python-docx` and record paragraph/table counts plus distinctive added headings. Compare the original with candidates before relying on checksums.
3. Compare MD5 values. In the observed case, the original invitation was 30,426 bytes with 36 paragraphs/3 tables; the edited copy was 37,995 bytes with 55 paragraphs/6 tables. `副本` and `副本2` were identical to each other, but both differed from the original.
4. Check Word container locations:
   - `~/Library/Containers/com.microsoft.Word/Data/Library/Preferences/AutoRecovery/`
   - `~/Library/Containers/com.microsoft.Word/Data/tmp/`
   - `~/Library/Containers/com.microsoft.Word/Data/Library/Application Support/Microsoft/Temp/`
   - `~/Library/Containers/com.microsoft.Word/Data/Library/Application Support/Microsoft/Office/16.0/OfficeFileCache/`
5. Check Word MRU JSON: `~/Library/Containers/com.microsoft.Word/Data/Library/Application Support/Microsoft/Office/16.0/aggmru/*/w-mru4-zh-CN-sr.json`. Parse `title`, `url`, `breadcrumbs`, `time_stamp`, `file_size`, and `modification_info` for the target title. OneDrive MRU entries may expose a `d.docs.live.net` URL even when the user is looking only at the local folder.
6. Check `.Trash` and both OneDrive trees. Prefer the user-facing `~/Library/CloudStorage/OneDrive-个人/` path after verifying duplicates.
7. For a verified candidate, make a sibling copy such as `*_已编辑恢复版.docx`; verify copy equality with `md5 -q` and reopen with `python-docx`.

## Temporary-file caution

A non-empty `~WRF*` file is only a candidate. In the observed case, a 360 KB `~WRF{...}` file was identified as a compound document but was not loadable by `textutil` or LibreOffice and contained no recognizable target Chinese text. Do not call such a file recovered without a successful parse or a verified Office conversion.

## Reporting contract

Report the exact recovered path, original-versus-candidate structural evidence, checksum of the recovery copy, and whether temporary/OneDrive candidates were parseable. Never delete source, duplicate, or temporary candidates during discovery.
