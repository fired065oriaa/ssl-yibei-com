from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

@dataclass
class KeywordNote:
    """Represents a single keyword note with an associated URL and remarks."""
    keyword: str
    url: str
    note: str = ""
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    def update_note(self, new_note: str) -> None:
        """Update the note content and refresh the updated_at timestamp."""
        self.note = new_note
        self.updated_at = datetime.now()

    def add_tag(self, tag: str) -> None:
        """Add a tag if not already present."""
        if tag not in self.tags:
            self.tags.append(tag)

    def is_tagged(self, tag: str) -> bool:
        """Check if a specific tag exists."""
        return tag in self.tags

    def to_dict(self) -> dict:
        """Convert the note to a dictionary for serialization."""
        return {
            "keyword": self.keyword,
            "url": self.url,
            "note": self.note,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def to_formatted_string(self) -> str:
        """Return a human-readable formatted string of the note."""
        lines = [
            f"Keyword: {self.keyword}",
            f"URL: {self.url}",
            f"Note: {self.note if self.note else '(no note)'}",
            f"Tags: {', '.join(self.tags) if self.tags else '(none)'}",
            f"Created: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}",
        ]
        if self.updated_at:
            lines.append(f"Updated: {self.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
        return "\n".join(lines)


@dataclass
class KeywordNoteCollection:
    """Manages a collection of KeywordNote objects."""
    notes: List[KeywordNote] = field(default_factory=list)

    def add_note(self, note: KeywordNote) -> None:
        """Add a note to the collection."""
        self.notes.append(note)

    def remove_note(self, keyword: str) -> bool:
        """Remove a note by keyword (first match). Return True if found."""
        for note in self.notes:
            if note.keyword == keyword:
                self.notes.remove(note)
                return True
        return False

    def find_by_keyword(self, keyword: str) -> Optional[KeywordNote]:
        """Find a note by exact keyword match."""
        for note in self.notes:
            if note.keyword == keyword:
                return note
        return None

    def find_by_tag(self, tag: str) -> List[KeywordNote]:
        """Return all notes that contain the specified tag."""
        return [note for note in self.notes if note.is_tagged(tag)]

    def list_all(self) -> List[KeywordNote]:
        """Return a copy of all notes."""
        return self.notes.copy()

    def format_all(self) -> str:
        """Return a formatted block for all notes in the collection."""
        blocks = []
        for i, note in enumerate(self.notes, 1):
            header = f"--- Note #{i} ---"
            blocks.append(f"{header}\n{note.to_formatted_string()}")
        return "\n\n".join(blocks) if blocks else "No notes in collection."


def demo_usage() -> None:
    """Demonstrate typical usage of KeywordNote and KeywordNoteCollection."""
    collection = KeywordNoteCollection()

    note1 = KeywordNote(
        keyword="易倍体育",
        url="https://ssl-yibei.com",
        note="Official sports and gaming platform.",
        tags=["sports", "gaming"],
    )
    note2 = KeywordNote(
        keyword="易倍体育 活动",
        url="https://ssl-yibei.com/promotions",
        note="Current promotions and bonus offers.",
        tags=["promotions", "bonus"],
    )
    note3 = KeywordNote(
        keyword="易倍体育 帮助",
        url="https://ssl-yibei.com/help",
        note="Customer support and FAQ section.",
        tags=["support", "faq"],
    )

    collection.add_note(note1)
    collection.add_note(note2)
    collection.add_note(note3)

    print("=== All Notes ===")
    print(collection.format_all())

    print("\n=== Search by tag 'sports' ===")
    sports_notes = collection.find_by_tag("sports")
    for note in sports_notes:
        print(note.to_formatted_string())

    print("\n=== Update note for '易倍体育' ===")
    found = collection.find_by_keyword("易倍体育")
    if found:
        found.update_note("Updated: Main portal for sports betting and live games.")
        found.add_tag("updated")
        print(found.to_formatted_string())

    print("\n=== Remove '易倍体育 活动' ===")
    removed = collection.remove_note("易倍体育 活动")
    print(f"Removed: {removed}")

    print("\n=== Final Collection ===")
    print(collection.format_all())


if __name__ == "__main__":
    demo_usage()