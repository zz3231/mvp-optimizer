#!/bin/bash

# SSH自动配置脚本 - 一次设置，永久使用
# 这个脚本会帮你完成SSH key的完整设置

set -e  # 遇到错误就停止

echo "=========================================="
echo "GitHub SSH Key 自动配置"
echo "一次设置，永久解决认证问题！"
echo "=========================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 步骤1：检查是否已有SSH key
echo "步骤 1/5: 检查现有SSH密钥..."
if [ -f ~/.ssh/id_ed25519 ] || [ -f ~/.ssh/id_rsa ]; then
    echo -e "${YELLOW}检测到已有SSH密钥${NC}"
    echo ""
    echo "现有密钥："
    ls -la ~/.ssh/*.pub 2>/dev/null || true
    echo ""
    read -p "是否使用现有密钥？(y/n): " USE_EXISTING
    
    if [ "$USE_EXISTING" = "y" ]; then
        if [ -f ~/.ssh/id_ed25519.pub ]; then
            KEY_FILE=~/.ssh/id_ed25519.pub
        else
            KEY_FILE=~/.ssh/id_rsa.pub
        fi
        SKIP_KEYGEN=true
    else
        SKIP_KEYGEN=false
    fi
else
    SKIP_KEYGEN=false
fi

# 步骤2：生成新SSH key（如果需要）
if [ "$SKIP_KEYGEN" = false ]; then
    echo ""
    echo "步骤 2/5: 生成新的SSH密钥..."
    read -p "请输入你的GitHub邮箱: " EMAIL
    
    echo ""
    echo "正在生成SSH密钥..."
    ssh-keygen -t ed25519 -C "$EMAIL" -f ~/.ssh/id_ed25519 -N ""
    
    KEY_FILE=~/.ssh/id_ed25519.pub
    echo -e "${GREEN}✓ SSH密钥生成成功！${NC}"
else
    echo -e "${GREEN}✓ 使用现有SSH密钥${NC}"
fi

# 步骤3：启动SSH agent并添加密钥
echo ""
echo "步骤 3/5: 配置SSH agent..."
eval "$(ssh-agent -s)" > /dev/null 2>&1

# 添加到SSH agent
ssh-add ~/.ssh/id_ed25519 2>/dev/null || ssh-add ~/.ssh/id_rsa 2>/dev/null
echo -e "${GREEN}✓ SSH密钥已添加到agent${NC}"

# 步骤4：配置SSH config（自动使用密钥）
echo ""
echo "步骤 4/5: 配置SSH config文件..."
if [ ! -f ~/.ssh/config ]; then
    touch ~/.ssh/config
    chmod 600 ~/.ssh/config
fi

# 检查是否已配置GitHub
if ! grep -q "Host github.com" ~/.ssh/config; then
    cat >> ~/.ssh/config << EOF

# GitHub SSH配置
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519
    AddKeysToAgent yes
    UseKeychain yes
EOF
    echo -e "${GREEN}✓ SSH config已配置${NC}"
else
    echo -e "${YELLOW}GitHub配置已存在，跳过${NC}"
fi

# 步骤5：显示public key并提供添加指引
echo ""
echo "步骤 5/5: 添加SSH密钥到GitHub..."
echo "=========================================="
echo -e "${YELLOW}你的SSH Public Key:${NC}"
echo ""
cat $KEY_FILE
echo ""
echo "=========================================="
echo ""

# 复制到剪贴板（Mac）
if command -v pbcopy > /dev/null; then
    cat $KEY_FILE | pbcopy
    echo -e "${GREEN}✓ Public key已复制到剪贴板！${NC}"
    echo ""
fi

echo "接下来的步骤："
echo ""
echo "1. 访问: https://github.com/settings/keys"
echo "2. 点击 'New SSH key'"
echo "3. Title: 填写 'My Mac' 或任何你喜欢的名字"
echo "4. Key type: 选择 'Authentication Key'"
echo "5. Key: 粘贴上面的内容（已在剪贴板中）"
echo "6. 点击 'Add SSH key'"
echo ""

read -p "添加完成后，按Enter继续..." 

# 测试SSH连接
echo ""
echo "测试SSH连接..."
echo ""

if ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
    echo -e "${GREEN}=========================================="
    echo "✓ SSH配置成功！"
    echo "==========================================${NC}"
    echo ""
    echo "现在你可以使用SSH URL推送代码了："
    echo ""
    read -p "请输入你的GitHub用户名: " GITHUB_USER
    read -p "请输入你的仓库名 (例如: mvp-optimizer): " REPO_NAME
    
    echo ""
    echo "执行以下命令推送代码："
    echo ""
    echo "git remote remove origin"
    echo "git remote add origin git@github.com:$GITHUB_USER/$REPO_NAME.git"
    echo "git push -u origin main"
    echo ""
    
    read -p "是否现在推送？(y/n): " DO_PUSH
    
    if [ "$DO_PUSH" = "y" ]; then
        git remote remove origin 2>/dev/null || true
        git remote add origin git@github.com:$GITHUB_USER/$REPO_NAME.git
        git add .
        git commit -m "Initial commit: MVP Optimizer" 2>/dev/null || echo "已有提交"
        git branch -M main
        git push -u origin main
        
        if [ $? -eq 0 ]; then
            echo ""
            echo -e "${GREEN}=========================================="
            echo "✓ 成功推送到GitHub！"
            echo "==========================================${NC}"
            echo ""
            echo "仓库地址: https://github.com/$GITHUB_USER/$REPO_NAME"
        fi
    fi
else
    echo -e "${RED}=========================================="
    echo "✗ SSH连接测试失败"
    echo "==========================================${NC}"
    echo ""
    echo "可能的原因："
    echo "1. 还没有添加SSH key到GitHub"
    echo "2. 网络连接问题"
    echo ""
    echo "请确保已完成上述步骤，然后重新运行此脚本"
fi

echo ""
echo "=========================================="
echo "配置完成！"
echo "=========================================="
echo ""
echo "从现在开始，你可以："
echo "- 使用 git@github.com:用户名/仓库名.git 作为remote URL"
echo "- 不再需要输入密码或token"
echo "- 自动认证，永久有效"
echo ""
echo "配置文件位置："
echo "- SSH密钥: ~/.ssh/id_ed25519"
echo "- SSH配置: ~/.ssh/config"
echo ""
