# submissions/TOSEM/templates/ — ACM TOSEM 官方模板

## 来源

| 文件 | 来源 | 描述 |
|---|---|---|
| `acmsmall-submission.tex` | acmart 2.18 包 `samples/` 子目录（CTAN） | 官方 TOSEM **投稿评审版**模板（`[acmsmall,screen,anonymous,review]`） |
| `acmsmall.tex` | acmart 2.18 包 `samples/` 子目录（CTAN） | 官方 TOSEM **journal regular** 模板（`[acmsmall]`） |
| `acmart.pdf` | acmart 2.18 包根目录（CTAN） | acmart 类完整用户文档（959 KB） |
| `acmguide.pdf` | acmart 2.18 包根目录（CTAN） | acmart 简明用户指南（438 KB） |
| `sample-base.bib` | acmart 2.18 包 `samples/` 子目录（CTAN） | ACM-Reference-Format 示例 bib |

**正本分发**：CTAN — <https://mirrors.ctan.org/macros/latex/contrib/acmart.zip>
**维护人**：Boris Veytsman（ACM 雇佣）
**License**：LPPL 1.3 · Copyright 2016–2025 ACM
**当前版本**：acmart **2.18 (2026-05-31)**

## 与本项目投稿稿的对照

本项目 [`NOETHER_paper_submission.tex`](../NOETHER_paper_submission.tex) 的 `\documentclass` 选项：

```latex
\documentclass[acmsmall,review,anonymous]{acmart}
```

官方 `acmsmall-submission.tex` 的 `\documentclass` 选项：

```latex
\documentclass[acmsmall,screen,anonymous,review]{acmart}
```

**差异**：

- 缺 `screen` 选项 — sRGB + 屏字体，便于 reviewer 屏上读。非必须，加 0 风险，与官方对齐。可在下一轮 polish 加。
- 顺序 `review,anonymous` vs `anonymous,review` — 选项顺序无关，无差。

## 同步官方更新

ACM 通过 CTAN + GitHub 同步发布 acmart。同步本目录命令：

```bash
cd submissions/TOSEM/templates
curl -sL -o /tmp/acmart.zip https://mirrors.ctan.org/macros/latex/contrib/acmart.zip
unzip -q /tmp/acmart.zip -d /tmp/
cd /tmp/acmart/samples && pdflatex samples.ins   # docstrip 生成 sample-*.tex
cp /tmp/acmart/samples/acmsmall{,-submission}.tex \
   /tmp/acmart/samples/sample-base.bib \
   /tmp/acmart/acmart.pdf \
   /tmp/acmart/acmguide.pdf \
   .
rm -rf /tmp/acmart /tmp/acmart.zip
```

CTAN 提供 acmart 包元数据页：<https://www.ctan.org/pkg/acmart>。
GitHub 开发版（**不要**用作生产模板）：<https://github.com/borisveytsman/acmart>。

## 不入 git 的派生物

`acmart.zip` 解压临时目录已删；本目录只保留长期稳定的官方 sample/doc 文件。
