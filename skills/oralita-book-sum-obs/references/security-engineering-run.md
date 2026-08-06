# Security Engineering Run Log

**Book:** Security Engineering 3rd Ed by Ross Anderson (1212pp, 9.1 MB)
**Target:** `F:\obsidian_note\swe-knowledge\software-engineering-note\13_Software_Security\`

| Metric | Value |
|--------|-------|
| Source size | 1,270,589 chars from 5 chapter groups |
| Output files | 5 files |
| Total size | 101 KB |
| Batches | 2 (3+2 tasks) |
| Duration | ~6 minutes |
| Wikilinks fixed | All checked - files from batch 2 already had wikilinks |

## Book Selection

User had only one book for this KA — *Security Engineering* by Anderson is the definitive reference. No comparison needed. Focused on software-relevant chapters (1-11, 21, 27-28) and skipped physical security chapters (locks, seals, nuclear C&C, security printing, biometrics).

## Structure

5 summary files covering the essential security topics for SWEBOK KA 13:

| File | Anderson Chapters | Key Content |
|---|---|---|
| 01_Security_Fundamentals | 1-3, 8 | Framework, opponent taxonomy, psychology/usability, economics |
| 02_Protocols_and_Cryptography | 4-5 | Authentication protocols, symmetric/asymmetric crypto, TLS |
| 03_Access_Control_and_Architecture | 6-7, 9-10 | ACLs/capabilities, OS security, MLS, distributed systems, inference control |
| 04_Network_Attack_and_Defence | 21 | DDoS, BGP, DNS security, malware, firewalls, IDS |
| 05_Secure_Development_and_Assurance | 27-28 | SSDLC, threat modeling, DevSecOps, Common Criteria |

## Notable Decisions

- **Skipped physical security chapters** (13-17, 19, 22-24): locks, alarms, nuclear C&C, biometrics, tamper resistance, phones, electronic warfare, DRM. These are systems engineering topics, not software security.
- **Ch 11 (Inference Control) was not in the extracted text** — source file ended at Ch 10. The note covers what was available.
- **Existing Cybersecurity folder preserved** — overview updated to add Anderson section alongside existing Cybersecurity content.

## Overview Update

Updated `Software Security Overview.md`:
- Added "Security Engineering (Anderson)" section with 5 file wikilinks
- Removed "What's Missing" section
- Preserved existing "Applied Security → Cybersecurity" section
