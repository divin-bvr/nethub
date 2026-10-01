window.NETHUB_MODULES = [
  {
    slug: "linux",
    title: "Linux for cybersecurity",
    tag: "Systems",
    img: "assets/nethub/illust/track-linux-kali.jpg",
    blurb: "Shell, permissions, services, and the boxes you attack and defend.",
    body: "This module is the operating system most labs actually run. You learn a real shell, users and permissions, services that listen on a port, logs that tell you what happened, and how a box looks when it is misconfigured. We do not start from slides. You sit at a terminal, break a permission, fix it, and write what you did in plain language. The Kali-style workstation is a tool in the room, not a costume. When you finish, you can move a file, read a process list, and explain why a service should not run as root. Enrol pays for a seat. After the desk confirms payment, an admin grants this module on your account so the labs unlock."
  },
  {
    slug: "python",
    title: "Python for cybersecurity",
    tag: "Automation",
    img: "assets/nethub/illust/track-python.jpg",
    blurb: "Scripts that parse logs, talk to APIs, and automate a hunt.",
    body: "Python is how you stop doing the same click twice. This module teaches enough language to parse a log, call an API, walk a folder of PCAP summaries, and write a small tool you can run again next Sunday. We stay on defensive and lab uses: no malware droppers, no credential stuffing of other people’s accounts. You leave able to read someone else’s script, change a path, and explain what the loop is doing. That is the skill employers mean when they say “scripting for security.” Enrol is the subscription. The desk grants the module after payment so you can open the notebooks and tasks."
  },
  {
    slug: "ai",
    title: "AI for cybersecurity",
    tag: "Detection",
    img: "assets/nethub/illust/track-ai.jpg",
    blurb: "Models as tools for triage — not a slogan on a slide.",
    body: "This module treats models as tools that help and fail. You see how a detector scores an alert, where a large language model invents a CVE that does not exist, and how to keep a human in the loop. We work from logs and tickets, not from marketing decks. You will write a short prompt that summarizes an incident, then check it against the raw events so you never ship a hallucination to a manager. Enrol unlocks the labs once an admin marks your subscription paid. Until then you can read this page and sit in Sunday lab as a guest of the room, not of this module."
  },
  {
    slug: "hash",
    title: "Hash cracking",
    tag: "Offensive lab",
    img: "assets/nethub/illust/track-hash.jpg",
    blurb: "Wordlists and GPU time on hashes you are allowed to recover.",
    body: "Hash cracking in Nethub is a lab skill, not a way onto someone else’s account. You learn what a hash is, why salt matters, how wordlists and rules work, and how GPU time is budgeted. We only recover hashes from exercises the desk provides. You will explain the difference between a fast hash and a slow one, and you will write a short note that a password policy can actually use. Enrol is payment for the seat. After you pay, an admin grants this module so the wordlists and the range boxes appear on your desk."
  },
  {
    slug: "osint",
    title: "OSINT",
    tag: "Collection",
    img: "assets/nethub/illust/track-osint.jpg",
    blurb: "Public sources, maps, and profiles. Collect, verify, write it down.",
    body: "Open-source intelligence here means public pages, maps, and records you are allowed to look at. You learn to collect without logging into other people’s accounts, to verify a claim against a second source, and to write a short brief that a mentor can read. We care about method: timestamp, URL, screenshot, and the sentence that says what you still do not know. That is how OSINT stays professional. Enrol sends you to pay for a subscription. The desk grants the module when payment is confirmed so the collection exercises unlock."
  },
  {
    slug: "forensics",
    title: "Forensics",
    tag: "Investigation",
    img: "assets/nethub/illust/track-forensics.jpg",
    blurb: "Preserve evidence, reconstruct an incident, write it plainly.",
    body: "Forensics in the lab is preservation first. You learn a write-blocker mindset, a simple chain of custody, how to image a disk in the exercise, and how to write a timeline that a non-specialist can follow. Tools matter less than the order of operations: do not write to the evidence, note the hash, say what you opened. You will reconstruct a small incident from artifacts the desk plants, then brief it in one page. Enrol is the subscription. An admin grants this module after you pay so the evidence packs appear on your seat."
  },
  {
    slug: "network",
    title: "Network security",
    tag: "Infrastructure",
    img: "assets/nethub/illust/track-network.jpg",
    blurb: "Packets, segmentation, remote access, and attacker paths.",
    body: "Network security is the path a packet takes and the doors you leave open. This module covers addressing, segmentation, remote access, and the captures that show a scan versus a login. You will read a simple packet list, name a protocol, and explain why a flat network turns one laptop into a company-wide event. Labs use the same racks and virtual nets as Sunday. Enrol pays for the seat. When the desk sees payment, an admin grants the module and the range VLANs become yours to use."
  },
  {
    slug: "soc",
    title: "SOC",
    tag: "Operations",
    img: "assets/nethub/illust/track-soc.jpg",
    blurb: "Alerts, dashboards, triage, and night-watch habits.",
    body: "The SOC module is the night watch: queues, dashboards, and the habit of closing an alert with a reason. You learn triage, escalation, and how to write a ticket that the next analyst can continue. We use the same screens as the range, not a cartoon wall of world maps. You will take a noisy alert, decide true or false, and record what you checked. Enrol is subscription payment. Access to this module is granted by an admin after that payment so the queue and the playbooks unlock on your desk."
  },
  {
    slug: "cloud",
    title: "Cloud security",
    tag: "Cloud",
    img: "assets/nethub/illust/track-cloud.jpg",
    blurb: "Identity, storage, and the misconfigurations that open a tenant.",
    body: "Cloud security in Nethub is identity, storage, and the default that nobody closed. You learn to read a simple IAM idea, why a public bucket is a finding, and how a forgotten test account becomes the incident. We stay in lab tenants the desk provides. You will list three misconfigurations you would look for on day one, and you will write them so a small company can actually fix them. Enrol takes you to pay. The admin grants the module after payment so the cloud labs attach to your seat."
  },
  {
    slug: "os",
    title: "Operating systems",
    tag: "Internals",
    img: "assets/nethub/illust/track-os.jpg",
    blurb: "Windows and Linux internals enough to hunt, harden, and recover.",
    body: "Operating systems is the layer under the tools. You compare Windows and Linux enough to hunt a process, harden a service, and recover a box you can snapshot in the lab. Hypervisors, users, services, and the difference between kernel and user space are the map. You will boot two VMs, name what is listening, and shut down what should not be. Enrol is the monthly seat. After you pay, an admin grants this module and the VM templates show up on your desk."
  },
  {
    slug: "pentest",
    title: "Penetration testing",
    tag: "Offensive",
    img: "assets/nethub/illust/track-pentest.jpg",
    blurb: "Find a path, prove it, document it — training, not a client test.",
    body: "Penetration testing as a learner track is scoped offensive practice. You find a path in a lab, prove it with a screenshot or a hash, and write a finding someone can remediate. This is not a client engagement and it is not a test of a network you do not own. Rules of engagement for the range are the rules. You leave able to describe impact in one paragraph. Company pentests live on the services page and are a different product. Enrol pays for the learner seat. An admin grants this module after payment so the offensive labs unlock."
  }
];
