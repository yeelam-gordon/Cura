import argparse
import hashlib
import json
import struct
import sys
from pathlib import Path, PurePosixPath


MACHINES = {"arm64": 0xAA64, "x64": 0x8664}
PE_SUFFIXES = {".exe", ".dll", ".pyd"}


def read_machine(path: Path) -> int:
    with path.open("rb") as stream:
        if stream.read(2) != b"MZ":
            raise ValueError("missing MZ header")
        stream.seek(0x3C)
        offset_bytes = stream.read(4)
        if len(offset_bytes) != 4:
            raise ValueError("truncated DOS header")
        pe_offset = struct.unpack("<I", offset_bytes)[0]
        stream.seek(pe_offset)
        if stream.read(4) != b"PE\0\0":
            raise ValueError("missing PE signature")
        machine_bytes = stream.read(2)
        if len(machine_bytes) != 2:
            raise ValueError("truncated COFF header")
        return struct.unpack("<H", machine_bytes)[0]


def candidates(root: Path) -> list[tuple[str, Path]]:
    if root.is_file():
        return [(root.name, root)] if root.suffix.lower() in PE_SUFFIXES else []
    if not root.is_dir():
        return []
    files = [
        (path.relative_to(root).as_posix(), path)
        for path in root.rglob("*")
        if path.is_file() and path.suffix.lower() in PE_SUFFIXES
    ]
    return sorted(files, key=lambda item: (item[0].casefold(), item[0]))


def validate(
    root: Path,
    architecture: str,
    required: list[str],
    manifest_out: Path | None,
) -> int:
    expected = MACHINES[architecture]
    found = candidates(root)
    failures: list[str] = []
    records = []

    if not found:
        failures.append(f"{root}: no PE candidates found")

    found_paths = {relative.casefold() for relative, _ in found}
    for required_path in required:
        normalized = PurePosixPath(required_path.replace("\\", "/")).as_posix()
        if normalized.casefold() not in found_paths:
            failures.append(f"missing required PE: {normalized}")

    for relative, path in found:
        try:
            machine = read_machine(path)
            data = path.read_bytes()
            records.append(
                {
                    "path": relative,
                    "size": len(data),
                    "sha256": hashlib.sha256(data).hexdigest(),
                    "machine": f"0x{machine:04X}",
                }
            )
            if machine != expected:
                failures.append(
                    f"{relative}: machine 0x{machine:04X}, expected 0x{expected:04X}"
                )
        except (OSError, ValueError, struct.error) as error:
            failures.append(f"{relative}: {error}")

    if manifest_out is not None and not failures:
        manifest = {
            "schema_version": 1,
            "architecture": architecture,
            "expected_machine": f"0x{expected:04X}",
            "files": records,
        }
        manifest_out.parent.mkdir(parents=True, exist_ok=True)
        manifest_out.write_text(
            json.dumps(manifest, sort_keys=True, separators=(",", ":")) + "\n",
            encoding="utf-8",
        )

    for failure in failures:
        print(f"ERROR: {failure}", file=sys.stderr)
    return 1 if failures else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Windows PE architecture.")
    parser.add_argument("path", type=Path)
    parser.add_argument("--architecture", required=True, choices=sorted(MACHINES))
    parser.add_argument("--require", action="append", default=[])
    parser.add_argument("--manifest-out", type=Path)
    args = parser.parse_args(argv)
    return validate(args.path, args.architecture, args.require, args.manifest_out)


if __name__ == "__main__":
    raise SystemExit(main())
