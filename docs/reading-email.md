# 阅读清单邮件推送

使用 Resend 免费版发送阅读清单，发件地址和收件地址由 GitHub Actions Variables 配置。
现有 GitHub Actions 在工作日北京时间 9:00 启动抓取；网站发布成功后，
将新清单、推荐理由、文章链接及本期归档链接发给指定收件人。
没有新清单或内容与已发布版本一致时跳过。邮件服务若拒绝请求，任务会报错。

## 启用

1. 登录 [Resend](https://resend.com/signup)，添加并验证 `fullstackjam.com`。
2. 按 Resend 提供的值配置发信用的 SPF 和 DKIM DNS 记录。
3. 创建仅有 Sending access、限定该域名的 API key。
4. 在本仓库的 GitHub Actions Secrets 中保存 `RESEND_API_KEY`。
   在 Variables 中配置 `READING_EMAIL_FROM`（发件地址，如 `no-reply@fullstackjam.com`）和
   `READING_EMAIL_TO`（收件地址）。地址可以直接在 Variables 页面查看和修改。
5. 配置完成后先发送一封测试邮件，再核对 Resend 的投递状态及收件箱。

未配置上述 Secret 或 Variables 时，工作流会跳过发信，原有网站更新照常运行。
重建网页不会触发发信；只有实际执行抓取的定时或手动任务才会发送。
Resend 使用同一封邮件内容生成的去重键，在 24 小时内避免重试导致重复发信。
任务重跑时也会将清单与之前发布的版本比较；因此发信失败后如果清单已经发布，
需要单独补发，重建网页不会自动重试邮件。

## 本地预览

先构建网站，再输出 HTML 预览。预览不需要 API key，也不会发信：

```bash
uv run python scripts/build_reading_site.py
uv run python -m scripts.send_reading_email --preview /tmp/reading-email-preview.html
```

个人推送可以通过移除 `READING_EMAIL_TO` Variable 停用。
此配置不提供公开订阅或退订表单；扩展到其他订阅者前需补充订阅管理。
