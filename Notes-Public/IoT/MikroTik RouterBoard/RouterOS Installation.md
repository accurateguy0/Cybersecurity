Installing RouterOS on x86 hardware (a standard PC or server) turns that computer into a powerful professional router. There are two main ways to do this, depending on whether you are installing it on a **physical computer (Bare Metal)** or a **Virtual Machine (VM)**.

---

### Method 1: Bare Metal (Installing on a physical PC/Server)

This method involves wiping the computer's hard drive and installing RouterOS as the primary operating system.

**1. Download the ISO**

- Go to the [MikroTik Download Page](https://www.google.com/url?sa=E&q=https%3A%2F%2Fmikrotik.com%2Fdownload).
- Look for the **x86** section.
- Download the **CD Image** (the .iso file).

**2. Create a Bootable USB**

- Since the file is an ISO, you need to "burn" it to a USB drive.
- Use a tool like **Rufus** (Windows) or **BalenaEtcher** (Mac/Linux).
- Note: In Rufus, if it asks for "ISO mode" vs "DD mode," try ISO mode first; if it doesn't boot, try DD mode.
    

**3. Boot the PC**

- Plug the USB into your target PC.
- Enter the BIOS/UEFI settings and ensure the PC is set to boot from the USB drive.
- **Important:** RouterOS x86 traditionally supports **Legacy BIOS**. If your PC is modern and only supports UEFI, you may need to enable "CSM" or "Legacy Mode" in the BIOS.

**4. The Installation Process**

- Once booted, you will see a blue screen with a list of "packages" (system, dhcp, routing, etc.).
- Press **a** to select all packages.
- Press **i** to install.
- It will ask if you want to keep old configurations (press **n**) and warn you that all data on the disk will be erased (press **y**).
- Once finished, remove the USB and press Enter to reboot.
