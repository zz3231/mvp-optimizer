#!/bin/bash

# 使用Personal Access Token推送到GitHub
# 使用方法: ./push_with_token.sh

echo "=========================================="
echo "GitHub推送 - 使用Personal Access Token"
echo "=========================================="
echo ""

# 检查是否已有token
if [ -f ".git_token" ]; then
    echo "检测到已保存的token"
    TOKEN=$(cat .git_token)
else
    echo "请输入你的GitHub信息："
    echo ""
    read -p "GitHub用户名: " USERNAME
    read -sp "Personal Access Token (不会显示): " TOKEN
    echo ""
    echo ""
    
    # 可选：保存token到本地（不推荐在共享电脑上）
    read -p "是否保存token到本地？(y/n): " SAVE_TOKEN
    if [ "$SAVE_TOKEN" = "y" ]; then
        echo "$TOKEN" > .git_token
        chmod 600 .git_token
        echo ".git_token" >> .gitignore
        echo "Token已保存到 .git_token"
    fi
fi

echo ""
read -p "GitHub仓库名称 (例如: mvp-optimizer): " REPO_NAME
read -p "GitHub用户名: " USERNAME

echo ""
echo "准备推送到: https://github.com/$USERNAME/$REPO_NAME"
read -p "继续？(y/n): " CONFIRM

if [ "$CONFIRM" != "y" ]; then
    echo "取消操作"
    exit 0
fi

echo ""
echo "步骤 1/4: 添加文件..."
git add .

echo ""
echo "步骤 2/4: 创建提交..."
git commit -m "Initial commit: Mean-Variance Portfolio Optimizer"

echo ""
echo "步骤 3/4: 设置远程仓库..."
git remote remove origin 2>/dev/null
git remote add origin https://${USERNAME}:${TOKEN}@github.com/${USERNAME}/${REPO_NAME}.git

echo ""
echo "步骤 4/4: 推送到GitHub..."
git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ 成功推送到GitHub！"
    echo "=========================================="
    echo ""
    echo "仓库地址: https://github.com/$USERNAME/$REPO_NAME"
    echo ""
    echo "下一步："
    echo "1. 访问你的GitHub仓库验证文件"
    echo "2. 访问 https://share.streamlit.io"
    echo "3. 部署你的应用"
else
    echo ""
    echo "=========================================="
    echo "❌ 推送失败"
    echo "=========================================="
    echo ""
    echo "可能的原因："
    echo "1. Token权限不足（需要勾选 'repo' 权限）"
    echo "2. 仓库不存在（请先在GitHub创建）"
    echo "3. 用户名或token错误"
    echo ""
    echo "请检查后重试"
fi
