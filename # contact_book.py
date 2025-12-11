# contact_book.py
# Contact Book (original style) - Created by: <Your Name>
# Simple CLI contact manager with JSON persistence

import json
import os
from typing import List, Dict

STORE_FILE = "my_contacts.json"


class ContactBook:
    def __init__(self, filepath: str = STORE_FILE):
        self.filepath = filepath
        self._contacts: List[Dict[str, str]] = []
        self._load()
    def _load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as fh:
                    data = json.load(fh)
                    if isinstance(data, list):
                        self._contacts = data
            except Exception:
                # If file is corrupted or unreadable, start fresh
                self._contacts = []

    def _save(self):
        with open(self.filepath, "w", encoding="utf-8") as fh:
            json.dump(self._contacts, fh, indent=2, ensure_ascii=False)

    def add_contact(self, name: str, phone: str, email: str = "", note: str = ""):
        contact = {
            "name": name.strip(),
            "phone": phone.strip(),
            "email": email.strip() or "N/A",
            "note": note.strip() or "N/A",
        }
        self._contacts.append(contact)
        self._save()

    def list_all(self) -> List[Dict[str, str]]:
        return list(self._contacts)  # shallow copy

    def search(self, query: str) -> List[Dict[str, str]]:
        q = query.lower().strip()
        return [
            c for c in self._contacts
            if q in c["name"].lower() or q in c["phone"] or (c.get("email") and q in c["email"].lower())
        ]

    def update_contact(self, index: int, **fields):
        if 0 <= index < len(self._contacts):
            for k, v in fields.items():
                if k in self._contacts[index] and v is not None:
                    self._contacts[index][k] = v.strip() or self._contacts[index][k]
            self._save()
            return True
        return False

    def delete_contact(self, index: int):
        if 0 <= index < len(self._contacts):
            removed = self._contacts.pop(index)
            self._save()
            return removed
        return None


def clear_screen():
    # Minimal cross-platform screen clear
    os.system("cls" if os.name == "nt" else "clear")


def prompt(msg: str, default: str = "") -> str:
    raw = input(f"{msg}{' ['+default+']' if default else ''}: ").strip()
    return raw if raw else default


def show_menu():
    print("\n=== CONTACT BOOK MENU ===")
    print("A - Add contact")
    print("V - View all contacts")
    print("S - Search contact")
    print("U - Update contact")
    print("D - Delete contact")
    print("E - Export contacts")
    print("Q - Quit")


def export_to_csv(contacts: List[Dict[str, str]], filename: str = "contacts_export.csv"):
    import csv
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Name", "Phone", "Email", "Note"])
        for c in contacts:
            writer.writerow([c["name"], c["phone"], c["email"], c["note"]])
    print(f"Exported {len(contacts)} contacts to {filename}")


def main():
    book = ContactBook()
    print("Welcome to your Contact Book !")

    while True:
        show_menu()
        choice = input("Choose an option: ").strip().upper()

        if choice == "A":
            name = input("Name: ").strip()
            phone = input("Phone: ").strip()
            email = input("Email (optional): ").strip()
            note = input("Note (optional): ").strip()
            if not name or not phone:
                print("Name and phone are required.")
            else:
                book.add_contact(name, phone, email, note)
                print("Contact added.")

        elif choice == "V":
            contacts = book.list_all()
            if not contacts:
                print("No contacts yet.")
            else:
                print("\nAll Contacts:")
                for i, c in enumerate(contacts, start=1):
                    print(f"{i}. {c['name']} | {c['phone']} | {c['email']} | {c['note']}")

        elif choice == "S":
            q = input("Search by name/phone/email: ").strip()
            hits = book.search(q)
            if not hits:
                print("No matches found.")
            else:
                print(f"Found {len(hits)} result(s):")
                for i, c in enumerate(hits, start=1):
                    print(f"{i}. {c['name']} | {c['phone']} | {c['email']} | {c['note']}")

        elif choice == "U":
            contacts = book.list_all()
            if not contacts:
                print("No contacts to update.")
                continue
            for i, c in enumerate(contacts, start=1):
                print(f"{i}. {c['name']} | {c['phone']}")
            try:
                idx = int(input("Enter contact number to update: ")) - 1
            except ValueError:
                print("Invalid number.")
                continue
            if not (0 <= idx < len(contacts)):
                print("Invalid index.")
                continue
            current = contacts[idx]
            print("Leave blank to keep current value.")
            new_name = prompt("New name", current["name"])
            new_phone = prompt("New phone", current["phone"])
            new_email = prompt("New email", current["email"])
            new_note = prompt("New note", current["note"])
            updated = book.update_contact(idx, name=new_name, phone=new_phone, email=new_email, note=new_note)
            print("Updated." if updated else "Update failed.")

        elif choice == "D":
            contacts = book.list_all()
            if not contacts:
                print("No contacts to delete.")
                continue
            for i, c in enumerate(contacts, start=1):
                print(f"{i}. {c['name']} | {c['phone']}")
            try:
                idx = int(input("Enter contact number to delete: ")) - 1
            except ValueError:
                print("Invalid number.")
                continue
            removed = book.delete_contact(idx)
            if removed:
                print(f"Deleted {removed['name']}.")
            else:
                print("Delete failed. Check index.")

        elif choice == "E":
            export_to_csv(book.list_all())

        elif choice == "Q":
            print("Goodbye — your contacts are saved.")
            break

        else:
            print("The option is Unknown. Please try again.")


if __name__ == "__main__":
    main()