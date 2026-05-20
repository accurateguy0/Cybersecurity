We are committed to protecting the interests of Security Researchers. The more closely your behavior follows these rules, the more we’ll be able to protect you if a difficult situation escalates.

Rules can vary for each program. Please carefully read the program brief for specific rules. These rules apply to all programs:

- Testing should be performed only on systems listed under the program brief ‘Targets’ section. Any other systems are Out Of Scope.
- Except when otherwise noted in the program brief, you should create accounts for testing purposes.
- Submissions must be made exclusively through Crowdcontrol to be considered for a reward.
- Communication regarding submissions must remain within Crowdcontrol and/or official Bugcrowd support channels for the duration of the disclosure process.
- Actions which affect the integrity or availability of program targets are prohibited and strictly enforced. If you notice performance degradation on the target systems, you must immediately suspend all use of automated tools.
- Submissions should have impact to the target’s security posture. Impact means the reported issue affects the target’s users, systems, or data security in a meaningful way. Submitters may be asked to defend the impact in order to qualify for a reward.
- Submissions may be closed if a Researcher is non-responsive to requests for information after 7 days.
- The existence or details of private or invitation-only programs must not be communicated to anyone who is not a Bugcrowd employee or an authorized employee of the organization responsible for the program.
- We encourage Researchers to include a video or screenshot Proof-of-Concept in their submissions. These files should not be shared publicly. This includes uploading to any publicly accessible websites (i.e. YouTube, Imgur, etc.). If the file exceeds 100MB, upload the file to a secure online service such as Vimeo, with a password. For more details, please refer to our [Reporting a Bug](https://docs.bugcrowd.com/researchers/reporting-managing-submissions/reporting-a-bug/) documentation.
- Bugcrowd’s Disclosure policies apply to all submissions made through the Bugcrowd platform, including Duplicates, Out of Scope, and Not Applicable submissions. Customers may select Nondisclosure, Coordinated Disclosure, or Custom Disclosure policies to be applied to their program brief. Please refer to our [Additional Disclosure Policies](https://docs.bugcrowd.com/researchers/disclosure/disclose-io-and-safe-harbor/) for details on the different Public Disclosure Policies at Bugcrowd.
- If a Researcher wants to retain disclosure rights for vulnerabilities that are out of scope for a bounty program, they should report the issue to the Program Owner directly. Bugcrowd can assist Researchers in identifying the appropriate email address to contact. Program Owners are encouraged to ensure their program scope includes all critical components they wish to receive vulnerability reports for.
- Violation of a program’s stated disclosure policy may result in enforcement action, as outlined in the Enforcement Actions section of the [Platform Behavior Standards](https://www.bugcrowd.com/resources/hacker-resources/platform-behavior-standards/).

### Common “Non-qualifying” Submission Types

Some submission types do not qualify for a reward because they have low security impact to the program owner, and thus, do not trigger a code change. This section contains a listing of issues found to be commonly reproducible and reported but are often ineligible. We strongly suggest you do not report these issues unless you can demonstrate a chained attack with higher impact.

- Descriptive error messages (e.g. Stack Traces, application or server errors).
- HTTP 404 codes/pages or other HTTP non-200 codes/pages.
- Banner disclosure on common/public services.
- Disclosure of known public files or directories, (e.g. robots.txt).
- Clickjacking and issues only exploitable through clickjacking.
- CSRF on forms that are available to anonymous users (e.g. the contact form).
- Logout Cross-Site Request Forgery (logout CSRF).
- Presence of application or web browser ‘autocomplete’ or ‘save password’ functionality.
- Lack of Secure and HTTPOnly cookie flags.
- Lack of Security Speedbump when leaving the site.
- Weak Captcha / Captcha Bypass
- Username enumeration via Login Page error message
- Username enumeration via Forgot Password error message
- Login or Forgot Password page brute force and account lockout not enforced.
- OPTIONS / TRACE HTTP method enabled
- SSL Attacks such as BEAST, BREACH, Renegotiation attack
- SSL Forward secrecy not enabled
- SSL Insecure cipher suites
- The Anti-MIME-Sniffing header X-Content-Type-Options
- Missing HTTP security headers, specifically (https://blog.veracode.com/2014/03/guidelines-for-setting-security-headers/)