sudo pkill -f "nft_server.py"
nohup sudo -E python -u nft_server.py 2>&1 > server.log &
tail -f server.log
