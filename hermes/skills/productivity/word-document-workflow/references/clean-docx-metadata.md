# 清理 docx 文件图元信息（元数据）

当需要去除 Word 文档中的作者、公司、最后修改者、修订编号等隐藏元数据时使用。

## 方法

使用 `python-docx` + `zipfile` + `lxml` 直接修改 docx 包内的 XML 文件。

## 完整脚本

```python
import datetime, zipfile, os, tempfile
from docx import Document
from lxml import etree

src = '输入文件.docx'
dst = '输出文件.docx'  # 可以覆盖原文件

# 1. 清理 CoreProperties（作者、标题、修订等）
doc = Document(src)
cp = doc.core_properties
for attr in ['author', 'title', 'subject', 'keywords', 'category', 'comments',
             'last_modified_by', 'last_printed']:
    try:
        setattr(cp, attr, '')
    except:
        pass
try:
    cp.revision = 1
except:
    pass
now = datetime.datetime.now()
try:
    cp.created = now
    cp.modified = now
except:
    pass

# 2. 保存到临时文件，获得更新后的 package
tmp_src = src + '.tmp_save'
doc.save(tmp_src)

# 3. 直接修改 zip 包中的 XML
tmp_dst = dst + '.tmp'
with zipfile.ZipFile(tmp_src, 'r') as zin:
    with zipfile.ZipFile(tmp_dst, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == 'docProps/core.xml':
                root = etree.fromstring(data)
                # 删除所有核心元数据标签
                tags_to_clear = [
                    '{http://purl.org/dc/elements/1.1/}creator',
                    '{http://purl.org/dc/elements/1.1/}title',
                    '{http://purl.org/dc/elements/1.1/}subject',
                    '{http://purl.org/dc/elements/1.1/}description',
                    '{http://schemas.openxmlformats.org/package/2006/metadata/core-properties}keywords',
                    '{http://schemas.openxmlformats.org/package/2006/metadata/core-properties}category',
                    '{http://schemas.openxmlformats.org/package/2006/metadata/core-properties}lastModifiedBy',
                    '{http://schemas.openxmlformats.org/package/2006/metadata/core-properties}lastPrinted',
                    '{http://schemas.openxmlformats.org/package/2006/metadata/core-properties}revision',
                ]
                for tag in tags_to_clear:
                    for el in root.iter(tag):
                        parent = el.getparent()
                        if parent is not None:
                            parent.remove(el)
                data = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
                zout.writestr(item, data)
            elif item.filename == 'docProps/app.xml':
                root = etree.fromstring(data)
                ns = 'http://schemas.openxmlformats.org/officeDocument/2006/extended-properties'
                for tag in ['{%s}Manager' % ns, '{%s}Company' % ns]:
                    for el in root.iter(tag):
                        if el.text:
                            el.text = ''
                data = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
                zout.writestr(item, data)
            else:
                zout.writestr(item, data)

os.replace(tmp_dst, dst)
os.remove(tmp_src)

print(f'元数据已清理完成: {dst}')
```

## 常见元数据标签

| 标签 | 所在 XML 文件 | 作用 |
|------|---------------|------|
| `dc:creator` | docProps/core.xml | 作者 |
| `cp:lastModifiedBy` | docProps/core.xml | 最后修改者 |
| `cp:revision` | docProps/core.xml | 修订版本号 |
| `dc:title` | docProps/core.xml | 文档标题 |
| `cp:keywords` | docProps/core.xml | 关键词 |
| `cp:category` | docProps/core.xml | 类别 |
| `dc:description` | docProps/core.xml | 备注/描述 |
| `cp:lastPrinted` | docProps/core.xml | 上次打印时间 |
| `Manager` | docProps/app.xml | 经理（企业信息） |
| `Company` | docProps/app.xml | 公司名称 |

## 验证清理结果

```python
from docx import Document
doc = Document('已清理.docx')
cp = doc.core_properties
print('Author:', repr(cp.author))
print('Last modified by:', repr(cp.last_modified_by))
print('Revision:', cp.revision)
```

## 注意事项

- 使用 `zipfile` 直接修改而不是 `python-docx` 的 `save()`，因为后者可能无法清除 app.xml 中的 Company 等字段
- 先通过 `doc.save()` 获取更新后的 core.xml，再通过 zipfile 清理，两步是必要的
- 如果 docx 文件较大，操作速度仍然很快（非解压全部，只是流式处理）
