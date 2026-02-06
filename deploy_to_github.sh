#!/bin/bash

# 部署脚本 - 推送到GitHub
# 使用方法: ./deploy_to_github.sh "你的GitHub仓库URL"

echo "=========================================="
echo "Mean-Variance Optimizer - GitHub部署"
echo "=========================================="
echo ""

# 检查参数
if [ -z "$1" ]; then
    echo "错误：请提供GitHub仓库URL"
    echo ""
    echo "使用方法："
    echo "  ./deploy_to_github.sh https://github.com/你的用户名/mvp-optimizer.git"
    echo ""
    exit 1
fi

REPO_URL=$1

echo "步骤 1/4: 添加所有文件到Git..."
git add .

echo ""
echo "步骤 2/4: 创建提交..."
git commit -m "Initial commit: Mean-Variance Portfolio Optimizer Web Application"

echo ""
echo "步骤 3/4: 设置远程仓库..."
git remote remove origin 2>/dev/null  # 删除旧的（如果存在）
git remote add origin "$REPO_URL"

echo ""
echo "步骤 4/4: 推送到GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "=========================================="
echo "完成！"
echo "=========================================="
echo ""
echo "下一步："
echo "1. 访问你的GitHub仓库验证文件已上传"
echo "2. 访问 https://share.streamlit.io"
echo "3. 登录并点击 'New app'"
echo "4. 选择你的仓库和 app.py 文件"
echo "5. 点击 Deploy!"
echo ""
