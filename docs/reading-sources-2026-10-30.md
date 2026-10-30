# Scour Discover 原始站点导入（2026-10-30）

来源：[Scour Discover](https://scour.ing/discover)。按本次读取时首页展示的 20 个原始站点核对；页面会动态变化，本次导入不自动跟踪其后续站点变动。

## 已加入的 15 个 RSS / Atom 源

| 站点 | 订阅地址 |
|---|---|
| Dheeraj Akula | https://dheerajakula.dev/rss.xml |
| It's FOSS | https://itsfoss.com/rss/ |
| Dan Luu | https://danluu.com/atom.xml |
| Xiangpeng's blog | https://blog.xiangpeng.systems/index.xml |
| CSO Online | https://www.csoonline.com/feed/ |
| Don't Worry About the Vase | https://thezvi.substack.com/feed |
| Tildes | https://tildes.net/topics.rss |
| Chromatic Club | https://www.chromatic-club.com/blog-feed.xml |
| Nelson Figueroa | https://nelson.cloud/index.xml |
| Tigris Object Storage Blog | https://www.tigrisdata.com/blog/rss.xml |
| turbopuffer Blog | https://turbopuffer.com/blog/rss.xml |
| Noted | https://noted.lol/rss/ |
| Words by Kesling | https://kesling.substack.com/feed |
| Nemo's Home | https://captnemo.in/atom.xml |
| arXiv — cs.CL | https://rss.arxiv.org/rss/cs.CL |

arXiv 按已确认的 cs.CL（计算与语言）分类订阅；RSS 主要提供摘要，现有流程不保证获得论文全文。

## 未加入的 5 个站点

已按你的确认暂不接入这五个站点。

| 站点 | 原因 |
|---|---|
| Every / Context Window | 原站未发现可用公开订阅地址；已核对的 Napkin Math 地址返回 404。官方帮助说明提供付费账户的个人 RSS，需要自己的授权订阅地址。 |
| Tiny Little Office | 当前是产品页面，未发现 RSS / Atom。 |
| Uncommon we:b（webdev.teknium.io） | 当前是资源目录，未发现 RSS / Atom。 |
| XDA | 原站公布 https://www.xda-developers.com/feed/，本次两次请求均遇到协议错误，未纳入定时抓取。 |
| Inside Atlassian | 浏览器 User-Agent 可读取公开 RSS，但 Horizon 实际请求重定向后返回 403；另一个公开 feed 地址不是有效 RSS / Atom，未纳入。 |

## 验证范围

原有 37 个源和推荐排序配置保留；本次加入后共 52 个源。
15 个新增站点均通过本机 Horizon 原生抓取器验证；arXiv cs.CL 此次返回格式有效、暂无条目的 RSS。
本次验证只读取公开页面和订阅内容，不调用模型生成推荐，也不发送邮件。
