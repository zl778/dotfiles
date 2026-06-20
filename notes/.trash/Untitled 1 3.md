// template.js
const folder = "video/"; // 目标文件夹
const dateStr = new Date().toISOString().split('T')[0]; // 格式：2024-06-01
const title = "新视频笔记"; // 默认标题，可后续修改
const filename = `${dateStr}-${title}.md`.replace(/[^a-zA-Z0-9\u4e00-\u9fa5\-]/g, '-'); // 简单处理非法字符

const fullPath = folder + filename;

// 检查文件是否已存在
if (app.vault.getAbstractFileByPath(fullPath)) {
    new Notice(`文件已存在：${fullPath}，请手动选择其他名称或路径。`);
} else {
    const content = `---
title: ${title}
date: ${new Date().toISOString()}
---

# ${title}

这是通过 Templater 在 video 文件夹下自动生成的笔记。

你可以在这里记录与视频相关的内容，比如：
- 视频链接
- 观看时间
- 笔记内容
- 思考与总结
---

> 创建时间：${new Date().toLocaleString()}
`;

    app.vault.create(fullPath, content);
    new Notice(`✅ 已在 video 文件夹下创建文件：${filename}`);
}