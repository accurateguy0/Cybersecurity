### . Install the missing library

The libpci missing error is caused by a missing package. Run this to fix it:

codeBash

```
sudo apt update && sudo apt install pciutils -y
```

### 2. Force Software Rendering (Bypass Graphics Errors)

To stop Firefox from crashing on the "framebuffer" error, you can tell it to use software rendering instead of hardware acceleration. Launch it like this:

codeBash

```
export LIBGL_ALWAYS_SOFTWARE=1
firefox &
```

Alternatively, try launching it with the "no-remote" flag if it says an instance is already running:

codeBash

```
firefox --no-remote http://10.112.144.183 &
```

### 3. Quickest Alternative: Use a Text Browser

If you just need to see the content of the page or interact with a basic web form and don't want to deal with GUI errors, use **Lynx** or **Links**. These are browsers that run directly inside your terminal:

codeBash

```
# Install it
sudo apt install links -y

# Run it
links http://10.112.144.183
```