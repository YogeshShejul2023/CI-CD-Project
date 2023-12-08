#!/bin/bash

# Set variables
CODE_DIR="/home/ubuntu/Yogesh"
NGINX_RESTART_CMD="sudo systemctl restart nginx"  # Adjust for your system

# Navigate to the code directory
cd $CODE_DIR || exit

# Pull the latest code from the repository
git pull origin master

# Restart Nginx
$NGINX_RESTART_CMD

# Log the deployment details (optional)
echo "Deployment completed on $(date)" >> /path/to/deployment.log
