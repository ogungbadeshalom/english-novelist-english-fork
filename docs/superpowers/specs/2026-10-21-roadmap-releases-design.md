# 设计：Roadmap 与版本更新日志的承载方式

日期：2026-10-21
状态：已批准（对话确认）

## 背景与问题

README 目前约 300 行，其中「🔄 版本更新」一节占 22 行且只覆盖 v2.0。随着版本迭代：

- 更新日志会随版本累积，README 越来越长；
- Roadmap 尚无承载位置。

主要读者在 GitHub 页面，因此优先使用 GitHub 原生能力。

## 方案（已选定）

采用 **GitHub Releases + 静态 ROADMAP.md**：

- 更新日志 → GitHub Releases（按版本组织、可订阅、侧边栏直达）；
- Roadmap → 仓库根目录 `ROADMAP.md`；
- README 只留链接与一句话指引，净减约 20 行。

备选方案（已否决）：CHANGELOG.md + ROADMAP.md（与 Releases 重复维护）；README 内 `<details>` 折叠（只解决视觉长度，第三方渲染支持不一）。

## 组成部分

### 1. `ROADMAP.md`（新建）

三段式结构：

```
# Roadmap
> 想法和建议欢迎到 Discussions 提 —— 你的反馈直接决定优先级。
## 已完成     — v2.0 要点、v2.x 后续已合并项
## 进行中     — 当前分支工作（占位，由用户填）
## 计划中     — 想法池（占位，由用户填）
```

「进行中/计划中」内容设计阶段无法代拟，实施时留占位并由用户补充。

### 2. README 瘦身

- 删除「🔄 版本更新」整节（L268-289），内容迁移至 Release；
- 原位置替换为约 3 行：更新日志见 Releases · Roadmap 见 ROADMAP.md；
- 顶部 Version badge 改为指向 Releases 列表页（`releases` 而非死链 `releases/tag/v2.0`）；
- 其余各节（赞助商、使用过程、交流、赞助、许可）不动。

### 3. 补建历史 Release

发现 tag v2.0 不存在（本地仅有 v1.0），badge 链接当前是死链。补建：

| Release | tag 位置 | 内容来源 |
|---------|----------|----------|
| v2.0 | `cb1ae70`（PR #11 v2.0 合并提交） | README「版本更新」一节原文 |
| v2.1 | `31d0dc5`（PR #17 v2.1 合并提交） | 从 v2.1 合并的 commit 记录起草 |

之后每次发版流程固定为：打 tag → `gh release create` 写 notes → ROADMAP.md 将对应项移入「已完成」。

### 4. 后续维护

- 发版时写 Release Notes，README 不再累积版本细节；
- ROADMAP.md 的「已完成」与 Release 保持同步，归档即一句话一条。

## 错误处理与验证

纯文档改动，验证方式：

1. 本地确认 README 与 ROADMAP.md 内所有相对/外链可达（尤其 Releases 链接在 tag 推送后才有效，需 push 后复核）；
2. push 后在 GitHub 页面确认 README 渲染、两个 Release 展示正常。

## 约束与风险

- `gh` CLI 不在 PATH 且需开代理（梯子）才能访问 GitHub API；补建 Release 的步骤需在代理可用时执行，实施计划中标注为可延后项。
- tag 一旦推送即对外可见，推送前需与用户确认 tag 位置无误。
