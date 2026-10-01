import random


def mcq(qid, q, choices, answer):
    return {"id": qid, "type": "mcq", "q": q, "choices": choices, "answer": answer}


def fill(qid, q, answers):
    return {"id": qid, "type": "fill", "q": q, "answers": [a.lower().strip() for a in answers]}


def match(qid, q, pairs):
    return {
        "id": qid,
        "type": "match",
        "q": q,
        "pairs": [{"id": str(i), "left": a, "right": b} for i, (a, b) in enumerate(pairs)],
    }


CATEGORIES = [
    {
        "slug": "fundamentals",
        "title": "Cyber fundamentals",
        "blurb": "CIA triad, malware, hashing, and the words you hear on day one.",
        "difficulty": "simple",
        "minutes": 15,
    },
    {
        "slug": "phishing",
        "title": "Phishing & people",
        "blurb": "Urgency, fake IT, QR codes, and how a person is the first control.",
        "difficulty": "simple",
        "minutes": 15,
    },
    {
        "slug": "network",
        "title": "Network security",
        "blurb": "Packets, ports, ARP, DNS, and what a firewall actually does.",
        "difficulty": "medium",
        "minutes": 20,
    },
    {
        "slug": "soc",
        "title": "SOC floor",
        "blurb": "Alerts, SIEM, triage, and what you do before you wipe a box.",
        "difficulty": "medium",
        "minutes": 20,
    },
    {
        "slug": "identity",
        "title": "Identity & access",
        "blurb": "Least privilege, MFA, tokens, and accounts that should already be gone.",
        "difficulty": "medium",
        "minutes": 20,
    },
    {
        "slug": "web",
        "title": "Web applications",
        "blurb": "Injection, XSS, CSRF, and the mistakes that still land in production.",
        "difficulty": "hard",
        "minutes": 25,
    },
    {
        "slug": "cloud",
        "title": "Cloud security",
        "blurb": "Shared responsibility, keys, buckets, and identities in someone else's datacenter.",
        "difficulty": "hard",
        "minutes": 25,
    },
    {
        "slug": "incident",
        "title": "Incident response",
        "blurb": "Contain, preserve, notify — without burning the evidence.",
        "difficulty": "hard",
        "minutes": 25,
    },
]


BANK = {
    "fundamentals": [
        mcq("f1", "The CIA triad is:", ["Confidentiality, Integrity, Availability", "Crypto, IPS, Antivirus", "Cloud, Identity, Access", "Contain, Isolate, Archive"], 0),
        mcq("f2", "A hash is mainly used to:", ["Encrypt so you can decrypt later", "Check that data was not changed", "Assign IP addresses", "Block every payload by itself"], 1),
        mcq("f3", "Ransomware typically:", ["Defragments the disk", "Encrypts files and demands payment", "Patches the OS for you", "Turns the firewall into a helpdesk"], 1),
        mcq("f4", "HTTPS adds what HTTP does not:", ["A shorter URL", "Encryption and integrity in transit", "Free domains", "Unlimited bandwidth"], 1),
        mcq("f5", "Least privilege means an account should have:", ["Domain admin by default", "Only the rights needed for the job", "The shared team password", "Access after the person leaves"], 1),
        mcq("f6", "A worm is different from a typical virus because it:", ["Needs a human to click every copy", "Spreads on its own across the network", "Only steals screenshots", "Cannot run on Windows"], 1),
        mcq("f7", "Two-factor authentication is:", ["Two passwords on the same form", "Something you know plus something you have or are", "A longer password", "A VPN with no login"], 1),
        mcq("f8", "A firewall's basic job is to:", ["Encrypt every disk", "Allow or deny traffic based on rules", "Replace backups", "Train users"], 1),
        mcq("f9", "Availability is broken when:", ["Data is readable by anyone", "Data is quietly changed", "Systems cannot be used when needed", "Logs are hashed"], 2),
        mcq("f10", "A botnet is:", ["One laptop with many browsers", "Many compromised devices under one controller", "A legal CDN", "An air-gapped lab"], 1),
        mcq("f11", "Patching is mainly about:", ["Changing wallpaper", "Closing known software holes attackers reuse", "Buying a new firewall brand", "Deleting logs"], 1),
        mcq("f12", "Social engineering attacks:", ["Only hardware", "People and trust, not just code", "Only satellites", "Only air-gapped vaults"], 1),
        mcq("f13", "A VPN is meant to:", ["Make the office Wi-Fi public", "Protect traffic between you and a trusted network", "Replace MFA forever", "Stop all phishing"], 1),
        mcq("f14", "Integrity means:", ["Data stays secret", "Data stays accurate and unaltered", "The site stays up", "The password is long"], 1),
        mcq("f15", "Malware that spies and reports back is often called:", ["A compiler", "Spyware", "A load balancer", "A hypervisor"], 1),
        mcq("f16", "Defense in depth means:", ["One perfect control", "Several layers so one failure is not the whole loss", "No logging", "Only physical locks"], 1),
        mcq("f17", "A strong password is mainly:", ["Your pet plus 123", "Long, unique, and not reused", "Written on the monitor", "Shared in Slack"], 1),
        mcq("f18", "Zero trust assumes:", ["The office LAN is always safe", "Never trust, always verify — even inside", "VPN users need no MFA", "Guest Wi-Fi equals admin"], 1),
        fill("f19", "CIA: Confidentiality, Integrity, and ______.", ["availability"]),
        fill("f20", "MFA stands for ______-factor authentication.", ["multi", "multiple"]),
        fill("f21", "A ______ encrypts files and demands payment.", ["ransomware"]),
        fill("f22", "HTTPS runs HTTP over ______.", ["tls", "ssl", "tls/ssl"]),
        match("f23", "Match the idea to its meaning.", [("Confidentiality", "Keep data from the wrong eyes"), ("Integrity", "Keep data from being quietly changed"), ("Availability", "Keep systems usable when needed")]),
        match("f24", "Match the malware type.", [("Virus", "Needs a host file or action to spread"), ("Worm", "Spreads on its own"), ("Trojan", "Looks useful, hides harm")]),
        match("f25", "Match the control.", [("Firewall", "Filter network traffic"), ("Backup", "Recover after loss"), ("MFA", "Extra proof of who you are")]),
        mcq("f26", "Logging matters because:", ["It fills the disk for fun", "You cannot investigate what you never recorded", "It replaces encryption", "It stops every attack live"], 1),
        mcq("f27", "An air-gapped system is:", ["Always on the public internet", "Isolated from other networks on purpose", "A cloud region name", "A phishing kit"], 1),
        mcq("f28", "A default password on a camera is a risk because:", ["Vendors never publish them", "Attackers try known factory logins first", "Cameras cannot join Wi-Fi", "HTTPS forbids cameras"], 1),
        mcq("f29", "The safest place for a recovery backup is:", ["Only on the same encrypted share as production", "Tested and isolated from the live domain", "Emailed as zip files", "The recycle bin"], 1),
    ],
    "phishing": [
        mcq("p1", "An urgent email from “IT” asking you to paste your password is usually:", ["A normal reset", "Phishing / social engineering", "Two-factor", "A VPN install"], 1),
        mcq("p2", "The safest way to open a “bank” link in email is to:", ["Click it immediately", "Type the bank URL yourself or use the official app", "Forward it to the team", "Reply with your OTP"], 1),
        mcq("p3", "A lookalike domain like nethub-club.com instead of nethub.club is:", ["Always the official site", "A common phishing trick", "Required for HTTPS", "Proof of MFA"], 1),
        mcq("p4", "If a caller demands your one-time code “to keep the account”, you should:", ["Read the code aloud", "Hang up and use the official channel", "Text it to a coworker", "Post it in chat"], 1),
        mcq("p5", "QR phishing (quishing) works by:", ["Encrypting the disk", "Sending you to a site you did not type", "Patching Android", "Blocking SMS"], 1),
        mcq("p6", "A CEO email asking for a gift-card purchase this minute is often:", ["Normal finance", "Business email compromise / pretexting", "A SIEM rule", "A TLS handshake"], 1),
        mcq("p7", "Hovering a link before clicking helps you:", ["Decrypt TLS", "See the real destination host", "Reset MFA", "Open a sandbox automatically"], 1),
        mcq("p8", "A PDF that says “enable macros to view” is:", ["Always safe from Adobe", "A common malware lure", "Required for PDF", "A DKIM signature"], 1),
        mcq("p9", "Spear phishing is:", ["Random spam to millions", "Targeted mail using details about you or your job", "Only SMS", "Only QR codes"], 1),
        mcq("p10", "If you already clicked a phishing link, first:", ["Ignore it", "Disconnect, tell the desk, change passwords from a clean device", "Forward the mail to customers", "Pay if they ask"], 1),
        mcq("p11", "Display names can be forged. Trust:", ["The From name in bold", "The real address and how you got there", "Any padlock icon", "A logo in the footer"], 1),
        mcq("p12", "A text that says your package failed and needs a card is often:", ["Courier policy", "Smishing", "A VPN invite", "A certificate pin"], 1),
        mcq("p13", "Attachment double extensions like invoice.pdf.exe are:", ["A Windows joke", "A way to hide an executable", "Required by Outlook", "Proof of signing"], 1),
        mcq("p14", "Vishing is:", ["Virus hashing", "Voice-call social engineering", "VLAN tagging", "A SIEM parser"], 1),
        mcq("p15", "A shared “password spreadsheet” in a phishing kit is there to:", ["Help you remember", "Steal many accounts at once", "Meet ISO", "Train MFA"], 1),
        mcq("p16", "Urgency and fear in a message are used to:", ["Slow you down", "Stop you from checking with a second channel", "Improve spelling", "Prove DKIM"], 1),
        mcq("p17", "Reporting phishing to the desk is useful because:", ["It wastes time", "Others can be blocked from the same lure", "It deletes backups", "It turns off MFA"], 1),
        fill("p18", "Phishing that uses SMS is often called ______.", ["smishing"]),
        fill("p19", "Phishing that uses a phone call is often called ______.", ["vishing"]),
        fill("p20", "BEC stands for business email ______.", ["compromise"]),
        fill("p21", "Do not share your one-time ______ with anyone who calls you.", ["password", "code", "otp", "token"]),
        match("p22", "Match the lure.", [("Urgent wire", "BEC / fake executive"), ("Enable macros", "Malware document"), ("Reset now or lock", "Credential harvest")]),
        match("p23", "Match the check.", [("Hover the link", "See the real host"), ("Call the known number", "Verify out of band"), ("Official app", "Avoid the emailed URL")]),
        match("p24", "Match the channel.", [("Email", "Classic phishing"), ("SMS", "Smishing"), ("Voice", "Vishing")]),
        mcq("p25", "A padlock in the browser means:", ["The site is honest", "The connection is encrypted — not that the site is the real bank", "The CEO wrote the page", "Macros are off"], 1),
        mcq("p26", "Typosquatting registers:", ["Your real domain", "A lookalike name people mistype", "Only government zones", "Air-gapped hosts"], 1),
        mcq("p27", "A helpdesk ticket that was never opened, asking you to “confirm the password”, is:", ["Normal IT", "A pretext you should verify on a known channel", "MFA enrollment", "A firewall rule"], 1),
        mcq("p28", "Homograph attacks use:", ["Similar-looking characters in a domain", "Only IPv6", "Only UDP 53", "Only QR paper"], 0),
        mcq("p29", "If a coworker’s mail asks for a password reset “from airport Wi-Fi”, you should:", ["Send the password", "Use a second known channel before you act", "CC the whole company", "Disable their MFA"], 1),
    ],
    "network": [
        mcq("n1", "A switch forwarding Ethernet frames by MAC is mainly at OSI:", ["Layer 1", "Layer 2", "Layer 3", "Layer 7"], 1),
        mcq("n2", "Which protocol maps IP to MAC on a local Ethernet segment?", ["DNS", "ARP", "SMTP", "TLS"], 1),
        mcq("n3", "DNS mainly translates:", ["MAC to serial", "Names to IP addresses", "Passwords to hashes", "VLANs to racks"], 1),
        mcq("n4", "TCP handshake is:", ["SYN, SYN-ACK, ACK", "FIN, RST, PSH", "GET, POST, HEAD", "ARP, RARP, DHCP"], 0),
        mcq("n5", "A default-deny firewall means:", ["All ports open unless listed", "Traffic is blocked unless a rule allows it", "ICMP is always allowed", "Only IPv6 is filtered"], 1),
        mcq("n6", "Port 443 is commonly:", ["SMTP", "HTTPS", "SSH", "RDP"], 1),
        mcq("n7", "SSH usually uses port:", ["22", "25", "80", "3389"], 0),
        mcq("n8", "A VLAN is used to:", ["Encrypt disks", "Segment broadcast domains", "Replace DNS", "Sign email"], 1),
        mcq("n9", "NAT typically:", ["Hashes passwords", "Translates private addresses to a public one", "Stops all malware", "Replaces TLS"], 1),
        mcq("n10", "A packet capture (pcap) is useful to:", ["See what really went on the wire", "Patch Windows", "Issue certificates", "Reset MFA"], 0),
        mcq("n11", "ICMP is commonly used by:", ["ping and some diagnostics", "HTTPS forms", "Kerberos tickets", "SQL queries"], 0),
        mcq("n12", "A rogue DHCP server can:", ["Only print banners", "Hand out a bad gateway and intercept traffic", "Patch switches", "Disable ARP forever"], 1),
        mcq("n13", "TLS protects data:", ["At rest on every disk automatically", "In transit between client and server", "Inside every database row", "On paper backups"], 1),
        mcq("n14", "Port scanning is:", ["Always illegal everywhere", "A way to learn which services answer", "A hash function", "A phishing kit"], 1),
        mcq("n15", "A DMZ is typically:", ["The CEO laptop", "A network zone for services that face untrusted networks", "An air gap", "A Wi-Fi password"], 1),
        mcq("n16", "UDP is different from TCP because it:", ["Always handshakes three times", "Does not guarantee delivery or order", "Cannot carry DNS", "Is only for email"], 1),
        mcq("n17", "An IDS mainly:", ["Blocks every packet", "Detects suspicious traffic and alerts", "Issues passports", "Replaces backups"], 1),
        mcq("n18", "An IPS sits where it can:", ["Only read logs tomorrow", "Actively block or drop bad traffic", "Print tickets", "Hash disks"], 1),
        fill("n19", "ARP maps an IP address to a ______ address.", ["mac", "hardware", "ethernet"]),
        fill("n20", "HTTPS commonly uses TCP port ______.", ["443"]),
        fill("n21", "The protocol that resolves names to IPs is ______.", ["dns"]),
        fill("n22", "SSH commonly uses TCP port ______.", ["22"]),
        match("n23", "Match the port.", [("22", "SSH"), ("53", "DNS"), ("443", "HTTPS")]),
        match("n24", "Match the layer (simple).", [("IP routing", "Network / Layer 3"), ("Ethernet MAC", "Data link / Layer 2"), ("HTTP", "Application / Layer 7")]),
        match("n25", "Match the tool idea.", [("Firewall", "Allow or deny by policy"), ("IDS", "Alert on patterns"), ("Packet capture", "Record the bytes")]),
        mcq("n26", "MAC flooding targets:", ["The switch CAM table so frames flood", "Only DNSSEC", "Only TLS 1.0", "Paper shredders"], 0),
        mcq("n27", "A site-to-site VPN is mainly for:", ["Two networks talking privately over the internet", "Phishing kits", "Guest printers", "Screen sharing only"], 0),
        mcq("n28", "DHCP provides:", ["TLS certificates", "Address and network config to hosts", "MFA tokens", "SQL schemas"], 1),
        mcq("n29", "East-west traffic is:", ["Internet to DMZ only", "Traffic between internal systems", "Only satellite links", "Only print jobs"], 1),
    ],
    "soc": [
        mcq("s1", "The first job with a SIEM alert is usually to:", ["Wipe the laptop", "Triage: true, false, or needs more data", "Post the payload publicly", "Ignore it until Friday"], 1),
        mcq("s2", "A false positive is:", ["A real breach", "An alert that fired but was not the bad thing you feared", "A missing log", "A ransomware note"], 1),
        mcq("s3", "A playbook is:", ["A movie script", "A repeatable set of steps for a class of alerts", "A firewall brand", "A phishing domain"], 1),
        mcq("s4", "SOAR is mainly about:", ["Playing music", "Automating response steps around tickets and tools", "Replacing all analysts", "Deleting SIEM"], 1),
        mcq("s5", "If an endpoint EDR says “beaconing to a rare host”, you should:", ["Unplug every building", "Investigate process, user, and destination before you destroy evidence", "Tweet IOCs immediately", "Format from BIOS first"], 1),
        mcq("s6", "Mean time to detect (MTTD) measures:", ["How fast you buy tools", "How long the bad activity sat before you saw it", "Password length", "Patch Tuesday"], 1),
        mcq("s7", "A use case in a SIEM is:", ["A furniture layout", "A detection idea mapped to data and an alert", "A coffee rota", "A VLAN number"], 1),
        mcq("s8", "You enrich an alert when you:", ["Delete it", "Add context: asset owner, geo, threat intel, history", "Change the wallpaper", "Disable MFA"], 1),
        mcq("s9", "A ticket should capture:", ["Only the meme", "What you saw, what you did, and what is still open", "The CEO salary", "Wi-Fi PSK"], 1),
        mcq("s10", "Log sources that never arrive are a problem because:", ["Disks stay empty", "You are blind in that corner", "Alerts get prettier", "MFA is stronger"], 1),
        mcq("s11", "Tuning a noisy rule means:", ["Turning all detections off", "Reducing junk without blinding the real cases", "Buying a louder siren", "Blocking DNS"], 1),
        mcq("s12", "An IOC is:", ["A coffee order", "A clue like a hash, IP, or domain tied to activity", "A VLAN", "A backup tape"], 1),
        mcq("s13", "Shift handoff should include:", ["Nothing, start fresh", "Open incidents, weak detections, and what to watch", "Personal passwords", "The alarm code only"], 1),
        mcq("s14", "A true positive that is allowed (policy) is often called:", ["A worm", "Benign / expected activity — document it", "Ransomware", "A zero-day always"], 1),
        mcq("s15", "When you isolate a host you mainly:", ["Throw it in a river", "Cut its network so it cannot talk while you investigate", "Publish its disk online", "Reset the building"], 1),
        mcq("s16", "A runbook for phishing often includes:", ["Paying the sender", "Pulling headers, URLs, and who clicked", "Disabling all mail forever", "Ignoring VIP inboxes"], 1),
        mcq("s17", "UEBA tries to:", ["Paint the SOC", "Spot users or hosts acting unlike their baseline", "Replace firewalls", "Issue passports"], 1),
        fill("s18", "SIEM stands for security information and ______ management.", ["event"]),
        fill("s19", "EDR stands for endpoint detection and ______.", ["response"]),
        fill("s20", "An ______ is a hash, IP, or domain used as a clue.", ["ioc", "indicator of compromise"]),
        fill("s21", "The first pass on an alert is called ______.", ["triage"]),
        match("s22", "Match the SOC idea.", [("SIEM", "Collect and alert on logs"), ("EDR", "Watch the host"), ("Playbook", "Repeatable steps")]),
        match("s23", "Match the outcome.", [("True positive", "The bad thing is real"), ("False positive", "The alert was wrong"), ("False negative", "You missed it")]),
        match("s24", "Match the action.", [("Isolate", "Cut the host off the net"), ("Enrich", "Add context"), ("Escalate", "Hand to IR / senior")]),
        mcq("s25", "A spike of failed logons then a success from a new country may mean:", ["A printer jam", "Credential stuffing or account takeover — investigate", "A healthy backup", "Only DST"], 1),
        mcq("s26", "You should not wipe a machine first when:", ["You need memory, disk, and logs for the case", "The CEO is bored", "The SIEM is green", "Coffee is cold"], 0),
        mcq("s27", "A detection that never fires in a year might be:", ["Perfect", "Broken, blind, or unused — test it", "Illegal", "A VLAN"], 1),
        mcq("s28", "Chain of custody in the SOC matters when:", ["You might go to legal or HR with the evidence", "You change a wallpaper", "You ping 8.8.8.8", "You rotate a chair"], 0),
        mcq("s29", "A good alert title is:", ["“Something”", "Specific: host, user, action, why it fired", "All caps only", "A password"], 1),
    ],
    "identity": [
        mcq("i1", "Password spraying is:", ["A buffer overflow", "Few common passwords tried across many accounts", "ARP spoofing", "SQL injection"], 1),
        mcq("i2", "A service account should usually:", ["Have an interactive daily login", "Be unique, least privilege, and monitored", "Share the helpdesk password", "Skip MFA because it is a robot"], 1),
        mcq("i3", "OAuth access tokens should be treated as:", ["Public banners", "Secrets — they act as the user to APIs", "MAC addresses", "VLAN tags"], 1),
        mcq("i4", "When someone leaves, their access should be:", ["Kept “just in case”", "Revoked the same day, including tokens and keys", "Emailed to the team", "Written on a whiteboard"], 1),
        mcq("i5", "Role-based access control (RBAC) assigns rights by:", ["Favorite color", "Job role, not one-off chaos", "IP only", "Desk number only"], 1),
        mcq("i6", "A shared admin password is bad because:", ["It is easy to type", "You cannot tell who did what", "It is too long", "Kerberos forbids it always"], 1),
        mcq("i7", "Just-in-time admin means:", ["Admin all day", "Elevate only when needed, then drop", "No logs", "One password forever"], 1),
        mcq("i8", "Kerberos is mainly:", ["A web cookie brand", "A ticket-based network authentication protocol", "A firewall", "A SIEM"], 1),
        mcq("i9", "A pass-the-hash attack reuses:", ["Printed badges", "Stolen password hashes / material to impersonate", "Only QR codes", "Only SMS"], 1),
        mcq("i10", "IdP means:", ["Intranet dump protocol", "Identity provider — the service that authenticates you", "A VLAN", "A pcap"], 1),
        mcq("i11", "SSO is useful because:", ["One login to many apps — still needs strong proof and offboarding", "Passwords can be the same as the username", "MFA is banned", "Logs go away"], 0),
        mcq("i12", "A session cookie without Secure/HttpOnly is:", ["Always fine", "Easier to steal with XSS or cleartext", "A Kerberos ticket", "An MFA device"], 1),
        mcq("i13", "Privileged access workstations exist to:", ["Play games", "Keep admin work off the everyday phishing laptop", "Share USB sticks", "Disable logging"], 1),
        mcq("i14", "Directory sync of disabled users that still have SaaS tokens means:", ["You are done", "Cloud sessions may still be alive — revoke them", "MFA is optional", "DNS is down"], 1),
        mcq("i15", "Biometrics are:", ["Unstealable forever", "Another factor — still need fallback and privacy care", "A replacement for all logs", "A VLAN"], 1),
        mcq("i16", "A break-glass account is:", ["Used daily for email", "An emergency admin path that is monitored and rare", "A phishing kit", "Guest Wi-Fi"], 1),
        mcq("i17", "SAML is commonly used to:", ["Capture packets", "Federate login between an IdP and an app", "Hash disks", "Scan ports"], 1),
        fill("i18", "RBAC stands for ______-based access control.", ["role"]),
        fill("i19", "SSO stands for single ______-on.", ["sign", "single sign"]),
        fill("i20", "Never reuse a ______ across work and personal sites.", ["password"]),
        fill("i21", "MFA should be required for ______ accounts especially.", ["admin", "privileged", "administrator"]),
        match("i22", "Match the identity idea.", [("Least privilege", "Only the rights for the job"), ("MFA", "More than a password"), ("Offboarding", "Cut access when people leave")]),
        match("i23", "Match the attack.", [("Spraying", "Few passwords, many accounts"), ("Stuffing", "Leaked pairs tried on other sites"), ("Phishing", "Trick the person out of the secret")]),
        match("i24", "Match the object.", [("Access token", "Lets an API act as you"), ("Refresh token", "Gets new access tokens"), ("Password hash", "Stored proof of the password")]),
        mcq("i25", "Conditional access can require:", ["No logs", "MFA or a healthy device before a sensitive app", "Shared passwords", "Guest admin"], 1),
        mcq("i26", "A local admin on every laptop is risky because:", ["Updates are faster", "One foothold becomes many", "Kerberos needs it", "DNS requires it"], 1),
        mcq("i27", "API keys in a public Git repo should be:", ["Ignored", "Rotated and treated as compromised", "Printed", "Used as the office Wi-Fi"], 1),
        mcq("i28", " PAM (privileged access management) is about:", ["Painting rooms", "Controlling and recording powerful logins", "Only printers", "Only IPv6"], 1),
        mcq("i29", "A user with two jobs should get:", ["Both full admin sets forever", "Access reviewed so extra roles do not pile up", "The CEO mailbox", "No MFA"], 1),
    ],
    "web": [
        mcq("w1", "SQL injection happens when:", ["The OS is unpatched only", "Untrusted input is mixed into a query as code", "TLS is 1.3", "Cookies are HttpOnly"], 1),
        mcq("w2", "Stored XSS is dangerous because:", ["It only hits the attacker", "A script saved in the app runs in other users’ browsers", "It patches SQL", "It disables CSRF"], 1),
        mcq("w3", "CSRF tricks a logged-in browser into:", ["Clearing DNS", "Sending a request the user did not mean", "Hashing passwords", "Opening Wireshark"], 1),
        mcq("w4", "Prepared statements help against:", ["DDoS only", "SQL injection", "Physical theft", "ARP spoof"], 1),
        mcq("w5", "A missing Content-Security-Policy makes ______ easier:", ["VLAN hopping", "XSS impact", "BGP hijack", "Disk encryption"], 1),
        mcq("w6", "Directory traversal tries to:", ["Read files outside the web root with ../", "Renew certificates", "Tune SIEM", "Set VLANs"], 0),
        mcq("w7", "An IDOR bug is when:", ["You can see or change another user’s object by guessing an ID", "TLS fails", "DNSSEC is on", "The WAF is loud"], 0),
        mcq("w8", "Output encoding is mainly for:", ["SQL backups", "Stopping XSS when you print untrusted text", "IP routing", "MFA"], 1),
        mcq("w9", "SameSite=Lax/Strict on cookies helps against:", ["Ransomware encryption", "Some CSRF", "Broken disks", "ARP cache"], 1),
        mcq("w10", "A WAF sits in front of apps to:", ["Replace secure code completely", "Filter some common web attacks", "Issue passports", "Hash BIOS"], 1),
        mcq("w11", "Command injection is when:", ["JSON is pretty", "OS commands are built from user input", "TLS stapling works", "CSS loads"], 1),
        mcq("w12", "Open redirect is used to:", ["Patch nginx", "Send victims through your trusted domain to a bad site", "Rotate logs", "Set MTU"], 1),
        mcq("w13", "Rate limiting login helps against:", ["Only XSS", "Password stuffing and spraying", "Only CSRF", "Only IDOR"], 1),
        mcq("w14", "Security headers like HSTS tell the browser to:", ["Disable JS forever", "Prefer HTTPS and remember it", "Allow mixed HTTP images always", "Skip cookies"], 1),
        mcq("w15", "A JWT in localStorage is riskier than an HttpOnly cookie because:", ["It is shorter", "XSS can steal it with script", "It cannot expire", "Browsers ignore it"], 1),
        mcq("w16", "File upload bugs often lead to:", ["Pretty thumbnails only", "Webshells if the file is executed", "Faster CSS", "Better MFA"], 1),
        mcq("w17", "CORS misconfiguration can:", ["Speed TCP", "Let a hostile site read your API from a victim browser", "Patch SQL", "Disable XSS"], 1),
        fill("w18", "XSS stands for cross-site ______.", ["scripting"]),
        fill("w19", "CSRF stands for cross-site ______ forgery.", ["request"]),
        fill("w20", "Use ______ statements instead of string-built SQL.", ["prepared", "parameterized", "parameterised"]),
        fill("w21", "IDOR stands for insecure direct object ______.", ["reference"]),
        match("w22", "Match the web bug.", [("SQLi", "Query built from input"), ("XSS", "Script in the page"), ("CSRF", "Unwanted request as the user")]),
        match("w23", "Match the fix.", [("Prepared statement", "SQLi"), ("Output encoding", "XSS"), ("Anti-CSRF token", "CSRF")]),
        match("w24", "Match the header idea.", [("CSP", "Limit script sources"), ("HSTS", "Force HTTPS"), ("X-Frame-Options", "Reduce clickjacking")]),
        mcq("w25", "Clickjacking uses:", ["A hidden iframe over a real button", "Only SMTP", "Only ARP", "Only bcrypt"], 0),
        mcq("w26", "Mass assignment is when:", ["The API binds extra fields the client should not set", "You scan all ports", "You rotate logs", "You pin TLS"], 0),
        mcq("w27", "A health endpoint that dumps env secrets is:", ["Fine in production", "An information leak — lock it down", "Required by HTTP/2", "A CSRF token"], 1),
        mcq("w28", "Server-side request forgery (SSRF) makes your server:", ["Faster", "Fetch URLs the attacker chooses, often inside the cloud", "Hash passwords twice", "Skip DNS"], 1),
        mcq("w29", "Parameterized queries still fail if you:", ["Use them everywhere", "Concatenate input into the query anyway", "Use TLS", "Log access"], 1),
    ],
    "cloud": [
        mcq("c1", "Shared responsibility means:", ["The cloud vendor does all security", "Vendor secures the cloud; you secure what you put in it", "No one patches", "Only physical locks matter"], 1),
        mcq("c2", "A public S3 / blob bucket with customer files is usually:", ["Required for HTTPS", "A data leak waiting to happen", "A SIEM", "A VLAN"], 1),
        mcq("c3", "Long-lived access keys in a repo should be:", ["Ignored", "Revoked and replaced with roles or short credentials", "Printed on badges", "Used as SSH"], 1),
        mcq("c4", "IMDSv2 on AWS is meant to make ______ harder:", ["DNSSEC", "SSRF stealing instance credentials", "TLS 1.3", "VLANs"], 1),
        mcq("c5", "A security group is closest to:", ["A physical cage", "A cloud firewall for an instance or NIC", "A SIEM parser", "A phishing kit"], 1),
        mcq("c6", "Root / owner account should be:", ["Used daily for email", "Locked down, MFA, almost never used", "Shared in Slack", "The CI password"], 1),
        mcq("c7", "Encryption at rest without key control still fails if:", ["Disks are cheap", "Anyone with the app role can read the data anyway", "TLS is on", "Logs exist"], 1),
        mcq("c8", "CloudTrail / activity logs matter because:", ["They replace IAM", "You need a record of who changed what", "They speed VMs", "They disable SSH"], 1),
        mcq("c9", "A serverless function with * on all resources is:", ["Least privilege", "Over-permissioned — shrink the role", "Required by HTTP", "A WAF"], 1),
        mcq("c10", "Exposing Redis or Mongo to 0.0.0.0 is:", ["Best practice", "A common cloud breach pattern", "Needed for TLS", "A backup strategy"], 1),
        mcq("c11", "Infrastructure as code helps security when you:", ["Click only in the console forever", "Review templates the same way you review code", "Disable logging", "Share root"], 1),
        mcq("c12", "A shadow account or forgotten subscription is risky because:", ["It is cheaper", "Nobody patches or watches it", "It cannot hold data", "MFA is automatic"], 1),
        mcq("c13", "Customer-managed keys are useful when:", ["You want no encryption", "You need to control rotation and who can decrypt", "You hate IAM", "You disable CloudTrail"], 1),
        mcq("c14", "Metadata IP 169.254.169.254 is:", ["A public website", "The instance metadata service many clouds use", "A DNS root", "An NTP pool"], 1),
        mcq("c15", "Network peering without inspection can:", ["Only speed backups", "Let a compromise walk into another VPC / VNet", "Replace MFA", "Hash disks"], 1),
        mcq("c16", "Object versioning + MFA delete helps against:", ["Only XSS", "Ransomware wiping buckets", "Only BGP", "Only CSRF"], 1),
        mcq("c17", "A CI/CD role that can deploy prod should:", ["Be the intern laptops", "Be tightly scoped and produce an audit trail", "Skip OIDC", "Use the root key"], 1),
        fill("c18", "IAM stands for identity and ______ management.", ["access"]),
        fill("c19", "A publicly listable object store is often called an open ______.", ["bucket"]),
        fill("c20", "Prefer short-lived ______ over long access keys.", ["roles", "tokens", "credentials"]),
        fill("c21", "The cloud vendor patches the ______; you patch the guest OS and apps (IaaS).", ["hypervisor", "hardware", "cloud infrastructure"]),
        match("c22", "Match the cloud idea.", [("Security group", "Allow/deny to an instance"), ("IAM role", "Who the workload is"), ("Bucket policy", "Who can read objects")]),
        match("c23", "Match the mistake.", [("0.0.0.0/0 on SSH", "World can try your admin port"), ("Public bucket", "World can read files"), ("Keys in Git", "World can act as you")]),
        match("c24", "Match the model (IaaS).", [("Vendor", "Hardware, hypervisor, regions"), ("You", "OS, apps, identities, data"), ("Shared", "Split by the service model")]),
        mcq("c25", "Multi-account / subscription isolation is for:", ["Pretty bills only", "Blast radius — prod is not the sandbox", "Disabling MFA", "Skipping logs"], 1),
        mcq("c26", "A public snapshot of a disk may contain:", ["Only empty sectors", "Secrets and customer data", "Only BIOS", "Only ARP"], 1),
        mcq("c27", "WAF + CDN help at the edge but do not replace:", ["Secure app code and IAM", "Electricity", "Racks", "Cables"], 0),
        mcq("c28", "Disable unused regions/services to:", ["Break DNS", "Shrink the attack surface you forget to watch", "Stop TLS", "Ban MFA"], 1),
        mcq("c29", "Assume-role instead of static keys is better because:", ["Roles never expire", "Credentials are short and tied to a workload", "Git needs them", "Buckets require them"], 1),
    ],
    "incident": [
        mcq("r1", "The first IR priority after safety is often:", ["Blame", "Contain spread, then preserve evidence", "Reimage every laptop in the country", "Tweet IOCs"], 1),
        mcq("r2", "You image a disk before wiping because:", ["It is slower", "You may need evidence and a clean recovery path", "Insurance forbids images", "SIEM forbids it"], 1),
        mcq("r3", "A ransomware note is:", ["Proof you should pay immediately", "An incident — isolate, notify, restore from clean backups", "A patch", "A VLAN"], 1),
        mcq("r4", "Chain of custody records:", ["Coffee orders", "Who had the evidence and when", "Wi-Fi PSK", "Favorite ports"], 1),
        mcq("r5", "Lessons learned meetings exist to:", ["Shame people", "Fix detections and process so the next one is smaller", "Delete logs", "Disable MFA"], 1),
        mcq("r6", "Legal hold means:", ["Throw the laptop", "Do not destroy potentially relevant data", "Pay ransom", "Reset all passwords twice only"], 1),
        mcq("r7", "A tabletop exercise is:", ["Moving desks", "A practiced walkthrough of an incident without the live fire", "A packet flood", "A phishing kit"], 1),
        mcq("r8", "When malware is still talking out, isolating the host:", ["Always destroys RAM", "Stops command-and-control if you do it with a plan", "Is illegal", "Replaces backups"], 1),
        mcq("r9", "Notification clocks (like breach laws) start from:", ["When marketing is ready", "When you reasonably know personal data may be at risk — know your law", "Patch Tuesday", "The next AGM"], 1),
        mcq("r10", "A dirty backup restored to prod can:", ["Heal everything", "Bring the attacker back", "Rotate keys automatically", "Disable phishing"], 1),
        mcq("r11", "Memory capture is useful because:", ["Disks never matter", "Some malware and keys live mainly in RAM", "It replaces logs", "It is prettier"], 1),
        mcq("r12", "Comms during an incident should be:", ["On the possibly compromised chat only", "On a known-good channel with a single story", "On public social first", "Silent forever"], 1),
        mcq("r13", "IOC sharing with peers is useful after:", ["You posted passwords", "You have a handle on accuracy and legal", "You wiped evidence", "You paid in bitcoin"], 1),
        mcq("r14", "Eradication is:", ["The press release", "Removing the attacker’s footholds, not just the first file", "Buying a new logo", "Closing the SIEM"], 1),
        mcq("r15", "Recovery includes:", ["Only hope", "Restore, watch for return, and prove clean", "Deleting CloudTrail", "Sharing root"], 1),
        mcq("r16", "A war room is:", ["A physical fight", "A dedicated space (or call) to coordinate the incident", "A VLAN", "A backup tape"], 1),
        mcq("r17", "If logs may be tampered, you should:", ["Trust them blindly", "Pull copies from other sources and note the gap", "Delete SIEM", "Reboot twice"], 1),
        fill("r18", "IR stands for incident ______.", ["response"]),
        fill("r19", "The NIST IR phases include preparation, detection, containment, eradication, and ______.", ["recovery"]),
        fill("r20", "Do not ______ a machine before you capture what you need.", ["wipe", "reimage", "format"]),
        fill("r21", "A ______ backup is one you have restored in a test.", ["tested", "verified", "known-good", "clean"]),
        match("r22", "Match the IR phase.", [("Contain", "Stop the spread"), ("Eradicate", "Remove the foothold"), ("Recover", "Bring services back clean")]),
        match("r23", "Match the artifact.", [("Disk image", "Preserve the drive"), ("Memory dump", "Preserve RAM"), ("Packet capture", "Preserve the wire")]),
        match("r24", "Match the mistake.", [("Wipe first", "Lose evidence"), ("Restore dirty backup", "Bring them back"), ("No comms plan", "Rumors fill the gap")]),
        mcq("r25", "Preparation includes:", ["Waiting for fire", "Contacts, logging, backups, and practiced roles", "Only a siren", "Disabling EDR"], 1),
        mcq("r26", "Paying ransom:", ["Guarantees files and silence", "Is a business/legal call — it does not replace IR", "Patches the hole", "Is required by TLS"], 1),
        mcq("r27", "A timeline in the report should be:", ["Guessed", "Built from logs and notes with timestamps", "Only screenshots of Slack", "The CEO bio"], 1),
        mcq("r28", "Aftercare watching (hunt) is for:", ["Decor", "Making sure the actor did not leave a second door", "Faster Wi-Fi", "Shorter passwords"], 1),
        mcq("r29", "Who can declare a major incident should be:", ["Anyone in Slack jokes", "Clear in the plan so you do not freeze", "Only the intern", "The vendor chatbot"], 1),
    ],
}


def category_by_slug(slug):
    for c in CATEGORIES:
        if c["slug"] == slug:
            return c
    return None


def pool_for(slug):
    return list(BANK.get(slug) or [])


NEED = 20
CHANGE_RATIO = 0.3


def pick_attempt_questions(slug, previous_ids):
    pool = pool_for(slug)
    if len(pool) < NEED:
        raise ValueError("Not enough questions in this category.")
    by_id = {q["id"]: q for q in pool}
    prev = [i for i in previous_ids if i in by_id]
    change = max(1, int(round(NEED * CHANGE_RATIO)))
    keep_n = NEED - change
    unused_ids = [q["id"] for q in pool if q["id"] not in prev]
    if not prev:
        picked_ids = [q["id"] for q in random.sample(pool, NEED)]
    else:
        keep = random.sample(prev, min(keep_n, len(prev)))
        need_new = NEED - len(keep)
        new_pool = unused_ids[:]
        if len(new_pool) < need_new:
            new_pool.extend([i for i in prev if i not in keep])
        new_ids = random.sample(new_pool, min(need_new, len(new_pool)))
        picked_ids = keep + new_ids
        if len(picked_ids) < NEED:
            rest = [q["id"] for q in pool if q["id"] not in picked_ids]
            picked_ids.extend(random.sample(rest, min(NEED - len(picked_ids), len(rest))))
    random.shuffle(picked_ids)
    return [by_id[i] for i in picked_ids[:NEED]]


def shuffle_mcq(item):
    order = list(range(len(item["choices"])))
    random.shuffle(order)
    choices = [item["choices"][i] for i in order]
    answer = order.index(item["answer"])
    return choices, answer


def present_question(item):
    if item["type"] == "mcq":
        choices, answer = shuffle_mcq(item)
        public = {"id": item["id"], "type": "mcq", "q": item["q"], "choices": choices}
        secret = {"id": item["id"], "type": "mcq", "answer": answer}
        return public, secret
    if item["type"] == "fill":
        public = {"id": item["id"], "type": "fill", "q": item["q"]}
        secret = {"id": item["id"], "type": "fill", "answers": item["answers"]}
        return public, secret
    left = [{"id": p["id"], "text": p["left"]} for p in item["pairs"]]
    right = [{"id": p["id"], "text": p["right"]} for p in item["pairs"]]
    random.shuffle(right)
    public = {"id": item["id"], "type": "match", "q": item["q"], "left": left, "right": right}
    secret = {"id": item["id"], "type": "match", "ok": {p["id"]: p["id"] for p in item["pairs"]}}
    return public, secret


def present_set(items):
    public = []
    secret = []
    for item in items:
        p, s = present_question(item)
        public.append(p)
        secret.append(s)
    return public, secret


def _norm(text):
    return " ".join(str(text or "").strip().lower().split())


def score_answers(secret, answers):
    answers = answers if isinstance(answers, dict) else {}
    right = 0
    detail = []
    for item in secret:
        qid = item["id"]
        given = answers.get(qid)
        if given is None and str(qid) in answers:
            given = answers[str(qid)]
        ok = False
        if item["type"] == "mcq":
            try:
                ok = int(given) == int(item["answer"])
            except (TypeError, ValueError):
                ok = False
        elif item["type"] == "fill":
            got = _norm(given)
            ok = any(_norm(a) == got or _norm(a) in got or got in _norm(a) for a in item["answers"]) if got else False
        elif item["type"] == "match":
            mapping = given if isinstance(given, dict) else {}
            ok = bool(item["ok"]) and all(
                str(mapping.get(k) or mapping.get(str(k)) or "") == str(v) for k, v in item["ok"].items()
            )
        if ok:
            right += 1
        detail.append({"id": qid, "ok": ok})
    return right, detail
