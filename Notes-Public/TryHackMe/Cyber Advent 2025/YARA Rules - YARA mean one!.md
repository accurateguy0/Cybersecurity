In what situations might defenders rely on this tool?

- **Post-incident analysis**: when the security team needs to verify whether traces of malware found on one compromised host still exist elsewhere in the environment.
- **Threat Hunting**: searching through systems and endpoints for signs of known or related malware families.
- **Intelligence-based scans**: applying shared YARA rules from other defenders or kingdoms to detect new indicators of compromise.
- **Memory analysis**: examining active processes in a memory dump for malicious code fragments.
A YARA rule is built from several key elements:

- **Metadata**: information about the rule itself: who created it, when, and for what purpose.
- **Strings**: the clues YARA searches for: text, byte sequences, or regular expressions that mark suspicious content.
- **Conditions**: the logic that decides when the rule triggers, combining multiple strings or parameters into a single decision.

Here’s how it looks in practice:

```php
rule TBFC_KingMalhare_Trace
{
    meta:
        author = "Defender of SOC-mas"
        description = "Detects traces of King Malhare’s malware"
        date = "2025-10-10"
    strings:
        $s1 = "rundll32.exe" fullword ascii
        $s2 = "msvcrt.dll" fullword wide
        $url1 = /http:\/\/.*malhare.*/ nocase
    condition:
        any of them
}
```

**Strings**

As mentioned earlier, strings are the clues that YARA searches for when scanning files, memory, or other data sources.  
They represent the signatures of malicious activity in fragments of text, bytes, or patterns that can reveal the presence of King Malhare's code. In YARA, there are three main types of strings, each with its own purpose. Let’s talk about them and see how they can help defend the kingdom of TBFC.  
  
**Text strings  
**Text strings are the simplest and most common type used in YARA rules. They represent words or short text fragments that might appear in a file, script, or memory. By default, YARA treats text strings as ASCII and case-sensitive, but you can modify how they behave using special modifiers - small keywords added after the string definition. The example below shows a simple rule that searches for the word **Christmas** inside a file:

```php
rule TBFC_KingMalhare_Trace
{
    strings:
        $TBFC_string = "Christmas"

    condition:
        $TBFC_string 
}
```

Sometimes, attackers like King Malhare try to hide their code by changing how text looks inside a file - using encoding, case tricks, or even encryption. YARA helps defenders counter these obfuscation methods with a few powerful modifiers that extend the capabilities of text strings:

- **Case-insensitive strings - nocase  
    **By default, YARA matches text exactly as written. Adding the `nocase` modifier makes the match ignore letter casing, so "Christmas", "CHRISTMAS", or "christmas" will all trigger the same result.

```php
strings:
    $xmas = "Christmas" nocase
```

- **Wide-character strings - wide, ascii**  
    Many Windows executables use two-byte Unicode characters. Adding `wide` tells YARA to also look for this format, while `ascii` enforces a single-byte search. You can use both together:

```php
strings:
    $xmas = "Christmas" wide ascii
```

- **XOR strings - xor  
    **Malhare's agents often XOR-encode text to hide it from scanners. Using the `xor` modifier, YARA automatically checks all possible single-byte XOR variations of a string - revealing what attackers tried to conceal.

```php
strings:
    $hidden = "Malhare" xor
```

- **Base64 strings - base64, base64wide**  
    Some malware encodes payloads or commands in Base64. With these modifiers, YARA decodes the content and searches for the original pattern, even when it’s hidden in encoded form.

```php
strings:
    $b64 = "SOC-mas" base64
```

Each of these modifiers makes your rule smarter and more resilient, ensuring that even when King Malhare disguises his code, the defenders of TBFC can still uncover the truth.  
  
**Hexadecimal strings  
**Sometimes, King Malhare's code doesn't leave readable words behind; instead, it hides in raw bytes deep inside executables or memory. That's when hexadecimal strings come to the rescue. Hex strings allow YARA to search for specific byte patterns, written in hexadecimal notation. This is useful when defenders need to detect malware fragments like file headers, shellcode, or binary signatures that can't be represented as plain text.

```php
rule TBFC_Malhare_HexDetect
{
    strings:
        $mz = { 4D 5A 90 00 }   // MZ header of a Windows executable
        $hex_string = { E3 41 ?? C8 G? VB }

    condition:
        $mz and $hex_string
}
```

**  
Regular expression strings  
**Not all traces of King Malhare's malware follow a fixed pattern. Sometimes, his code mutates, small changes in file names, URLs, or commands make it harder to detect using plain text or hex strings. That's where regular expressions come in. Regex allows defenders to write flexible search patterns that can match multiple variations of the same malicious string.  
It's especially useful for spotting URLs, encoded commands, or filenames that share a structure but differ slightly each time.

```php
rule TBFC_Malhare_RegexDetect
{
    strings:
        $url = /http:\/\/.*malhare.*/ nocase
        $cmd = /powershell.*-enc\s+[A-Za-z0-9+/=]+/ nocase

    condition:
        $url and $cmd
}
```

**Match a single string**  
The simplest condition, the rule triggers if one specific string is found. For example, the variable xmas.

```php
condition:
    $xmas
```

**Match any string  
**When multiple strings are defined, the rule can be configured to trigger as soon as any one of them is found:

```php
condition:
    any of them
```

This approach is useful for detecting early signs of compromise; even a single matching clue can be enough to raise attention.  
  
**Match all strings  
**To make the rule stricter, you can require that all defined strings appear together:

```php
condition:
    all of them
```

This approach reduces false positives; YARA will only flag a file if every indicator matches.

**Combine logic using: and, or, not  
**Defenders often need more control over how rules behave. Logical operators let you combine multiple checks into one condition, just like building a small defensive strategy.

```php
condition:
    ($s1 or $s2) and not $benign
```

This means the rule will trigger if either $s1 or $s2 is found, but not $benign. In other words: detect suspicious code, but ignore harmless system files.  
  
**Use comparisons like: filesize, entrypoint, or hash  
**YARA can also check file properties, not just contents. For example, you can detect files that are unusually small or large, a common trick used by King Malhare to disguise his payloads.

```php
condition:
    any of them and (filesize < 700KB)
```


We can use the `man yara` command to find out what flags could be useful in our scenario, and we find the following:

- `-r` - Allows YARA to scan directories recursively and follow symlinks
- `-s` - Prints the strings found within files that match the rule
[regex101: build, test, and debug regex](https://regex101.com/)
