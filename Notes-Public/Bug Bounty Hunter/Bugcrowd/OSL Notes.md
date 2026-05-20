OSL is Asia’s leading stablecoin trading and payment infrastructure. 


# Ratings/Rewards  
For the initial prioritization/rating of findings, this engagement will use the Bugcrowd Vulnerability Rating Taxonomy. 

# Target Scope
[https://www.osl.com/hk-en](https://www.google.com/url?sa=E&q=https%3A%2F%2Fwww.osl.com%2Fhk-en)
[https://www.osl.com/en](https://www.google.com/url?sa=E&q=https%3A%2F%2Fwww.osl.com%2Fen)


While your subfinder command will find many subdomains (e.g., api.osl.com, dev.osl.com, etc.), you must be careful. **The Risk:** Often, if a program lists specific URLs like www.osl.com/hk-en rather than *.osl.com, they are running a **narrow scope** program. 
- If you use subfinder and find dev.osl.com or api-test.osl.com, and you test them, you will likely be **disqualified**.
- **Why?** The policy explicitly lists **"Staging and development environments"** as **Out of Scope**. Subdomain discovery often leads directly to these forbidden environments.
The policy says: **"Out of Scope: Use of automated scanners without prior approval."**
- While subfinder is a reconnaissance tool, if you follow it up with an automated vulnerability scanner (like Nuclei, Nikto, or Burp Suite’s active scanner), you are violating the policy.
You mentioned using subfinder. Usually, researchers use this to find Subdomain Takeovers (pointing to a dead GitHub page, S3 bucket, etc.).
- **The Policy says:** "Excluded: Subdomain takeover on **unused** subdomains."
- This means if you find an old, forgotten subdomain and prove you can take it over, they will mark it as "Informational" (P5) or "N/A" and **will not pay you.**

Your commands (naabu, httpx, aquatone) are designed for **Wide Scope** (testing every subdomain). However, the policy you shared is a **Narrow Scope**.

Since the program explicitly excludes https://www.osl.com/id-id and focuses on /hk-en and /en, you should filter your results immediately.
**Update your URL gathering:**

```bash
# Set target to the specific domain
TARGET="www.osl.com"

# Gather URLs and filter for only the In-Scope paths
gau $TARGET --threads 5 | grep -E "/hk-en|/en" | sort -u | anew all_urls.txt
waybackurls $TARGET | grep -E "/hk-en|/en" | sort -u | anew wayback_urls.txt
```

Since the tech stack is listed as NextJS/React, look for exposed API keys in the client-side JS bundles or _next/data routes. 
#### The gf patterns (XSS, SQLi, etc.)

- **Effectiveness:** Very high.
- **Note:** Since the site uses **NextJS/ReactJS**, traditional SQLi is rare. You should prioritize **XSS** and **Open Redirects**.
- **Pro-Tip:** Look for _next/data/ URLs in your params.txt. These often contain JSON data used for page rendering and are prime spots for IDORs or data leaks.

#### The katana command (Crawling)

- **The Risk:** katana is an active crawler. The policy states: "Use of automated scanners without prior approval" is out of scope.
- **How to stay safe:** If you use Katana, keep the rate limit low.
```bash
katana -u https://www.osl.com/hk-en -js-crawl -d 3 -rl 10 -silent
```

#### The JS Secret Search (The while read loop)
```bash
cat js_files.txt | while read url; do curl -s "$url" | grep -E "(api_key|apikey|secret|token|password|passwd|auth|bearer|AWS|S3|firebase)" ; done
```
- **Effectiveness:** Very High for this target.
- **NextJS specific:** Look for .map files (source maps). If they left source maps enabled, you can reconstruct the original source code, making it much easier to find logic flaws.
- **Improvement:** Instead of just grep, try using a specialized tool like **nuclei** with "exposed-panels" and "token-spray" templates, or **mantra** to find secrets in JS.
### Missing Logic for this Policy

**A. Rate Limiting (Wait! Be careful)**  
The policy says: "Rate limiting bypass attempts" are **Excluded**.

- **Action:** If you find a login or OTP page, **do not** try to brute force it. They will mark it as P5/Excluded.

**B. Post-Exploitation**  
The policy says: "If you believe you've identified a vulnerability... please stop testing and submit."

- **Action:** If your gf sqli leads to a working injection, do not try to dump the whole database. Just get the user() or version() and submit it immediately.

**Pro-Tip:** Since this is a **crypto/stablecoin platform**, the most valuable bugs are usually **Logic Flaws** in the "Trade" or "Wallet" sections. If you find an API endpoint in a JS file that looks like /api/v1/wallet/withdraw, investigate that very carefully!

**Try to find the "Site Manifest":**  
Look for these URLs in your browser:

- https://www.osl.com/_next/static/p7qRxvU3NcdgrtdceSnbE/_buildManifest.js
- https://www.osl.com/_next/static/p7qRxvU3NcdgrtdceSnbE/_ssgManifest.js
Inside these files, you will see a list of **every single page** on the website. If you find a page like /admin, /config, or /internal, you can try to visit it directly.
Nothing found.

### 4. Search for "Secrets" (The Automated Way)

Since you are already downloading JS files, you should search for API keys. You don't need to wait for Katana to finish if you already have a js_files.txt.

**Run this "Secret Searcher" now:**



```Bash
# Create a small script to find common secrets
cat << 'EOF' > find_secrets.sh
#!/bin/bash
while read url; do
    echo "Checking: $url"
    content=$(curl -s -L "$url")
    # Search for Google Keys, AWS, Secrets, and Internal OSL links
    echo "$content" | grep -Ei "AIza[0-9A-Za-z-_]{35}|secret[-_]key|access[-_]key|token:|bearer|auth|internal-api|dev-api|staging" >> raw_secrets.txt
done < js_files.txt
EOF

chmod +x find_secrets.sh
./find_secrets.sh
```

You previously found the Build ID: **p7qRxvU3NcdgrtdceSnbE**.

Since OSL is a financial site, they often have "Internal" or "Staff" routes that are hidden from the public but present in the JavaScript.

**Run this command to find the Site Map (Build Manifest):**

```Bash
curl -s "https://www.osl.com/_next/static/p7qRxvU3NcdgrtdceSnbE/_buildManifest.js" | grep -Eo "/[a-zA-Z0-9./_-]+" | sort -u
```
### 1. What is dx-sdk.js?

Looking at the code (specifically references to dingxiang-inc.com and constid), this is the **DingXiang Anti-Bot/Fingerprinting SDK**.

- **Purpose:** OSL uses this to identify your browser, check if you are a bot, and prevent "Account Takeover" (ATO) attacks.
    
- **What the code does:** It collects your canvasFP (Canvas Fingerprint), audioFP (Audio Fingerprint), webgl data, and ip.
    

**The Scope Warning:**  
Your Bugcrowd policy says **"Third party providers and services" are Out of Scope.** Since DingXiang is a third-party security vendor, a bug inside this script (like an XSS in the SDK itself) would likely be rejected by OSL as "not their bug."

**HOWEVER:** If OSL has hardcoded **their own** secret keys inside the configuration of this script, that **is** a valid finding.

###  Check for Information Disclosure in the Headers

```Bash
curl -I -s https://www.osl.com/hk-en
```
**Look for:**

- X-Powered-By: Does it show a specific version of Next.js or Node.js?
- Server: Does it show a version of Nginx or Cloudflare that might have a CVE?
- **Missing Content-Security-Policy:** If they are a financial site and have a weak CSP, you can report it as a "Security Misconfiguration" (P4).
### Summary of your next move:

1. **Stop** looking at dx-sdk.js (it’s third-party).
2. **Stop** looking at the root of web-static-glb.osl.com (it's a locked S3 bucket).
3. **Focus** on the **_buildManifest.js** file. If you can find a hidden page that isn't linked on the main site, that is your best chance for a bounty.
###  Finding: Internal Hostname Leak (P4/Informational)

Look at this header:  
link: <http://www-web-osl.prod.osl-internal.com/hk-en>; rel="alternate"...
- **What it is:** The server is leaking the internal DNS name used inside their private network: www-web-osl.prod.osl-internal.com.
- **Why it matters:** While you can't access an .internal domain from the internet, this confirms they are using **Envoy** (seen in x-envoy-upstream-service-time) to proxy requests to internal microservices.
- **Action:** This is usually a **P4 (Low)** finding on Bugcrowd. It is called **"Internal IP/Hostname Disclosure."**

### 4. Analyze the CSP (Broken Link Hijacking)

The Content Security Policy (CSP) is massive. It lists many third-party domains.

- **Strategy:** Check if any of those domains (especially the ada.support or osltest.com ones) are available for registration.
- **If you can take over a domain listed in their CSP**, you can bypass their security headers to perform a Stored XSS. This is a **P2/P3 bug**.

### 5. AWS Infrastructure Leak

The cookie set-cookie: AWSALB=... confirms they are using an **Amazon Web Services (AWS) Application Load Balancer**.

- This tells you the backend is likely running in **AWS EC2 or EKS (Kubernetes)**.
- Since you know they use AWS, you can try to look for exposed S3 buckets or AWS-specific misconfigurations (though this is harder with Cloudflare in the way).

### Your Next "Big" Move (In-Scope Logic)

Since the subdomains and staging are out of scope, and the automated scans are empty, you must look for **Business Logic Flaws** on the hk-en site.

**Try this on https://www.osl.com/hk-en:**

1. **Look for the "Sign Up" flow:**
    - Is there a way to register an account with a "disposable" email?
    - During registration, intercept the request in Burp Suite/Network Tab. Look for extra parameters like role: "user". Try changing it to role: "admin".
2. **Look at the "Perspectives" / Blog section:**
    
    - You saw a URL like .../insights/osl-community-ambassdor/.
    - Try **XSS** in the search bar or comments if they exist.
    - Try **Parameter Pollution**: ?slug=test&slug=another-test.
3. **Check for "Directory Traversal" in the _next/data routes:**
    
    - You found: /_next/data/[BUILD-ID]/hk-en/perspectives/insights/[SLUG].json
    - Try replacing [SLUG] with ../../../../etc/passwd or ..%2f..%2f..%2fconfig. It likely won't work, but it's a standard check for Next.js apps

### Step 2: Manual Recon (The "Detective" Walk)

Don't run tools yet. Just look at the site.

1. **Browse:** Go to https://www.osl.com/hk-en.
2. **Inspect Source:** Right-click anywhere on the page -> **View Page Source**.
3. **Find the Build ID:** Press Ctrl+F and search for /_next/static/. You will see a long random string (e.g., p7qRxvU3...). **Copy this string.** This is the key to finding hidden files.

|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| https://web-static-hk.osl.com/web-osl/_next/static/chunks/2972-ea60c007e9ce3c35.js](https://web-static-hk.osl.com/web-osl/_next/static/chunks/2972-ea60c007e9ce3c35.js https://web-static-hk.osl.com/web-osl/_next/static/chunks/745-63bdb057c4c1f613.js](https://web-static-hk.osl.com/web-osl/_next/static/chunks/745-63bdb057c4c1f613.js)" async=""></script><script src="[https://web-static-hk.osl.com/web-osl/_next/static/chunks/260205ab3f3.js](https://web-static-hk.osl.com/web-tatic/chunks/2603-033a97b8205ab3f3.js)" async=""></script><script src="[https://web-static-hk.osl.com/web-osl/_next/static/chunks/8310-f2ce049f4c67104b.js](https://web-static-hk.osl.com/web-osl/_next/static/chunks/8310-f2ce049f4c67104b.js)" async=""></script><script src="[https://web-static-hk.osl.com/web-osl/_next/static/chunks/9352-796e06d77793b0b7.js](https://web-static-hk.osl.com/web-osl/_next/static/chunks/9352-796e06d77793b0b7.js)" async=""></script><script src="[https://web-static-hk.osl.com/web-osl/_next/static/chunks/8459-55416e841db96c6a.js](https://web-static-hk.osl.com/web-osl/_next/static/chunks/8459-55416e841db96c6a.js)" async=""></script><script src="[https://web-static-hk.osl.com/web-osl/_next/static/chunks/1021-22e52d66dcda338f.js](https://web-static-hk.osl.com/web-osl/_next/static/chunks/1021-22e52d66dcda338f.js)" async=""></script><script src="[https://web-static-hk.osl.com/web-osl/_next/static/chunks/9576-97f48d06821fc468.js](https://web-static-hk.osl.com/web-osl/_next/static/chunks/9576-97f48d06821fc468.js)" async=""></script><script src="[https://web-static-hk.osl.com/web-osl/_next/static/chunks/2732-e1cd6c13e6328e49.js](https://web-static-hk.osl.com/web-osl/_next/static/chunks/2732-e1cd6c13e6328e49.js)" async=""></script><script src="[https://web-static-hk.osl.com/web-osl/_next/static/chunks/9545-f90ed8f885a37b8e.js](https://web-static-hk.osl.com/web-osl/_next/static/chunks/9545-f90ed8f885a37b8e.js)" async=""></script><script src="[https://web-static-hk.osl.com/web-osl/_next/static/chunks/8224-b327cdede7ebbca6.js](https://web-static-hk.osl.com/web-osl/_next/static/chunks/8224-b327cdede7ebbca6.js)" async=""></script><script src="[https://web-static-hk.osl.com/web-osl/_next/static/chunks/7287-584c371ae58468eb.js](https://web-static-hk.osl.com/web-osl/_next/static/chunks/7287-584c371ae58468eb.js)" async=""></script><script src="[https://web-static-hk.osl.com/web-osl/_next/static/chunks/9823-64e43769c13cf408.js](https://web-static-hk.osl.com/web-osl/_next/static/chunks/9823-64e43769c13cf408.js)" async=""></script><script src="[https://web-static-hk.osl.com/web-osl/_next/static/chunks/9133-8c6d57c8ba1d5fdf.js](https://web-static-hk.osl.com/web-osl/_next/static/chunks/9133-8c6d57c8ba1d5fdf.js)" async=""></script><script src="[https://web-static-hk.osl.com/web-osl/_next/static/chunks/9893-92c8ac39d3a4ea07.js](https://web-static-hk.osl.com/web-osl/_next/static/chunks/9893-92c8ac39d3a4ea07.js)" async=""></script><script src="[https://web-static-hk.osl.com/web-osl/_next/static/chunks/9-d75f635e2845f83e.js](https://web-static-hk.osl.com/web-osl/_next/static/chunks/9-d75f635e2845f83e.js)" async=""></script><script src="[https://web-static-hk.osl.com/web-osl/_next/static/chunks/4016-96c57fc9b3e65d37.js](https://web-static-hk.osl.com/web-osl/_next/static/chunks/4016-96c57fc9b3e65d37.js)" async=""></script><script src="[https://web-static-hk.osl.com/web-osl/_next/static/chunks/3260-7427b37e59db75cf.js](https://web-static-hk.osl.com/web-osl/_next/static/chunks/3260-7427b37e59db75cf.js)" async=""></script><script src="[https://web-static-hk.osl.com/web-osl/_next/static/chunks/8485-cbc7f803ec16fafd.js](https://web-static-hk.osl.com/web-osl/_next/static/chunks/8485-cbc7f803ec16fafd.js)" async=""></script><script src="[https://web-static-hk.osl.com/web-osl/_next/static/chunks/4161-5aee91976da00e01.js](https://web-static-hk.osl.com/web-osl/_next/static/chunks/4161-5aee91976da00e01.js)" async=""></script><script src="[https://web-static-hk.osl.com/web-osl/_next/static/chunks/5063-30dde9034441e9dc.js](https://web-static-hk.osl.com/web-osl/_next/static/chunks/5063-30dde9034441e9dc.js)" async=""></script><script src="[https://web-static-hk.osl.com/web-osl/_next/static/chunks/4444-a8d2ade4f074a794.js](https://web-static-hk.osl.com/web-osl/_next/static/chunks/4444-a8d2ade4f074a794.js)" async=""></script><script src="[https://web-static-hk.osl.com/web-osl/_next/static/chunks/8653-e6f7669c722b439a.js](https://web-static-hk.osl.com/web-osl/_next/static/chunks/8653-e6f7669c722b439a.js)" async=""></script><script src="[https://web-static-hk.osl.com/web-osl/_next/static/chunks/5938-41e97a831019f7f9.js](https://web-static-hk.osl.com/web-osl/_next/static/chunks/5938-41e97a831019f7f9.js)" async=""></script><script src="[https://web-static-hk.osl.com/web-osl/_next/static/chunks/8878-7952ad0ee490aff7.js](https://web-static-hk.osl.com/web-osl/_next/static/chunks/8878-7952ad0ee490aff7.js)" async=""></script><script src="[https://web-static-hk.osl.com/web-osl/_next/static/chunks/2071-09124a40a2e77141.js](https://web-static-hk.osl.com/web-osl/_next/static/chunks/2071-09124a40a2e77141.js)" async=""></script><script src="[https://web-static-hk.osl.com/web-osl/_next/static/chunks/app/%5Blocale%5D/page-67d86e844fd29b0b.js](https://web-static-hk.osl.com/web-osl/_next/static/chunks/app/%5Blocale%5D/page-67d86e844fd29b0b.js)" async=""></script><script src="[https://web-static-hk.osl.com/web-osl/_next/static/chunks/app/layout-9c0baa409dad6fee.js](https://web-static-hk.osl.com/web-osl/_next/static/chunks/app/layout-9c0baa409dad6fee.js)" async=""></script><script src="[https://web-static-hk.osl.com/web-osl/_next/static/chunks/5074-61fc7f84531c5b85.js](https://web-static-hk.osl.com/web-osl/_next/static/chunks/5074-61fc7f84531c5b85.js)" async=""></script><script src="[https://web-static-hk.osl.com/web-osl/_next/static/chunks/app/global-error-04745f644b2236ff.js](https://web-static-hk.osl.com/web-osl/_next/static/chunks/app/global-error-04745f644b2236ff.js)" async=""></script><script src="[https://web-static-hk.osl.com/web-osl/_next/static/chunks/3145-820f8af13165d29c.js](https://web-static-hk.osl.com/web-osl/_next/static/chunks/3145-820f8af13165d29c.js)" async=""></script><script src="[https://web-static-hk.osl.com/web-osl/_next/static/chunks/3423-d54fed0718c9975a.js](https://web-static-hk.osl.com/web-osl/_next/static/chunks/3423-d54fed0718c9975a.js)" async=""></script><script src="[https://web-static-hk.osl.com/web-osl/_next/static/chunks/9029-14648375fdcf828c.js](https://web-static-hk.osl.com/web-osl/_next/static/chunks/9029-14648375fdcf828c.js)" async=""></script><script src="[https://web-static-hk.osl.com/web-osl/_next/static/chunks/6137-01f7c5ccd62588a8.js](https://web-static-hk.osl.com/web-osl/_next/static/chunks/6137-01f7c5ccd62588a8.js)" async=""></script><script src="[https://web-static-hk.osl.com/web-osl/_next/static/chunks/4631-c13fb22245a72122.js](https://web-static-hk.osl.com/web-osl/_next/static/chunks/4631-c13fb22245a72122.js)" async=""></script><script src="[https://web-static-hk.osl.com/web-osl/_next/static/chunks/9035-d1feb6bdd130146d.js](https://web-static-hk.osl.com/web-osl/_next/static/chunks/9035-d1feb6bdd130146d.js)" async=""></script><script src="[https://web-static-hk.osl.com/web-osl/_next/static/chunks/6484-a01cf4f202e2d32e.js](https://web-static-hk.osl.com/web-osl/_next/static/chunks/6484-a01cf4f202e2d32e.js)" async=""></script><script src="[https://web-static-hk.osl.com/web-osl/_next/static/chunks/4260-3dea4fd11c1e4793.js](https://web-static-hk.osl.com/web-osl/_next/static/chunks/4260-3dea4fd11c1e4793.js)" async=""></script><script src="[https://web-static-hk.osl.com/web-osl/_next/static/chunks/app/%5Blocale%5D/layout-a486466213142104.js](https://web-static-hk.osl.com/web-osl/_next/static/chunks/app/%5Blocale%5D/layout-a486466213142104.js)" async=""></script><script src="[https://web-static-hk.osl.com/web-osl/_next/static/chunks/app/%5Blocale%5D/error-d53584cfb1be4734.js](https://web-static-hk.osl.com/web-osl/_next/static/chunks/app/%5Blocale%5D/error-d53584cfb1be4734.js)" async=""></script><script src="[https://web-static-hk.osl.com/web-osl/_next/static/chunks/8300-690037c431262925.js](https://web-static-hk.osl.com/web-osl/_next/static/chunks/8300-690037c431262925.js)" async=""></script><script src="[https://web-static-hk.osl.com/web-osl/_next/static/chunks/app/%5Blocale%5D/not-found-a57cd0b741c6871d.js]https://web-static-hk.osl.com/web-osl/_next/static/chunks/app/%5Blocale%5D/not-found-a57cd0b741c6871d.js |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
https://web-static-hk.osl.com/web-osl/_next/static/chunks/polyfills-78c92fac7aa8fdd8.js](https://web-static-hk.osl.com/web-osl/_next/static/chunks/polyfills-78c92fac7aa8fdd8.js

"verifyId":"50629b7e-ca4a-4519-8a4a-70c3902880cd","uuid":"70d7e175-40ba-4175-a86e-58b440f893da"

trace_id":"f89959e57180473aab06bb4f9b431340
"parent_span_id":"aed92f3c710d20ec


- **Jumio SDK Token:** You found token=6GTC327TW5D2TER3I7O6DJL6VU in META-INF.
    
    - Verdict: This is a license key for the Jumio KYC SDK. Usually, these are meant to be in the app. However, if you can use this token to access OSL's Jumio dashboard, it's a **P1**. (Highly unlikely, but keep it in your notes).

### Step 2: The "Broken CSP" Stored XSS

In your Sentry logs and CSP header, I see OSL trusts sentry.io and sentry.osl.com.

- **The Lead:** You found a Sentry "Internal Error" report.
- **The Theory:** If you can trigger an error (like a 404 or 500) and OSL's error page displays your input, you can bypass the Cloudflare WAF by using Sentry.
    
- **Baby Step:**
    1. Try to visit a page that doesn't exist: https://www.osl.com/hk-en/testing123
    2. Check the page. Does it say "Page testing123 not found"?
    3. If yes, try: https://www.osl.com/hk-en/{{7*7}}
    4. **The Goal:** If the page says "Page 49 not found", you found **Server-Side Template Injection (SSTI)**. This is a **P1 ($1,500)**.
it doesnt work unfortunately, the broken csp stored xss.

### 3. The "Native Library" lead (Step 4 from last time)

You ran strings on the .so files and found:  
-----BEGIN RSA PRIVATE KEY-----

**Baby Step:**

1. Run this command on your extracted APK folder:
    ```
    strings lib/*/*.so | grep -A 5 "BEGIN RSA PRIVATE KEY"
    ```
    
2. **The Goal:** Does it show a giant block of random letters (Base64) after that line?
    
    - **If YES:** You found a hardcoded private key. This is a **Critical P1**.
    - **If NO:** (If it just shows the header and nothing else), it is likely just a reference in the code and not the actual key.
 strings lib/*/*.so | grep -A 5 "BEGIN RSA PRIVATE KEY"
-----BEGIN RSA PRIVATE KEY-----
codecvt_byname<wchar_t, char, mbstate_t>::codecvt_byname failed to construct for
numpunct_byname<wchar_t>::numpunct_byname failed to construct for
locale not supported
stold
terminate_handler unexpectedly threw an exception
--
-----BEGIN RSA PRIVATE KEY-----
codecvt_byname<wchar_t, char, mbstate_t>::codecvt_byname failed to construct for
numpunct_byname<wchar_t>::numpunct_byname failed to construct for
locale not supported
stod
stold

a dead end?