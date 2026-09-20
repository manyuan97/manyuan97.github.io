# Manyuan Zhang · Personal homepage

简洁的静态学术主页，借鉴 Jon Barron、Hao Shao 和 Xudong Lu 的主页风格。直接部署到 GitHub Pages，无需 Node.js 或前端框架。

## 修改内容

- `template.html`：个人简介、联系方式、经历、页面结构。
- `content.json`：完整论文列表、新闻、奖项和项目。
- `style.css`：字体、颜色、布局和移动端样式。
- `script.js`：论文筛选。
- `assets/papers/`：精选论文插图；来源见该目录的 `SOURCES.md`。
- `assets/fonts/`：本地 Lato 字体及其 OFL 许可证。

每篇论文的 `selected` 决定是否默认显示，`selected_order` 控制精选顺序。`image` 和 `summary` 可选；所有论文都可通过 All 或年份筛选查看。`authors_html` 支持加粗姓名和贡献标记。`tech_reports` 使用论文 `id` 引用 Tech Report & Projects 区块中的条目；这些条目不会重复出现在 Research 列表中。Research 支持 All、2026、2025、Earlier 四种筛选。新增论文时请使用唯一的 `id`。

`content.json` 中的 HTML 字段仅用于网站作者维护的可信内容，不接收用户输入。

## 构建与预览

```sh
./build.sh
python3 -m http.server 8000 --bind 127.0.0.1
```

打开 http://localhost:8000 。构建只依赖 Python 3 标准库；生成的 `index.html` 需要和 CSS、JavaScript、图片、字体一起提交。GitHub Pages 直接提供生成后的静态文件，不需要在服务端执行 Python。禁用 JavaScript 时，全部论文仍可阅读。

`index.jemdoc`、`jemdoc.py`、`jemdoc.css` 和 `MENU` 是旧版留档；新版以 `template.html` 和 `content.json` 为内容源，请勿再用 jemdoc 覆盖 `index.html`。

## 迁移说明

内容来自迁移时的 `index.html`，保留 47 篇论文、32 条新闻、5 项挑战赛奖项和 2 个项目。个人经历结合已有 `cv.tex` 整理。CV 文件保持原样。

迁移时修正了拼写和明显的链接格式错误；另根据论文原始来源修正：

- [Deep Reward Supervisions](https://arxiv.org/abs/2405.00760) 的论文链接（旧版误指向 Motion-I2V）。
- [FlowFormer++](https://openaccess.thecvf.com/content/CVPR2023/html/Shi_FlowFormer_Masked_Cost_Volume_Autoencoding_for_Pretraining_Optical_Flow_Estimation_CVPR_2023_paper.html) 的标题与会议年份（CVPR 2023）。

旧版 Large-scale Masked Face Recognition 的链接为无效的 `Towards`，已保留论文文字并移除该链接。原有 MapMyVisitors 统计继续加载，地图可在页脚的 Visitors 中展开。
