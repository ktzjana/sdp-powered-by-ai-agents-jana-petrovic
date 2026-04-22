from dataclasses import dataclass


@dataclass
class Command:
    action: str
    row: int | None = None
    col: int | None = None


class InputParser:
    @staticmethod
    def parse(raw: str) -> Command:
        parts = raw.strip().split()
        if parts[0] == "r" and len(parts) == 3:
            return Command(action="reveal", row=int(parts[1]), col=int(parts[2]))
        if parts[0] == "f" and len(parts) == 3:
            return Command(action="flag", row=int(parts[1]), col=int(parts[2]))
        raise ValueError(f"Invalid input: {raw!r}")
