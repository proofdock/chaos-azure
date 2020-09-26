#!/bin/bash

echo Input configuration: duration="$input_duration" seconds, path="$input_path"

touch "$input_path"
partition=$(df "$input_path" | awk '/^\/dev/ {print $1}')
echo The partition for "$input_path" is "$partition"
block_size=$(blockdev --getbsz "$partition")
echo The partition block size is "$block_size" bytes

# File template for /tmp/loop.sh
cat << EOF > /tmp/loop.sh
#!/bin/bash
while [ true ];
do
    sudo dd if=/dev/urandom of="$input_path" bs="$block_size" count=10000 iflag=fullblock
done
EOF

# Execute the /tmp/loop.sh as long as the timeout holds
chmod +x /tmp/loop.sh
timeout --preserve-status "$input_duration" /tmp/loop.sh "$input_path" "$block_size"

# Clean up actions
sudo rm "$input_path"
sudo rm /tmp/loop.sh