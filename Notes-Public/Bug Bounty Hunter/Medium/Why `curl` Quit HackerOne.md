# 

[

![Abhishek meena](https://miro.medium.com/v2/resize:fill:32:32/1*g4tYjgpvB52xwZPNMcvefg.png)





](https://medium.com/@Aacle?source=post_page---byline--526a05e12289---------------------------------------)

[Abhishek meena](https://medium.com/@Aacle?source=post_page---byline--526a05e12289---------------------------------------)

Follow

2 min read

·

Feb 17, 2026

74

2

**Daniel Stenberg**, the creator of `curl`, recently made waves by removing the project from **HackerOne**. This wasn't because `curl` became insecure; it’s because the project was being buried under "AI slop"—automated, hallucinated bug reports that wasted the team’s limited time.

## The Hallucination Problem

The issue isn’t that AI finds bugs; it’s that AI _invents_ them. Stenberg shared examples where researchers submitted reports that were technically impossible:

- **The “Self-Inflicted” Bug**: One reporter claimed a **Use-After-Free** vulnerability but provided a Proof of Concept (PoC) where they manually freed the memory themselves before using it.
- **The Ignored Guard Clause**: Another report flagged a “dangerous” `strcpy` function, completely ignoring the `if` statement directly above it that prevented any overflow. When challenged, the AI-driven response simply doubled down on the error.

Free Read : [Click](https://medium.com/@Aacle/why-curl-quit-hackerone-526a05e12289?sk=1508e1c15884520c490db64e02cb0a9f)

## Signal vs. Noise

Elite researcher **Sean Heeland** noted that using advanced AI for deep security research often results in a **1-to-50 signal-to-noise ratio**. For every one real bug, there are 50 hallucinations.

Under the **Bugcrowd VRT**, memory corruption like **Remote Code Execution (RCE)** is a **Priority 1** issue. However, when “researchers” forward 50 fake P1s to a maintainer without checking them, they aren’t helping — they are performing a Denial-of-Service attack on the maintainer’s schedule.

## The Takeaway for the Community

AI is a powerful assistant, but it is a terrible pilot.

1. **Verify Every PoC**: If you can’t explain why the code is vulnerable without quoting an LLM, don’t report it.
2. **Respect the Maintainers**: Open-source legends like the `curl` team are often volunteers. Don't make them your personal AI-triage service.
3. **Think Before You Prompt**: Use AI to write fuzzing harnesses or explain complex logic, not to guess at vulnerabilities.

If we keep sending “slop,” we will lose more than just the `curl` program—we’ll lose the trust that makes bug bounties work.