docker run -d \
   -p 9000:9000 \
   -p 9001:9001 \
   --name minio \
   -v ./minio_data:/data \
   -e "MINIO_ROOT_USER=U4B6Zib75DXSPmavZb" \
   -e "MINIO_ROOT_PASSWORD=Q4#QP4dudUobU#NBcGB7RMKV4ajYb" \
   quay.io/minio/minio server /data --console-address ":9001"