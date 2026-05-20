# Cybersecurity Research & Learning Lab

A comprehensive repository of cybersecurity notes, lab environments, Red Team exercises, and SOC Analyst training materials. This repository tracks my journey through various platforms including TryHackMe, PortSwigger Academy, and Blue Team Labs Online.

## 📁 Repository Structure

### 1. [🧪 Labs](https://www.google.com/url?sa=E&q=./labs)

Contains hands-on environments and source code for vulnerability testing.

- **Chained-Trust:** A web-based lab environment featuring a Node.js server (server.js) designed to test trust relationships and file upload vulnerabilities.

### 2. [📓 Notes-Public](https://www.google.com/url?sa=E&q=./Notes-Public)

A massive library of research and study guides categorized by domain:

- **AI Hacking:** Notes on hacking AI models and prompt engineering (Updated for 2025/2026 landscapes).
- **Blue Team:** Resources for SIEM tools, Digital Forensics, Incident Response, and Threat Intel.
- **Bug Bounty Hunter:** Automation scripts, reconnaissance techniques, and write-ups from HackerOne/Bugcrowd.
- **IoT:** Specific focus on MikroTik RouterBoard configuration and security.
- **TryHackMe:** Organized by Learning Path:
    
    - SOC L1 & L2: Logging, Splunk, TShark, and Traffic Analysis.
    - CTF: Write-ups for boxes like Blueprint, Pyrat, and GeoServer.
    - Cyber Advent: Notes from the 2025/2026 seasonal events.
- **Portswigger Academy:** Focused on SQL Injection (Blind, Union, and Logic subversion).
    

### 3. [🔴 Red Team Docs](https://www.google.com/url?sa=E&q=./Red_Team_Docs)

Documentation for offensive operations and CTF competitions.

- **Scripts:** Custom Python/Bash scripts for flag retrieval, Diffie-Hellman decryption, and port scanning.
- **PicoCTF:** Targeted notes on Reverse Engineering and Web Exploitation.
- **90-Day Plan:** A structured cybersecurity roadmap.

### 4. [🛡️ SOC Analyst](https://www.google.com/url?sa=E&q=./SOC%20Analyst)

Materials related to defensive security and Blue Team operations.

- **BTLabs:** Phishing analysis (EML files), Network Analysis (PCAPNG), and Ransomware investigation.
- **Reference:** Windows Forensics cheatsheets and Snort rule guides.
- **Career:** Recruitment tasks and report-writing examples.

### 5. [🛠️ THM-Documents](https://www.google.com/url?sa=E&q=./THM-documents)

Working files used during TryHackMe rooms.

- **Exploits/Tools:** MD5 collision tools (fastcoll), brute-force scripts (brutus.py), and OpenVPN troubleshooting.
- **Artifacts:** Logs, SSH keys (id_rsa), and steganography samples.

---

## 🚀 Getting Started

### Prerequisites

- **Markdown Viewer:** Best viewed in [Obsidian](https://www.google.com/url?sa=E&q=https%3A%2F%2Fobsidian.md%2F) or VS Code (many notes contain embedded images).
- **Lab Environment:** To run the chained-trust lab:
    ```bash
    cd labs/chained-trust
    npm install
    node server.js
    ```

### Key Topics Covered

|                    |                                                        |
| ------------------ | ------------------------------------------------------ |
| Domain             | Focus Area                                             |
| **Web Sec**        | IDOR, SSRF, SQLi, XSS, Broken Access Control           |
| **Defensive**      | Splunk, Snort, TShark, Log Analysis, Phishing Analysis |
| **Scripting**      | Python (Exploits), Bash (Automation), Node.js (Labs)   |
| **Infrastructure** | MikroTik, AWS S3 Security, Active Directory            |

---

## 🛡️ Ethical Disclosure

This repository is for educational purposes only. All techniques and scripts were tested in controlled environments or authorized bug bounty programs. **Never use these tools on systems you do not have explicit permission to test.**