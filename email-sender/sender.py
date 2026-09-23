#!/usr/bin/env python3
"""
email-sender: send personalized bulk emails from a CSV contact list + template.

- contacts.csv columns: name, email (extra columns are usable as {placeholders})
- template.txt: plain-text body using {name} style placeholders
- config.json: SMTP settings + subject line (copy config.example.json to start)

Safe by default: --dry-run only prints what WOULD be sent.
Use --send to actually deliver via SMTP.

Usage:
    python sender.py --dry-run
    python sender.py --send --config config.json
"""

import argparse
import csv
import re
import smtplib
import ssl
import sys
import json
from email.message import EmailMessage
from string import Template


def render(template_str: str, contact: dict) -> str:
    """Render {name}-style placeholders from a contact dict."""
    dollarized = re.sub(r"\{(\w+)\}", r"${\1}", template_str)
    return Template(dollarized).safe_substitute(contact)


def load_contacts(path: str) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def build_message(cfg: dict, contact: dict, body_template: str) -> EmailMessage:
    subject = render(cfg["subject"], contact)
    body = render(body_template, contact)
    msg = EmailMessage()
    msg["From"] = f"{cfg.get('from_name', '')} <{cfg['username']}>"
    msg["To"] = contact["email"]
    msg["Subject"] = subject
    msg.set_content(body)
    return msg


def main() -> None:
    parser = argparse.ArgumentParser(description="Send personalized bulk emails.")
    parser.add_argument("--contacts", default="contacts.csv")
    parser.add_argument("--template", default="template.txt")
    parser.add_argument("--config", default="config.json")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--dry-run", action="store_true", default=True,
                       help="Preview emails without sending (default)")
    group.add_argument("--send", action="store_true",
                       help="Actually send the emails via SMTP")
    args = parser.parse_args()

    contacts = load_contacts(args.contacts)
    with open(args.template, encoding="utf-8") as f:
        body_template = f.read()

    if args.send:
        try:
            with open(args.config, encoding="utf-8") as f:
                cfg = json.load(f)
        except FileNotFoundError:
            sys.exit("Error: config.json not found. Copy config.example.json first.")
        context = ssl.create_default_context()
        with smtplib.SMTP(cfg["smtp_host"], cfg.get("smtp_port", 587)) as server:
            server.starttls(context=context)
            server.login(cfg["username"], cfg["password"])
            for contact in contacts:
                server.send_message(build_message(cfg, contact, body_template))
                print(f"Sent -> {contact['email']}")
        print(f"\nDone. {len(contacts)} emails sent.")
    else:
        print(f"=== DRY RUN: {len(contacts)} emails (nothing sent) ===\n")
        for contact in contacts:
            subject = render("Subject: Hello {name}, quick update for you", contact)
            body = render(body_template, contact)
            print(f"To: {contact['email']}\n{subject}\n{'-' * 40}\n{body}\n{'=' * 40}\n")


if __name__ == "__main__":
    main()
