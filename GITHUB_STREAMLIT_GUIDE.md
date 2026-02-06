# 完整部署指南：GitHub + Streamlit Cloud

## 第一步：准备Git仓库

### 1.1 检查Git是否安装

打开终端（Terminal），运行：

```bash
git --version
```

如果没有安装，去 https://git-scm.com/downloads 下载安装。

### 1.2 进入项目目录

```bash
cd "/Users/andyzhang/Desktop/26_Spring/Asset_Management/-Pre-first class readings/mvp_web"
```

### 1.3 初始化Git仓库

```bash
git init
```

你会看到：`Initialized empty Git repository...`

### 1.4 添加所有文件

```bash
git add .
```

### 1.5 创建第一次提交

```bash
git commit -m "Initial commit: Mean-Variance Portfolio Optimizer"
```

## 第二步：在GitHub上创建仓库

### 2.1 登录GitHub

访问：https://github.com

如果没有账号，先注册一个（免费）。

### 2.2 创建新仓库

1. 点击右上角的 **"+"** 号
2. 选择 **"New repository"**
3. 填写信息：
   - **Repository name**: `mvp-optimizer` （或者你喜欢的名字）
   - **Description**: `Mean-Variance Portfolio Optimizer - Columbia Business School`
   - **Public** 或 **Private**：选择 **Public**（免费部署需要public）
   - ❗ **不要**勾选 "Add a README file"
   - ❗ **不要**勾选 "Add .gitignore"
   - ❗ **不要**选择 "Choose a license"
4. 点击 **"Create repository"**

### 2.3 记录仓库URL

创建后，你会看到类似这样的URL：

```
https://github.com/你的用户名/mvp-optimizer.git
```

复制这个URL！

## 第三步：推送代码到GitHub

### 3.1 添加远程仓库

在终端运行（替换成你的URL）：

```bash
git remote add origin https://github.com/你的用户名/mvp-optimizer.git
```

### 3.2 重命名分支为main（如果需要）

```bash
git branch -M main
```

### 3.3 推送代码

```bash
git push -u origin main
```

如果是第一次推送，可能需要输入GitHub用户名和密码（或者token）。

**注意**：GitHub现在使用Personal Access Token而不是密码。

#### 如何获取Token（如果需要）：

1. 访问：https://github.com/settings/tokens
2. 点击 **"Generate new token"** → **"Generate new token (classic)"**
3. 给token一个名字，如 "MVP Optimizer Deployment"
4. 勾选 **"repo"** 权限
5. 点击 **"Generate token"**
6. **复制token**（只显示一次！）
7. 在推送时，用token作为密码

### 3.4 验证推送成功

访问你的GitHub仓库页面：

```
https://github.com/你的用户名/mvp-optimizer
```

应该能看到所有文件。

## 第四步：部署到Streamlit Cloud

### 4.1 访问Streamlit Cloud

打开：https://share.streamlit.io

### 4.2 登录

1. 点击 **"Sign in"**
2. 选择 **"Continue with GitHub"**
3. 授权Streamlit访问你的GitHub

### 4.3 部署新应用

1. 点击 **"New app"** 按钮

2. 填写部署信息：
   - **Repository**: 选择 `你的用户名/mvp-optimizer`
   - **Branch**: `main`
   - **Main file path**: `app.py`

3. **Advanced settings**（可选）：
   - Python version: `3.9` 或 `3.10`
   - 其他保持默认

4. 点击 **"Deploy!"**

### 4.4 等待部署

- 第一次部署需要 2-5 分钟
- 你会看到实时日志
- 显示 "Your app is live!" 就成功了

### 4.5 获取应用URL

部署成功后，你会得到一个公开URL：

```
https://你的用户名-mvp-optimizer-app-xxxxx.streamlit.app
```

## 第五步：测试应用

### 5.1 访问URL

打开浏览器，访问你的应用URL。

### 5.2 测试功能

1. 输入资产数据
2. 点击 "Optimize Portfolio"
3. 查看结果和图表
4. 测试 Sensitivity Analysis

## 第六步：更新应用（未来）

当你修改代码后：

### 6.1 在本地提交更改

```bash
git add .
git commit -m "描述你的更改"
git push
```

### 6.2 自动部署

Streamlit Cloud会自动检测到更改并重新部署！

- 通常需要 30秒-2分钟
- 在 Streamlit Cloud 管理界面可以看到部署状态

## 常见问题排查

### 问题1：git push被拒绝

**错误信息**：
```
remote: Support for password authentication was removed...
```

**解决方案**：
使用Personal Access Token代替密码（见第三步3.3）。

### 问题2：部署失败 - 找不到模块

**错误信息**：
```
ModuleNotFoundError: No module named 'xxx'
```

**解决方案**：
确保 `requirements.txt` 包含所有依赖。

### 问题3：应用一直Loading

**可能原因**：
- 优化时间太长
- 内存不足

**解决方案**：
- 减少efficient frontier点数
- 减少资产数量测试

### 问题4：Cannot push to private repository

**解决方案**：
将仓库改为Public：
1. 去GitHub仓库页面
2. Settings → 拉到最底部
3. Change visibility → Make public

## 快速命令参考

### 完整部署流程（一次性）

```bash
# 进入项目目录
cd "/Users/andyzhang/Desktop/26_Spring/Asset_Management/-Pre-first class readings/mvp_web"

# 初始化git
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: Mean-Variance Portfolio Optimizer"

# 添加远程仓库（替换URL）
git remote add origin https://github.com/你的用户名/mvp-optimizer.git

# 推送
git branch -M main
git push -u origin main
```

### 日常更新流程

```bash
# 修改代码后...

git add .
git commit -m "描述你的更改"
git push
```

## 检查清单

- [ ] Git已安装
- [ ] GitHub账号已创建
- [ ] 仓库已创建（public）
- [ ] 代码已推送到GitHub
- [ ] Streamlit Cloud账号已创建
- [ ] 应用已部署
- [ ] 应用URL可访问
- [ ] 功能测试通过

## 下一步

1. **分享URL**：把应用URL分享给他人
2. **自定义域名**（可选）：在Streamlit Cloud设置
3. **监控使用**：查看访问统计
4. **持续改进**：根据反馈更新代码

## 需要帮助？

- Streamlit文档：https://docs.streamlit.io
- Streamlit论坛：https://discuss.streamlit.io
- GitHub帮助：https://docs.github.com

---

**恭喜！你的应用现在已经部署到云端了！** 🎉
