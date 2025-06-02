<h1 align="center">🔍 Domain-Digger — Subdomain Enumeration Tool</h1>
<p align="center">
  <em>Discover subdomains fast with Certificate Transparency logs and resolve them like a pro.</em>
</p>

---

## ✨ Features

- 🔎 **Fetch subdomains** from [crt.sh]
- 🌐 **Resolve domains** to IP addresses using `gevent`
- 📤 **Flexible Output Options**:
  - ✅ Resolved IPs (for tools like Masscan)
  - 🌍 HTTPS URLs (for quick recon)
  - 🧾 Full domain + IP list
- 🚀 **High performance** via gevent greenlets

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/yashisingh26/Domain-Digger.git
cd Domain-Digger

# Create a virtual environment
python3 -m venv venv

# Activate the environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

🛠️ Usage
python3 Domain-Digger.py -d example.com [options]

Required:
-d, --domain : 🌐 Target domain name (e.g., example.com)

Optional:
-u, --urls : 📄 Output as https://sub.domain.com

-m, --masscan: 🧱 Output resolved IPs only (Masscan-compatible)

⚠️ Notes
❌ Subdomains without valid DNS records will be marked as unresolved

🔓 This tool uses public CT data — no brute-forcing involved


👨‍💻 Author
Yashi Singh
💬 Contributions, issues, and PRs are welcome!

