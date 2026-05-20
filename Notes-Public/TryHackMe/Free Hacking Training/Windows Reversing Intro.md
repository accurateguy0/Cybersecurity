IDA Freeware. Historically the downside to IDA has always been its pricing, however, thanks to recent developments in other tools, the free version of IDA now has many more features than it used to. Other good tools include x64dbg, Ghidra, WinDBG, Radare2, and of course GDB. My daily drivers are x64dbg and Ghidra. IDA is used for this series since it's easy for beginners and results in us only having to use one tool.

**You need to have internet access to be able to decompile code with IDA Freeware, so it will NOT work in the provided VM.**  
IDA also has a decompiler. Do not become reliant on decompilers as they aren't always accurate and often have issues representing every instruction in longer sections of code. With that said, they are a great place to get a general idea of what's going on. To decompile, IDA calls it pseudocode, you can click on the area of code you want to decompile and press _F5_. You can also go to _View > Open Subviews > Generate Pseudocode_.

#### Functions

On the left, you can see the Functions window which shows the identified functions for the current program. Depending on what symbols you have access to, you may have more or less functions with actual names. If there are no symbols to identify a function, it will instead be given a generic name such as sub_140001000 where 140001000 is the address of the function.

#### Other Subviews

You can find other useful tabs/subviews under _View > Open Subviews_. I encourage you to play around with the different subviews as there's a significant amount of information found within them. One subview in particular which you should get familiar with is the _Strings_ subview. Here you can view all identified strings in memory. This can be helpful, as we will see later when finding a certain function or place of interest.

Let's say you have an array of 5 integers that starts at the address of 0x4000. The size of the array is 20 bytes since each integer is 4 bytes. The first integer is at 0x4000+0x0, the second is at 0x4000+0x04, and so on. Arrays are usually easy to analyze, like the character array (string) we encountered in the loop task.

Let's say we have the following class:

```cpp
class Human {
public:
	int age;
	float height;
	char* name;
	Human(char* newName, int newAge, float newHeight)
		: age(newAge), height(newHeight), name(newName) {}
};
```

This class's data will take up 16 bytes. 4 bytes for the age, 4 bytes for the height, and 8 for the name (pointers hold addresses and addresses in x64 are 8 bytes). How would this be identified in assembly? Let's say a pointer to the class is contained in RAX, and the address of the class is 0x4000. Here's some pseudo-assembly:

```asm
mov RAX, 0x4000     ; RAX = Address of the class and the age variable (offset 0)
lea RBX, [RAX+0x4]  ; RBX = Address of height
lea RCX, [RAX+0x8]  ; RCX = Address of name
mov [RAX], 0x32     ; age = 50
mov [RBX], 0x48     ; height = 72
mov [RCX], 0x424F42 ; name = "BOB"
```

#### Imports, Exports, Modules

You've probably seen many function names that are all nonsense. As mentioned earlier, most function names do not survive through compilation since they are just there for human understanding. You may, however, notice that some names do exist. This could be because of two main reasons.

- First, the tool recognizes the function and names it accordingly. IDA does this with FLIRT (Fast Library Identification and Recognition Technology) signatures. FLIRT signatures are used to identify standard library functions. The general idea of how they work is they search memory for a chunk of bytes that match a known chunk of bytes in a standard library function. Once a match is found, the function can be named accordingly. You can learn more about FLIRT signatures on the [IDA/Hex-Rays website](https://hex-rays.com/products/ida/tech/flirt/in_depth/). The main() function is a little more difficult since its signature is different for every program. However, IDA can still sometimes find it using some tricks. One commonality of the main() function is that it's called from the program entry point, usually towards the end. There's also usually a test against the return value of main() to determine if anything other than zero was returned.
-  Second, its name may be preserved because it's imported from or exported by a DLL. For a developer to use a function from a DLL the developer needs to know and be able to resolve the name of the function they want. Because of this, the names have to stay intact. The DLL can expose its function names through the DLL/PE header, library file, or header file (.h or .hpp). The library and header files are not required, but they are usually included.
**Imports** are the functions the executable is using/importing from a DLL, and **exports** are the functions a DLL provides/exports. DLL's are known as dynamic-link libraries since they are loaded into memory once and can be loaded into any number of processes at any time without making any more copies. The Windows OS is built on DLLs.

**Modules** are essentially anything related to a process that import or export functions. For example, Loop.exe includes modules such as ntdll.dll, kernel32.dll, etc. If you were to run Loop.exe, while it is running Loop.exe itself is considered a module of the process.

C++ function overloading allows you to have two different functions with the same names that take different parameters. This becomes a problem when a DLL is exporting functions since the exported names will be the same. For developers, this problem is solved by using libraries and header files. On a lower level, this problem is solved by mangling the names so they are unique. _**ALL**_ exported **C++** function names get mangled whether they have overrides or not.

Function mangling is also called function decoration, which is probably a more appropriate name just not as popular. Although the mangled names may look like random garbage, there is a method to the madness. Here is an example of a mangled function name: `??0?$_Yarn@D@std@@QEAA@PEBD@Z`. As random as it may seem, it can be decoded. By de-mangling the name you can find the function type and parameter types. Different compilers use different mangling schemes, in this series of rooms everything uses the Microsoft C++ compiler and mangling scheme. You don't need to know how the schemes work since reverse engineering tools can decode them, but if you'd like here are some links.  

Microsoft C++ Mangling Scheme: [http://mearie.org/documents/mscmangle/](http://mearie.org/documents/mscmangle/)  
More Mangling Schemes: [https://en.wikipedia.org/wiki/Name_mangling](https://en.wikipedia.org/wiki/Name_mangling)

Side note for the programmers out there. Putting `extern "C"` before a function makes it use C linkage, thus removing the name mangling. This does prevent you from overloading the function.

#### Running DLL

When reverse engineering a DLL you may want to run it so you can analyze it in a debugger. This presents an obvious problem, you can't simply run a DLL. Here's a bit more detail on how DLLs work.

When a DLL is loaded, the function DllMain() is executed within the context of the process which loads the DLL. Here the DLL can run whatever code it wants.

You may have heard of DLL injection, this is one way it can be done. You can get the target process to call LoadLibrary() on your DLL which will cause DllMain() within your DLL to be executed within the context of the target process.

There's a program that comes with Windows called rundll32.exe which does pretty much that, it just loads your DLL making DllMain() execute. As a developer, you can make rundll32.exe execute functions within the DLL, but I don't think anyone does this.

Here are some places you can learn more about IDA:

- [https://www.youtube.com/playlist?list=PLKwUZp9HwWoDDBPvoapdbJ1rdofowT67z](https://www.youtube.com/playlist?list=PLKwUZp9HwWoDDBPvoapdbJ1rdofowT67z)
- [https://www.youtube.com/watch?v=tt15P5Om3Zg](https://www.youtube.com/watch?v=tt15P5Om3Zg)[](https://www.youtube.com/watch?v=tt15P5Om3Zg)
- [https://hex-rays.com/products/ida/tech/flirt/in_depth/](https://hex-rays.com/products/ida/tech/flirt/in_depth/)

If you have the time I'd recommend looking into Ghidra and, if you plan on sticking with Windows, x64dbg. Ghidra is a great alternative to IDA, just not as mature. The nicest thing about Ghidra over IDA is the price. Ghidra is free, IDA is expensive. So far we've been using IDA Freeware which is great but there are some serious limitations. With a price tag of free, Ghidra supports loads of architectures and is written in Java so it runs on pretty much anything. Its decompiler is pretty good, I do think the decompiler IDA has is better though.