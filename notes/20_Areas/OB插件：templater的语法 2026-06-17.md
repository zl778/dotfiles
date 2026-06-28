#a/learning/software

**常用语法**

## **1. 文件信息 `tp.file`**

```
<% tp.file.title %>
```

当前文件名。

```
<% tp.file.path(true) %>
```

当前文件完整路径。

```
<% tp.file.folder(true) %>
```

当前文件所在文件夹。

```
<% tp.file.creation_date("YYYY-MM-DD HH:mm") %>
```

创建时间。

```
<% tp.file.last_modified_date("YYYY-MM-DD HH:mm") %>
```

最后修改时间。

```
<% await tp.file.rename("新文件名") %>
```

重命名当前笔记。

```
<% await tp.file.move("/journals/" + tp.file.title) %>
```

移动当前笔记到指定文件夹。

## **2. 日期时间 `tp.date`**

```
<% tp.date.now("YYYY-MM-DD") %>
```

今天日期。

```
<% tp.date.now("YYYY年MM月DD日 dddd") %>
```

中文风格日期加星期。

```
<% tp.date.tomorrow("YYYY-MM-DD") %>
```

明天。

```
<% tp.date.yesterday("YYYY-MM-DD") %>
```

昨天。

```
<% tp.date.now("YYYY-MM-DD", 7) %>
```

7 天后。

```
<% tp.date.now("YYYY-MM-DD", -7) %>
```

7 天前。

## **3. 用户输入 `tp.system`**

```
<% tp.system.prompt("请输入标题") %>
```

弹窗输入文字。

```
<% tp.system.prompt("请输入作者", "默认作者") %>
```

带默认值。

```
<% tp.system.suggester(["读书", "视频", "软件"], ["读书", "视频", "软件"]) %>
```

弹出选择菜单。

```
<% tp.system.suggester(
  ["未开始", "进行中", "已完成"],
  ["to-do", "doing", "done"]
) %>
```

显示中文，实际插入英文值。

## **4. 光标位置**

```
<% tp.file.cursor() %>
```

模板插入后，光标停在这里。

多个光标：

```
<% tp.file.cursor(1) %>
<% tp.file.cursor(2) %>
```

## **5. 插入另一个模板**

```
<% tp.file.include("[[模板名]]") %>
```

比如：

```
<% tp.file.include("[[Template/基础信息]]") %>
```

## **6. 条件判断**

```
<%*
let type = await tp.system.suggester(["读书", "视频", "软件"], ["book", "video", "software"]);

if (type === "book") {
  tR += "## 作者\n\n## 读书摘录\n";
} else if (type === "video") {
  tR += "## 视频链接\n\n## 视频总结\n";
} else {
  tR += "## 软件用途\n\n## 配置记录\n";
}
%>
```

## **7. 变量写法**

```
<%*
let author = await tp.system.prompt("输入作者");
let status = await tp.system.suggester(["待读", "在读", "读完"], ["to-read", "reading", "done"]);

tR += `作者：${author}\n`;
tR += `状态：${status}\n`;
%>
```

## **8. YAML 属性模板**

```
---
title: <% tp.file.title %>
created: <% tp.date.now("YYYY-MM-DD HH:mm") %>
tags:
  - 学习
status: <% await tp.system.suggester(["to-read","reading","done"], ["to-read","reading","done"]) %>
author: <% await tp.system.prompt("输入作者") %>
---
```

## **9. 日记模板示例**

```
---
created: <% tp.date.now("YYYY-MM-DD HH:mm") %>
tags:
  - 日志
---

# <% tp.date.now("YYYY-MM-DD dddd") %>

## 今日记录

<% tp.file.cursor() %>

## 待办

- [ ] 

## 总结
```

## **10. 插件记录模板示例**

```
---
created: <% tp.date.now("YYYY-MM-DD") %>
tags:
  - 软件
  - Obsidian
status: <% await tp.system.suggester(["想试", "使用中", "弃用"], ["to-try", "using", "abandoned"]) %>
---

# <% tp.file.title %>

## 插件用途

## 适合场景

## 常用命令

## 我的设置

## 注意事项

<% tp.file.cursor() %>
```

你现在最值得先记住这几个：`tp.file.title`、`tp.date.now()`、`tp.system.prompt()`、`tp.system.suggester()`、`tp.file.cursor()`。这几个已经能做出非常实用的日记、视频笔记、插件记录、读书笔记模板了。