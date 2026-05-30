"""Brick 8: Command Parsing — extract action and target from transcribed text.

Pass condition: all test phrases parse correctly. No hardware needed.
This runs a set of known inputs and validates the output.
"""

import sys
import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class Command:
    action: str   # "DRIVE" or "STOP"
    target: Optional[str]

    def __repr__(self):
        return f"Command(action={self.action}, target={self.target})"


# Patterns that trigger the drive action
DRIVE_PATTERNS = [
    r"(?:drive|go|move|navigate|head)\s+to\s+(?:the\s+)?(.+)",
    r"(?:find|locate|look\s+for)\s+(?:the\s+)?(.+)",
    r"(?:hey\s+rover\s+)?(?:drive|go|find)\s+(?:to\s+)?(?:the\s+)?(.+)",
]

# Patterns that trigger a stop
STOP_PATTERNS = [
    r"^stop$",
    r"^halt$",
    r"^freeze$",
    r"stop\s+(?:now|immediately|moving)",
    r"emergency\s+stop",
]


def parse_command(text: str) -> Command:
    """Parse a transcribed text string into a Command."""
    text = text.strip().lower().rstrip('.')

    # Check stop patterns first (safety priority)
    for pattern in STOP_PATTERNS:
        if re.search(pattern, text):
            return Command(action="STOP", target=None)

    # Check drive patterns
    for pattern in DRIVE_PATTERNS:
        match = re.search(pattern, text)
        if match:
            target = match.group(1).strip().rstrip('.')
            return Command(action="DRIVE", target=target)

    # Unknown command
    return Command(action="UNKNOWN", target=None)


def main():
    test_cases = [
        ("drive to the cup", Command("DRIVE", "cup")),
        ("go to the red ball", Command("DRIVE", "red ball")),
        ("stop", Command("STOP", None)),
        ("hey rover find the cat", Command("DRIVE", "cat")),
        ("move to the chair", Command("DRIVE", "chair")),
        ("navigate to the door", Command("DRIVE", "door")),
        ("locate the blue box", Command("DRIVE", "blue box")),
        ("stop now", Command("STOP", None)),
        ("halt", Command("STOP", None)),
        ("find the water bottle", Command("DRIVE", "water bottle")),
        ("drive to cup.", Command("DRIVE", "cup")),
        ("emergency stop", Command("STOP", None)),
    ]

    passed = 0
    failed = 0

    print("Command Parser Test Suite")
    print("=" * 60)

    for text, expected in test_cases:
        result = parse_command(text)
        ok = result.action == expected.action and result.target == expected.target

        status = "PASS" if ok else "FAIL"
        if ok:
            passed += 1
        else:
            failed += 1

        print(f"  {status}: \"{text}\"")
        print(f"         -> {result}")
        if not ok:
            print(f"         expected: {expected}")

    print("=" * 60)
    print(f"Results: {passed}/{len(test_cases)} passed")

    if failed == 0:
        print("PASS: All command parsing tests passed")
        return True
    else:
        print(f"FAIL: {failed} test(s) failed")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
