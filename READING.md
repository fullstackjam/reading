# Jam's Reading List

基于 [Horizon](https://github.com/Thysrael/Horizon) 的个人候选阅读清单。
网站：https://reading.fullstackjam.com

## 阅读流程

RSS 候选 → 提取原文 → 按长期阅读价值评分 → 每期最多 5 篇 → 网页推荐 → 手动收进 Notion。
已导入 2026-10-27 的 Feedly OPML：45 条订阅去重为 44 个源，保留 Programming / Life 分组（跨组重复的「胡涂说」归入 Life）。Netflix、Cloudflare、伪架构师和 Scott’s Weblog 使用已验证的现行 Feed 地址。
这是订阅快照，之后在 Feedly 增删订阅不会自动同步；未来文章按运行间隔采集，不会一次回溯所有历史文章。
导入时本机检查：37 个源返回可解析的 Feed；酷壳、Application Security、Uber Engineering Blog（RSSHub）、piglei、plantegg、WY’Blogs、数字移民暂时无法读取，仍保留并启用，后续运行会继续尝试。该结果不保证 GitHub runner 的网络访问情况相同。
公开页面只发布生成的短简介、推荐理由和原文链接，不发布 Notion 收藏或抓取的完整正文。

## 配置

- `data/reading.json`：信源、DeepSeek 模型、数量和分组上限。
- `profiles/reading/`：跨领域、注重长期价值的评分与推荐文案规则。
- `site/style.css`、`scripts/build_reading_site.py`：静态页面。
- `.github/workflows/reading.yml`：北京时间每周一至周五 09:00 执行；不套用节假日或调休表，GitHub 可能延迟调度。
- GitHub Actions Secret `DEEPSEEK_API_KEY`：运行时提供，不能放进配置文件。

`gh-pages` 保存网站和 `summaries/` Markdown 历史；每轮先恢复历史，再生成、构建和发布。
首页显示最新一期，`/archive/` 列出所有往期。上次成功运行时间用于确定下一次采集窗口；没有新文章时正常结束，保留已有清单并更新采集时间。
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
`Finish Pages HTTPS` 是仅手动触发的一次性部署收尾作业，等待证书签发、启用 HTTPS 并检查首页；没有定时触发器，不调用模型。

## 已知边界

Horizon 提取失败时会退回 RSS 内容；本项目用评分规则排除明显残缺的摘要，但尚未增加程序级的正文完整性门禁。
推荐条目会标明网页正文提取、RSS 内容或网页失败后的 RSS 回退，不能把回退内容当作已验证的全文。
长文章输入上限为 100,000 字符，超过上限会取头、中、尾；不能保证每篇逐字阅读全文。
原始文章未来失效时，本站保留的是推荐内容和链接，完整正文归档仍由收录流程负责。
