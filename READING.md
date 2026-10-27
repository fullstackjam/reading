# Jam's Reading List

基于 [Horizon](https://github.com/Thysrael/Horizon) 的个人候选阅读清单。
网站：https://reading.fullstackjam.com

## 阅读流程

RSS 候选 → 提取原文 → 按长期阅读价值评分 → 每期最多 5 篇 → 网页推荐 → 手动收进 Notion。
初始信源来自现有 Feedly 截图中的六个订阅；尚未导入完整订阅列表。
公开页面只发布生成的短简介、推荐理由和原文链接，不发布 Notion 收藏或抓取的完整正文。

## 配置

- `data/reading.json`：信源、DeepSeek 模型、数量和分组上限。
- `profiles/reading/`：跨领域、注重长期价值的评分与推荐文案规则。
- `site/style.css`、`scripts/build_reading_site.py`：静态页面。
- `.github/workflows/reading.yml`：北京时间周二、周五 08:17 执行；GitHub 可能延迟调度。
- GitHub Actions Secret `DEEPSEEK_API_KEY`：运行时提供，不能放进配置文件。

`gh-pages` 保存网站和 `summaries/` Markdown 历史；每轮先恢复历史，再生成、构建和发布。
首页显示最新一期，`/archive/` 列出所有往期。上次成功运行时间用于确定下一次采集窗口。
同一天重新生成会更新当天一期，所有版本仍可在 Git 历史中找回。

## 本地运行

```bash
uv sync --extra dev
# Set DEEPSEEK_API_KEY in the process environment.
uv run horizon --config data/reading.json --hours 168
uv run python scripts/build_reading_site.py
uv run python -m http.server 8765 --directory public
```

在 Actions 页面手动运行 `Reading list`，`refresh=true` 重新采集推荐，`false` 只重新发布网页。
调整样式后 push `main` 只构建网页，不调用模型。

## 已知边界

Horizon 提取失败时会退回 RSS 内容；本项目用评分规则排除明显残缺的摘要，但尚未增加程序级的正文完整性门禁。
长文章输入上限为 100,000 字符，超过上限会取头、中、尾；不能保证每篇逐字阅读全文。
原始文章未来失效时，本站保留的是推荐内容和链接，完整正文归档仍由收录流程负责。
