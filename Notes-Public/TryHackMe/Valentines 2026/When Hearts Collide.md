Use fastcoll

sudo apt update
sudo apt install -y g++ libboost-all-dev git
git clone https://github.com/brimstone/fastcoll.git
cd fastcoll
make
```

### Step 2: Generate the Collision Pair

Now you will take your original dog image and create two new files (dog_A.jpg and dog_B.jpg) that look identical but have different data and the **same MD5 hash**.

Assuming your image is named dog.jpg:

```
./fastcoll_tool -p dog.jpg -o dog_A.jpg dog_B.jpg
```
### Step 3: Verify the Collision

Check that the files are different but their hashes are the same:

codeBash

```
# Check MD5 hashes (Should be IDENTICAL)
md5sum dog_A.jpg dog_B.jpg

# Check SHA1 hashes (Should be DIFFERENT)
sha1sum dog_A.jpg dog_B.jpg

Upload both Dog_A.jpg and Dog_B.jpg