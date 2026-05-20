Therefore, anything that needs to be run on a Windows Operating System is executed using an executable file, also called a Portable Executable file (PE file), as it can be run on any Windows system. A PE file is a Common Object File Format (COFF) data structure. The COFF consists of Windows PE files, DLLs, shared objects in Linux, and ELF files. For this room, we will only be covering the Windows PE files.

We will use the `wxHexEditor` utility, present in the next task's attached VM to perform this task.

As we view the file in a Hex editor, we observe that manually interpreting all this data might become too tedious. Therefore, we will use a tool `pe-tree` in the attached VM to help us analyze the PE header. This is what we see when we open a PE file using `pe-tree`.

![A PE file as shown by the pe-tree utility](https://tryhackme-images.s3.amazonaws.com/user-uploads/61306d87a330ed00419e22e7/room-content/1b5ee018dd56753682a480e83a0789f2.png)
In the right pane here, we see some tree-structure dropdown menus. The left pane is just shortcuts to the dropdown menus of the right pane. Some of the important headers that we will discuss in this room are:

- IMAGE_DOS_HEADER
- IMAGE_NT_HEADERS  
    - FILE_HEADER
    - OPTIONAL_HEADER
    - IMAGE_SECTION_HEADER
    - IMAGE_IMPORT_DESCRIPTOR

All of these headers are of the data type [STRUCT](https://docs.microsoft.com/en-us/cpp/cpp/struct-cpp?view=msvc-170). A struct is a user-defined data type that combines several different types of data elements in a single variable. Since it is user-defined, we need to see the documentation to understand the type for each STRUCT variable. The documentation for each header can be found on [MSDN](https://docs.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-image_nt_headers32), where you can find the data types of the different fields inside these headers.


![PE file as seen in a Hex Editor, with IMAGE_DOS_HEADER highlighted](https://tryhackme-images.s3.amazonaws.com/user-uploads/61306d87a330ed00419e22e7/room-content/5a5864011a51bcfc1b363ce611a442e0.png)  

In the screenshot above from the Hex Editor, notice the first two bytes that say `4D 5A`. They translate to the `MZ` characters in ASCII, as shown in the right pane of the Hex Editor. So what do these characters mean?

The MZ characters denote the initials of [Mark Zbikowski](https://en.wikipedia.org/wiki/Mark_Zbikowski), one of the Microsoft architects who created the MS-DOS file format. The MZ characters are an identifier of the Portable Executable format. When these two bytes are present at the start of a file, the Windows OS considers it a Portable Executable format file.

IMAGE_NT_HEADERS in [Microsoft Documentation](https://docs.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-image_nt_headers32). This header contains most of the vital information related to the PE file. In pe-tree, this is how the IMAGE_NT_HEADERS look like:

![IMAGE_NT_HEADERS as seen in the pe-tree utility](https://tryhackme-images.s3.amazonaws.com/user-uploads/61306d87a330ed00419e22e7/room-content/48f2264530712e1b95f9c33a045e7280.png)


Let's learn about some of the critical fields in the OPTIONAL_HEADER.

- _Magic:_ The Magic number tells whether the PE file is a 32-bit or 64-bit application. If the value is 0x010B, it denotes a 32-bit application; if the value is 0x020B, it represents a 64-bit application. The above screenshot of the Hex Editor shows the highlighted bytes, which show the magic of the loaded PE file. Since the value is 0x010B, it shows that it is a 32-bit application.
- _AddressOfEntryPoint:_ This field is significant from a malware analysis/reverse-engineering point of view. This is the address from where Windows will begin execution. In other words, the first instruction to be executed is present at this address. This is a Relative Virtual Address (RVA), meaning it is at an offset relative to the base address of the image (ImageBase) once loaded into memory.
- BaseOfCode and BaseOfData: These are the addresses of the code and data sections, respectively, relative to ImageBase.
- _ImageBase:_ The ImageBase is the preferred loading address of the PE file in memory. Generally, the ImageBase for .exe files is 0x00400000, which is also the case for our PE file. Since Windows can't load all PE files at this preferred address, some relocations are in order when the file is loaded in memory. These relocations are then performed relative to the ImageBase.
- _Subsystem:_ This represents the Subsystem required to run the image. The Subsystem can be Windows Native, GUI (Graphical User Interface), CUI (Commandline User Interface), or some other Subsystem. The screenshot above from the pe-tree utility shows that the Subsystem is 0x0002, representing Windows GUI Subsystem. We can find the complete list in [Microsoft Documentation](https://docs.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-image_optional_header32).
- _DataDirectory:_ The DataDirectory is a structure that contains import and export information of the PE file (called Import Address Table and Export Address Table). This information is handy as it gives a glimpse of what the PE file might be trying to do. We will expand on the import information later in this room.

This is what the IMAGE_IMPORT_DESCRIPTOR looks like in the pe-tree utility.

![IMAGE_IMPORT_DESCRIPTOR as shown using the pe-tree utility](https://tryhackme-images.s3.amazonaws.com/user-uploads/61306d87a330ed00419e22e7/room-content/7ef95b3a891b858660b13c7fd416490a.png)

Here we can see that the PE file we are looking at imports functions from ADVAPI32.dll, SHELL32.dll, ole32.dll, COMCTL32.dll, and USER32.dll. These files are dynamically linked libraries that export Windows functions or APIs for other PE files. The above screenshot shows that the PE file imports some functions that perform some registry actions. To find more information about what the function does, we can check out Microsoft Documentation. For example, [this link](https://docs.microsoft.com/en-us/windows/win32/api/winreg/nf-winreg-regcreatekeyexw) has details about the RegCreateKeyExW function.

In the above screenshot, we can see the values OriginalFirstThunk and FirstThunk. The Operating System uses these values to build the Import Address Table (IAT) of the PE file. We will learn more about these values in the coming rooms.

In the above screenshot, we can see the values OriginalFirstThunk and FirstThunk. The Operating System uses these values to build the Import Address Table (IAT) of the PE file. We will learn more about these values in the coming rooms.