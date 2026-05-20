### 1. Make EVERY file in the current directory executable

If you are already inside the folder:

```
chmod +x *
```

### 2. Make only Shell Scripts (.sh) executable

This is the safest and most common method for Bug Bounty hunters. It ensures you don't accidentally try to "execute" a text file or a log file.
```
chmod +x *.sh
```

### 3. Make everything in subdirectories executable (Recursive)

If you have scripts inside folders within folders, use the -R flag:

```
chmod -R +x .
```

(The dot . at the end means "this current directory and everything inside it".)

### 4. The "Professional" Way (Using find)

If you want to be precise and only make **files** executable (ignoring folders), use the find command. This is very useful when your recon folder gets messy:

codeBash

```
find . -type f -name "*.sh" -exec chmod +x {} +
```

- -type f: Look for files only.
- -name "*.sh": Only files ending in .sh.
- -exec chmod +x {}: Run the chmod command on every file found.