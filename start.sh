token=$(curl https://token.crushing.xyz/refresh-token)
# java -Xmx512m -jar /app/webdav.jar --aliyundrive.refresh-token=$token --server.port=8848 --aliyundrive.auth.enable=true --aliyundrive.auth.user-name=admin --aliyundrive.auth.password=3356 &
aliyundrive-webdav -p 8848 -U admin -W 3356 -r $token &
python3 update.py && python3 -m bot