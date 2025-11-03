cd ~/repositories/inventory_bot && \
pkill -f bot.py && \
sleep 2 && \
git pull origin main && \
sleep 2 && \
chmod +x backup_db.sh start_bot.sh keep_alive.sh check_status.sh && \
./start_bot.sh && \
sleep 2 && \
./check_status.sh