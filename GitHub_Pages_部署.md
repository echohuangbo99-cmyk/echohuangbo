# 快速部署到 GitHub Pages（完全免费！）

> 无需服务器，无需付费，只需要 GitHub 账户

## 📋 五步完成部署

### Step 1: 创建 GitHub 仓库

1. 访问 https://github.com/new
2. 仓库名填写：`objection-assistant`
3. 选择 "Public"（公开，这样任何人都可以访问）
4. 点击 "Create repository"

### Step 2: 上传文件

**方式 A：使用 Git 命令行（推荐）**

```bash
# 进入项目目录
cd /Users/bobo/WorkBuddy/20260331155330

# 初始化 Git
git init
git add .
git commit -m "Initial commit: 松鼠AI异议查询助手"

# 关联远程仓库（替换 your-username）
git remote add origin https://github.com/your-username/objection-assistant.git
git branch -M main
git push -u origin main
```

**方式 B：使用 GitHub 网页界面**

1. 打开刚才创建的仓库
2. 点击 "Upload files"
3. 拖拽所有文件到上传框：
   - `index.html` （静态版本）
   - `objections_db.json` （异议数据）
   - `README.md` （说明文档）
4. 点击 "Commit changes"

### Step 3: 启用 GitHub Pages

1. 进入仓库 → Settings（设置）
2. 左侧选择 "Pages"
3. 在 "Build and deployment" 中：
   - Branch 选择：`main`
   - Folder 选择：`/ (root)`
4. 点击 "Save"

### Step 4: 获取公网地址

GitHub 会自动生成一个访问地址，格式为：
```
https://your-username.github.io/objection-assistant
```

等待 2-3 分钟，然后访问这个 URL！

### Step 5: 分享链接

现在你可以把这个链接分享给所有销售团队成员，他们都可以在线访问：

```
📱 在线版本：https://your-username.github.io/objection-assistant

扫描 QR 码或复制链接，随时随地查询异议处理话术！
```

---

## 🚀 其他免费托管方案

| 平台 | 优点 | 缺点 | 部署时间 |
|------|------|------|--------|
| **GitHub Pages** | 完全免费，无限使用 | 静态网站，无后端 | 2-3 分钟 |
| **Vercel** | 部署超快，自动优化 | 需要信用卡（免费额度） | 1 分钟 |
| **Netlify** | 免费额度充足 | 有流量限制 | 1 分钟 |
| **Render** | 支持动态后端 | 免费服务器较慢 | 5 分钟 |

### 选择建议：
- 🥇 **首选**: GitHub Pages（完全免费，无任何限制）
- 🥈 **备选**: Vercel（部署速度最快）
- 🥉 **功能丰富**: Render（支持 Python 后端）

---

## 💡 更新异议数据

当你在本地更新了 `objections_db.json` 后，只需要重新推送到 GitHub：

```bash
# 1. 更新本地数据
# （编辑 objections_db.json）

# 2. 提交并推送
git add objections_db.json
git commit -m "更新异议数据库"
git push

# 3. GitHub Pages 会自动更新网站（2-3 分钟内生效）
```

---

## 🔧 高级配置

### 自定义域名

如果你有自己的域名，可以将其指向 GitHub Pages：

1. 在 GitHub Settings → Pages → Custom domain 输入你的域名
2. 在你的域名提供商那里添加 CNAME 记录指向 GitHub

例如：
```
objection.yourcompany.com → your-username.github.io
```

### 启用 HTTPS

GitHub Pages 默认提供 HTTPS 支持，完全安全。

### 添加分析

在 `index.html` 中加入 Google Analytics：

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

---

## 📊 如何监控访问

### 方式 1: GitHub 流量分析
进入仓库 → Insights → Traffic 可以看到访问统计

### 方式 2: Google Analytics
1. 在 `index.html` 中添加 GA 追踪代码
2. 访问 Google Analytics 查看实时流量

### 方式 3: 简单计数器
在 HTML 中添加访问计数（可用第三方服务）

---

## 🎯 完整流程总结

```
1. 创建 GitHub 仓库
   ↓
2. 上传项目文件
   ↓
3. 启用 GitHub Pages
   ↓
4. 等待 2-3 分钟
   ↓
5. 访问 https://your-username.github.io/objection-assistant
   ↓
6. 分享链接给团队
   ↓
✅ 完成！所有人都可以在线访问了！
```

---

## 🆘 常见问题

**Q: 为什么访问不了？**
A: 检查是否 2-3 分钟已过。如果还是不行，检查仓库设置中是否正确启用了 Pages。

**Q: 可以在手机上访问吗？**
A: 完全可以！任何手机、平板、电脑都能访问。

**Q: 如何更新数据？**
A: 编辑 GitHub 上的文件或本地编辑后 push，自动更新。

**Q: 有没有流量限制？**
A: GitHub Pages 没有流量限制，完全免费无限使用。

**Q: 需要代码知识吗？**
A: 不需要！按照步骤做就行。

---

## 📱 分享模板

将此文本分享给团队：

```
🎉 我们的异议查询助手现在上线了！

📱 访问地址：https://your-username.github.io/objection-assistant

✨ 功能：
- 搜索 11+ 条真实销售异议
- 智能话术推荐
- 数据支撑和成功案例
- 手机/电脑都支持
- 完全免费

💡 使用方式：
1. 在浏览器打开链接
2. 搜索相关异议
3. 一键复制话术到微信/电话

👥 让我们一起提高成交率！
```

---

**最后更新**: 2026-03-31  
**作者**: AI 助手
