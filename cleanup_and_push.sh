#!/bin/bash

# 清理并只推送核心文件到GitHub

echo "=========================================="
echo "清理项目，只保留核心文件"
echo "=========================================="
echo ""

cd "/Users/andyzhang/Desktop/26_Spring/Asset_Management/-Pre-first class readings/mvp_web"

# 删除辅助文件（保留在本地作为参考）
echo "识别的核心文件："
echo "  ✓ app.py (主应用)"
echo "  ✓ optimizer.py (优化引擎)"
echo "  ✓ sensitivity.py (敏感性分析)"
echo "  ✓ visualizations.py (可视化)"
echo "  ✓ utils.py (工具函数)"
echo "  ✓ requirements.txt (依赖)"
echo "  ✓ README.md (文档)"
echo "  ✓ .streamlit/config.toml (配置)"
echo "  ✓ .gitignore (Git配置)"
echo ""

echo "将从Git中移除（但保留在本地）："
echo "  - 所有 .md 文档（除了 README.md）"
echo "  - 所有 .sh 脚本"
echo "  - test.py"
echo "  - .git_token"
echo ""

read -p "继续？(y/n): " CONFIRM

if [ "$CONFIRM" != "y" ]; then
    echo "取消操作"
    exit 0
fi

echo ""
echo "正在清理..."

# 从Git中移除已跟踪的辅助文件（保留在本地）
git rm --cached DEPLOYMENT.md 2>/dev/null
git rm --cached FIX_AUTH_ERROR.md 2>/dev/null
git rm --cached GITHUB_STREAMLIT_GUIDE.md 2>/dev/null
git rm --cached PROJECT_SUMMARY.md 2>/dev/null
git rm --cached QUICKSTART.md 2>/dev/null
git rm --cached SSH_COMPLETE_GUIDE.md 2>/dev/null
git rm --cached STEP_BY_STEP_DEPLOY.md 2>/dev/null
git rm --cached deploy_to_github.sh 2>/dev/null
git rm --cached fix_email_privacy.sh 2>/dev/null
git rm --cached push_with_token.sh 2>/dev/null
git rm --cached setup_ssh.sh 2>/dev/null
git rm --cached test.py 2>/dev/null
git rm --cached .git_token 2>/dev/null

echo "✓ 辅助文件已从Git移除（本地仍保留）"
echo ""

# 查看将要推送的文件
echo "将要推送到GitHub的文件："
echo "=========================================="
git ls-files
echo "=========================================="
echo ""

read -p "确认推送这些文件？(y/n): " PUSH_CONFIRM

if [ "$PUSH_CONFIRM" = "y" ]; then
    echo ""
    echo "创建提交..."
    git add .
    git commit -m "Clean up: Keep only core application files"
    
    echo ""
    echo "推送到GitHub..."
    git push -u origin main
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "=========================================="
        echo "✓ 成功！"
        echo "=========================================="
        echo ""
        echo "已推送的核心文件："
        echo "  - app.py"
        echo "  - optimizer.py"
        echo "  - sensitivity.py"
        echo "  - visualizations.py"
        echo "  - utils.py"
        echo "  - requirements.txt"
        echo "  - README.md"
        echo "  - .streamlit/config.toml"
        echo ""
        echo "辅助文件仍保留在本地作为参考"
        echo ""
        echo "GitHub仓库: https://github.com/zz3231/mvp-optimizer"
    else
        echo ""
        echo "推送失败，请检查错误信息"
    fi
else
    echo "取消推送"
fi
