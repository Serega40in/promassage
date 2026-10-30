import json
import re
import sys
from pathlib import Path

path = Path("content.json")
data = json.loads(path.read_text(encoding="utf-8"))
allowed = {
    "brand", "tagline", "eyebrow", "heroTitle", "heroScript", "heroDescription",
    "heroArtLabel", "servicesEyebrow", "servicesTitle", "servicesIntro", "services",
    "bookingTitle", "bookingDescription", "telegram", "phoneDisplay", "phoneTel",
    "aboutTitle", "aboutDescription", "aboutQuote", "contactTitle", "contactDescription"
}
unknown = set(data) - allowed
missing = allowed - set(data)
if unknown or missing:
    raise SystemExit(f"Invalid content keys. Unknown={sorted(unknown)}, missing={sorted(missing)}")

for key in allowed - {"services"}:
    value = data[key]
    if not isinstance(value, str) or not value.strip() or len(value) > 700:
        raise SystemExit(f"{key}: expected non-empty text up to 700 characters")
    if re.search(r"<\s*/?\s*[a-zA-Z!]", value):
        raise SystemExit(f"{key}: HTML markup is not allowed")

if not data["telegram"].startswith("https://t.me/") or len(data["telegram"]) > 100:
    raise SystemExit("telegram must be a short https://t.me/ link")
if not re.fullmatch(r"\+?[0-9 ()-]{7,24}", data["phoneTel"]):
    raise SystemExit("phoneTel contains unsupported characters")
services = data["services"]
if not isinstance(services, list) or not 1 <= len(services) <= 8:
    raise SystemExit("services must be a list of 1 to 8 entries")
for i, service in enumerate(services):
    if not isinstance(service, dict) or set(service) != {"code", "title", "description", "note"}:
        raise SystemExit(f"services[{i}]: invalid fields")
    for key, value in service.items():
        if not isinstance(value, str) or not value.strip() or len(value) > 240:
            raise SystemExit(f"services[{i}].{key}: expected text up to 240 characters")
        if re.search(r"<\s*/?\s*[a-zA-Z!]", value):
            raise SystemExit(f"services[{i}].{key}: HTML markup is not allowed")
print("content.json validation passed")
