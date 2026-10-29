# 阅读清单邮件推送

使用 Resend 免费版发送阅读清单，发件地址和收件地址由 GitHub Actions Variables 配置。
由 cron-job.org 在工作日北京时间 9:00 请求启动 GitHub Actions 抓取；网站发布成功后，
将新清单、推荐理由、文章链接及本期归档链接发给指定收件人。
没有新清单或内容与已发布版本一致时跳过。邮件服务若拒绝请求，任务会报错。

## 推荐规则

阅读价值仍由 AI 按 `profiles/reading/analysis.md` 评分，但分数仅用于排序，
不设最低分门槛，也不按技术、生活等分类限制数量。每次从成功评分的候选文章中
按分数从高到低选择最多 5 篇；不足 5 篇就按实际数量输出。
分析失败、没有有效评分的条目不进入推荐，并保留分析错误日志。
网页抓取失败时，来源行会标注使用 RSS 内容；正文不足以评价时，推荐说明需明确标注
“正文不足，无法可靠评价”，避免将缺失正文误当作文章质量差。

候选时间范围仍为上次运行以来的新文章（首次运行回溯 7 天）。
这不保证每天有 5 篇候选文章，也不会自动补入此前未推荐的旧文章。

## 启用

1. 登录 [Resend](https://resend.com/signup)，添加并验证 `fullstackjam.com`。
2. 按 Resend 提供的值配置发信用的 SPF 和 DKIM DNS 记录。
3. 创建仅有 Sending access、限定该域名的 API key。
4. 在本仓库的 GitHub Actions Secrets 中保存 `RESEND_API_KEY`。
   在 Variables 中配置 `READING_EMAIL_FROM`（发件地址，如 `no-reply@fullstackjam.com`）和
   `READING_EMAIL_TO`（收件地址）。地址可以直接在 Variables 页面查看和修改。
5. 配置完成后先发送一封测试邮件，再核对 Resend 的投递状态及收件箱。

未配置上述 Secret 或 Variables 时，工作流会跳过发信，原有网站更新照常运行。
重建网页不会触发发信；只有实际执行抓取的外部定时触发或手动任务才会发送。
Resend 使用同一封邮件内容生成的去重键，在 24 小时内避免重试导致重复发信。
任务重跑时也会将清单与之前发布的版本比较；因此发信失败后如果清单已经发布，
需要单独补发，重建网页不会自动重试邮件。

需要补发或验证真实投递时，触发工作流并设置 `resend_latest: true`。
此选项会补发最新一期已发布的非空清单，保留原清单日期；`refresh: false` 可跳过重新抓取。
显式补发若缺发信配置会报错；同一次 Actions 运行重试使用相同去重键，新的运行可以再次补发。
正常定时请求省略 `resend_latest`，默认不补发旧清单。

## 定时触发

GitHub 自带的 `schedule` 已移除，定时调度由 cron-job.org 管理。
GitHub Actions 仍负责执行抓取、发布和邮件发送，执行开始时间也受 runner 排队影响。
任务管理：[Reading list · 工作日 09:00](https://console.cron-job.org/jobs/8746111)。

1. 时区：`Asia/Shanghai`；周一至周五 `09:00`（`0 9 * * 1-5`）。
2. 请求：`POST https://api.github.com/repos/fullstackjam/reading/actions/workflows/reading.yml/dispatches`。
3. 请求头：`Accept: application/vnd.github+json`、`Content-Type: application/json`、
   `Authorization: Bearer <dedicated-token>`。
4. 请求体：`{"ref":"main","inputs":{"refresh":true}}`。
5. 专用 fine-grained GitHub token 仅选择 `fullstackjam/reading`，授予 `Actions: Read and write`；
   token 保存在密码库和 cron-job.org 的请求头中，不放进仓库或 URL。

cron-job.org 请求成功仅代表 GitHub 接受了触发请求。生成和发信是否成功，
仍需查看 [Reading list 的运行记录](https://github.com/fullstackjam/reading/actions/workflows/reading.yml)。
当前 token 到期日为 `2027-10-29`；到期前需要在 GitHub 续期并更新 cron-job.org 的请求头。

## 本地预览

先构建网站，再输出 HTML 预览。预览不需要 API key，也不会发信：

```bash
uv run python scripts/build_reading_site.py
uv run python -m scripts.send_reading_email --preview /tmp/reading-email-preview.html
```

个人推送可以通过移除 `READING_EMAIL_TO` Variable 停用。
此配置不提供公开订阅或退订表单；扩展到其他订阅者前需补充订阅管理。
