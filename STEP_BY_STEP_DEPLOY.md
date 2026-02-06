# 🚀 一步步部署到Streamlit Cloud

## 📋 前置准备

### 需要的账号：
1. ✅ GitHub账号 (https://github.com/signup)
2. ✅ Streamlit Cloud账号（用GitHub登录，免费）

---

## 🎯 完整流程（大约15分钟）

### 第一部分：GitHub准备 (5分钟)

#### 步骤1：创建GitHub仓库

1. **登录GitHub**
   - 访问：https://github.com
   - 如果没有账号，点击"Sign up"注册（免费）

2. **创建新仓库**
   - 点击右上角 **"+"** → **"New repository"**
   
3. **填写仓库信息**：
   ```
   Repository name: mvp-optimizer
   Description: Mean-Variance Portfolio Optimizer
   Public: ✓ (必须选这个才能免费部署)
   
   ⚠️ 重要：不要勾选任何checkbox！
   - ❌ Add a README file
   - ❌ Add .gitignore
   - ❌ Choose a license
   ```

4. **点击绿色按钮 "Create repository"**

5. **复制仓库URL**
   - 你会看到一个以 `.git` 结尾的URL
   - 类似：`https://github.com/你的用户名/mvp-optimizer.git`
   - **复制这个URL！** （待会要用）

---

### 第二部分：推送代码到GitHub (3分钟)

#### 方法A：使用部署脚本（推荐，最简单）

1. **打开终端（Terminal）**
   - Mac: Spotlight搜索 "Terminal"
   - 或者在Cursor中打开integrated terminal

2. **运行部署脚本**
   ```bash
   cd "/Users/andyzhang/Desktop/26_Spring/Asset_Management/-Pre-first class readings/mvp_web"
   
   ./deploy_to_github.sh "你的仓库URL"
   ```
   
   **例如**：
   ```bash
   ./deploy_to_github.sh "https://github.com/andyzhang/mvp-optimizer.git"
   ```

3. **输入GitHub凭证**
   - Username: 你的GitHub用户名
   - Password: **Personal Access Token** (不是密码！见下方)

#### 如何获取Personal Access Token：

如果是第一次推送，需要token：

1. 访问：https://github.com/settings/tokens
2. 点击 **"Generate new token"** → **"Generate new token (classic)"**
3. 填写：
   - Note: `MVP Optimizer`
   - Expiration: `90 days`
   - 勾选：**`repo`** (全部repo权限)
4. 点击底部 **"Generate token"**
5. **⚠️ 复制token（只显示一次！保存到安全地方）**
6. 在命令行提示输入password时，粘贴这个token

#### 方法B：手动命令（如果脚本不工作）

```bash
cd "/Users/andyzhang/Desktop/26_Spring/Asset_Management/-Pre-first class readings/mvp_web"

git add .
git commit -m "Initial commit: MVP Optimizer"
git remote add origin https://github.com/你的用户名/mvp-optimizer.git
git branch -M main
git push -u origin main
```

#### 验证成功：

访问你的GitHub仓库页面，应该看到所有文件：
- app.py
- optimizer.py
- sensitivity.py
- visualizations.py
- utils.py
- requirements.txt
- README.md
- 等等...

---

### 第三部分：部署到Streamlit Cloud (5分钟)

#### 步骤1：访问Streamlit Cloud

1. 打开：https://share.streamlit.io
2. 点击 **"Sign in"** 或 **"Get started"**
3. 选择 **"Continue with GitHub"**
4. 授权Streamlit访问你的GitHub（点击 "Authorize streamlit"）

#### 步骤2：创建新应用

1. 点击 **"New app"** 按钮（右上角）

2. 选择部署源：
   ```
   Repository: 你的用户名/mvp-optimizer
   Branch: main
   Main file path: app.py
   ```

3. **（可选）点击 "Advanced settings"**：
   ```
   Python version: 3.9
   ```

4. 点击蓝色按钮 **"Deploy!"**

#### 步骤3：等待部署

- 你会看到实时日志滚动
- 第一次部署需要 **2-5分钟**
- 过程：
  1. ⏳ Installing dependencies...
  2. ⏳ Building app...
  3. ✅ Your app is live!

#### 步骤4：获取URL并测试

部署成功后：
1. 自动跳转到你的应用
2. URL格式：`https://你的用户名-mvp-optimizer-app-xxxxx.streamlit.app`
3. **测试功能**：
   - 输入资产数据
   - 点击 "Optimize Portfolio"
   - 查看efficient frontier
   - 测试sensitivity analysis

---

## ✅ 检查清单

部署成功后，确认：

- [ ] GitHub仓库已创建且是Public
- [ ] 所有代码文件已推送到GitHub
- [ ] Streamlit Cloud应用状态显示 "Running"
- [ ] 可以访问应用URL
- [ ] Portfolio Optimization功能正常
- [ ] Sensitivity Analysis功能正常
- [ ] 图表正常显示

---

## 🔄 日后更新代码

当你修改代码后，只需三个命令：

```bash
cd "/Users/andyzhang/Desktop/26_Spring/Asset_Management/-Pre-first class readings/mvp_web"

git add .
git commit -m "描述你的更改"
git push
```

**Streamlit会自动检测并重新部署！**（大约30秒-2分钟）

---

## 🐛 常见问题

### 问题1：git push要求密码但密码不对

**解决**：GitHub不再接受密码，必须使用Personal Access Token
- 按照上面"获取Personal Access Token"的步骤操作

### 问题2：Streamlit部署失败 - ModuleNotFoundError

**检查**：
```bash
cat requirements.txt
```

确保包含：
```
numpy>=1.21.0
pandas>=1.3.0
scipy>=1.7.0
matplotlib>=3.4.0
streamlit>=1.20.0
```

### 问题3：推送被拒绝 - Repository is private

**解决**：
1. 去GitHub仓库页面
2. Settings → Danger Zone
3. Change visibility → Make public

### 问题4：应用一直loading

**可能原因**：
- 第一次访问需要启动容器（1-2分钟）
- 优化时间过长

**解决**：
- 耐心等待
- 刷新页面
- 减少资产数量测试

---

## 📞 需要帮助？

1. **检查部署日志**：
   - 在Streamlit Cloud点击应用
   - 查看 "Logs" tab
   - 看具体错误信息

2. **GitHub问题**：
   - 确认仓库是Public
   - 确认所有文件都已推送
   - 检查 requirements.txt

3. **联系支持**：
   - Streamlit论坛：https://discuss.streamlit.io
   - GitHub文档：https://docs.github.com

---

## 🎉 恭喜！

你的Portfolio Optimizer现在已经：
- ✅ 托管在GitHub上（版本控制）
- ✅ 部署到云端（全球访问）
- ✅ 自动更新（推送即部署）
- ✅ 完全免费！

**分享你的应用URL给同学、教授或投资者吧！**
