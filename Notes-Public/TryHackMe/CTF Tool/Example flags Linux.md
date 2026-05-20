# head

### View the first 64 bytes in Hex (Recommended)
```
head -c 64 FW_WRT1900ACSV2_2.0.3.201002_prod.img | hexdump -C
```

### The Standard Way (First 20 "Lines")

If you just want to see the first 20 lines as the computer sees them:

```
head -n 20 FW_WRT1900ACSV2_2.0.3.201002_prod.img
```
### The Readable Way (Recommended)

This command looks at the beginning of the file and extracts only the **human-readable text** (words, versions, labels) found in those first lines:
```
head -n 50 FW_WRT1900ACSV2_2.0.3.201002_prod.img | strings
```

- head -n 50: Grabs the first 50 lines.
- strings: Filters out the binary "trash" and only shows readable text like "Linksys", "Linux", or "Build date".

# strings

```
strings -n 10 FW_WRT1900ACSV2_2.0.3.201002_prod.img | head -n 50
```

- -n 10: Only shows sequences of at least 10 readable characters.

# find
find <starting_point> -name <filename>

Breakdown of the Information

- /dev/root is the main disk of the system with --G total, 12G used, <REDACTED>G free, and is 17% full.
- tmpfs entries are temporary filesystems stored in RAM, not on the physical disk.
- /dev/shm is a shared memory area with 1.9G available and 0 used.
- /run/user/114 is similar temporary storage for another system user, also 387M total and mostly empty.

To search the entire hard drive (/) for a directory (-type d) named exactly ".git" (-name ".git"), and hide all the annoying "Permission denied" errors (2>/dev/null), copy and paste this exactly:


find / -type d -name ".git" 2>/dev/null

find / -name "rockyou.txt" 2>/dev/null