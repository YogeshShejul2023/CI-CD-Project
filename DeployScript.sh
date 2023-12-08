#!/bin/bash
sudo rm -rf /var/www/html
GITHUB_REPO_URL="git remote add origin https://github.com/YogeshShejul2023/CI-CD-Project.git"
DEPLOY_DIR="/var/www/html"
git clone $GITHUB_REPO_URL $DEPLOY_DIR
sudo systemctl restart nginx