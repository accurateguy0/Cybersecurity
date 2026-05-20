| Hive Name    | Contains                                                                                         | Location                                                         |
| ------------ | ------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------- |
| SYSTEM       | - Services<br>- Mounted Devices<br>- Boot Configuration<br>- Drivers<br>- Hardware               | `C:\Windows\System32\config\SYSTEM`                              |
| SECURITY     | - Local Security Policies<br>- Audit Policy Settings                                             | `C:\Windows\System32\config\SECURITY`                            |
| SOFTWARE     | - Installed Programs<br>- OS Version and other info<br>- Autostarts<br>- Program Settings        | `C:\Windows\System32\config\SOFTWARE`                            |
| SAM          | - Usernames and their Metadata<br>- Password Hashes<br>- Group Memberships<br>- Account Statuses | `C:\Windows\System32\config\SAM`                                 |
| NTUSER.DAT   | - Recent Files<br>- User Preferences<br>- User-specific Autostarts                               | `C:\Users\username\NTUSER.DAT`                                   |
| USRCLASS.DAT | - Shellbags<br>- Jump Lists                                                                      | `C:\Users\username\AppData\Local\Microsoft\Windows\USRCLASS.DAT` |

 These Registry Hives contain binary data that cannot be opened directly from the file. So, double-clicking them would only display things you won't ever understand. Then how can we possibly view the registry data?

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/68d2c1e7ab94268f6271de1d/room-content/68d2c1e7ab94268f6271de1d-1763584779702.png)

As you can see in the Registry Editor screenshot above, there are some folders named `HKEY_LOCAL_MACHINE`, `HKEY_CURRENT_USER`, and more. But didn't we expect `SYSTEM`, `SECURITY`, `SOFTWARE`, etc., to be seen so we can view their data? Don't worry, Windows organizes all the Registry Hives into these structured **Root Keys**. Instead of seeing the Registry Hives, you would always get these registry root keys whenever you open the registry.

## Registry Forensics

Since the registry contains a wide range of data about the Windows system, it plays a crucial role in forensic investigations. Registry forensics is the process of extracting and analyzing evidence from the registry. In Windows digital forensic investigations, investigators analyze registry, event logs, file system data, memory data, and other relevant data to construct the whole incident timeline. 

The table below lists some registry keys that are particularly useful during forensic investigations.

| Registry Key                                                             | Importance                                                                                                           |
| ------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------- |
| `HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist`     | It stores information on recently accessed applications launched via the GUI.                                        |
| `HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\TypedPaths`     | It stores all the paths and locations typed by the user inside the Explorer address bar.                             |
| `HKLM\Software\Microsoft\Windows\CurrentVersion\App Paths`               | It stores the path of the applications.                                                                              |
| `HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\WordWheelQuery` | It stores all the search terms typed by the user in the Explorer search bar.                                         |
| `HKLM\Software\Microsoft\Windows\CurrentVersion\Run`                     | It stores information on the programs that are set to automatically start (startup programs) when the users logs in. |
| `HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs`     | It stores information on the files that the user has recently accessed.                                              |
| `HKLM\SYSTEM\CurrentControlSet\Control\ComputerName\ComputerName`        | It stores the computer's name (hostname).                                                                            |
| `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall`               | It stores information on the installed programs.                                                                     |

**Step 3: Handling Dirty Hives**

While loading Registry Hives, it is important to know that these Registry Hives can sometimes be "dirty" when collected from live systems, meaning they may have incomplete transactions. To ensure clean loading:

1.On the **Load hives** pop-up, navigate to `C:\Users\Administrator\Desktop\Registry Hives   `2. Select the desired hive file (e.g., SYSTEM)  
**3. Hold SHIFT**, then press **Open** to load associated transaction log files. This ensures you get a clean, consistent hive state for analysis.