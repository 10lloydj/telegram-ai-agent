# Hetzner VPS Deployment Guide

## 1. Create Hetzner VPS

1. Go to [Hetzner Cloud Console](https://console.hetzner-cloud.com/)
2. Create new project: "telegram-ai-agent"
3. Add server:
   - **Location**: Nuremberg or Helsinki (closest to you)
   - **Image**: Ubuntu 22.04
   - **Type**: CX11 (€3.29/month) - 1 vCPU, 2GB RAM, 20GB SSD
   - **SSH Key**: Upload your public key
   - **Name**: telegram-ai-agent

## 2. Initial Server Setup

SSH into your server:
```bash
ssh root@YOUR_SERVER_IP
```

Update system and install Docker:
```bash
# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
apt install docker-compose-plugin -y

# Start Docker
systemctl enable docker
systemctl start docker

# Install Git
apt install git -y

# Create app user (optional but recommended)
useradd -m -s /bin/bash app
usermod -aG docker app
```

## 3. Deploy Application

Switch to app user (if created):
```bash
su - app
```

Clone your repository:
```bash
git clone https://github.com/YOUR_USERNAME/telegram-ai-agent.git
cd telegram-ai-agent
```

Set up environment:
```bash
cp .env.example .env
nano .env  # Edit with your actual values
```

**Important**: Update these values in `.env`:
- `API_ID` - Your Telegram API ID
- `API_HASH` - Your Telegram API hash  
- `TARGET_CHAT_ID` - The chat ID to monitor
- `OPENAI_API_KEY` - Your OpenAI API key
- `SELF_USERNAME` - Your Telegram username

Transfer your session file:
```bash
# From your local machine:
scp me.session root@YOUR_SERVER_IP:/home/app/telegram-ai-agent/
```

Deploy:
```bash
./deploy.sh
```

## 4. Verify Deployment

Check if services are running:
```bash
docker compose ps
```

View logs:
```bash
docker compose logs -f app
```

You should see: "Agent running with ingestion/notifier enabled"

## 5. Ongoing Management

**View logs:**
```bash
docker compose logs -f
```

**Restart services:**
```bash
docker compose restart
```

**Update application:**
```bash
git pull origin main
./deploy.sh
```

**Create database backup:**
```bash
./backup.sh
```

**Stop services:**
```bash
docker compose down
```

## 6. Security (Recommended)

Set up UFW firewall:
```bash
ufw allow OpenSSH
ufw allow 22
ufw enable
```

Set up automatic updates:
```bash
apt install unattended-upgrades -y
dpkg-reconfigure -plow unattended-upgrades
```

## 7. Monitoring

**Check disk usage:**
```bash
df -h
```

**Check memory usage:**
```bash
free -h
```

**Check Docker stats:**
```bash
docker stats
```

## Troubleshooting

**If app fails to start:**
1. Check logs: `docker compose logs app`
2. Verify `.env` file has correct values
3. Ensure `me.session` file exists
4. Check if Postgres is healthy: `docker compose ps`

**If database issues:**
1. Check Postgres logs: `docker compose logs db`
2. Restart database: `docker compose restart db`
3. Restore from backup if needed

**Cost**: €3.29/month total for VPS + PostgreSQL + 24/7 operation
