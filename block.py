import os
import json
import hashlib
from typing import NoReturn


BLOCKCHAIN_DIR = "blockchain/"


def get_hash(prev_block: str) -> str:
    with open(BLOCKCHAIN_DIR + prev_block, "rb") as f:
        content = f.read()
    return hashlib.md5(content).hexdigest()


def check_integrity() -> list[dict]:
    files = sorted(os.listdir(BLOCKCHAIN_DIR), key=lambda x: int(x))
    results = []

    for file in files[1:]:
        with open(BLOCKCHAIN_DIR + file) as f:
            block = json.load(f)

        prev_hash = block.get("prev_block").get("hash")
        prev_filename = block.get("prev_block").get("filename")
        actual_hash = get_hash(prev_filename)

        if prev_hash == actual_hash:
            res = "ok"
        else:
            res = "was changed"

        print(f"Block {prev_filename}: {res}")
        results.append({'block': prev_filename, 'result': res})
    
    return results


def write_block(borrower: str, lender: str, amount: int) -> NoReturn:
    blocks_count = len(os.listdir(BLOCKCHAIN_DIR))
    prev_block = str(blocks_count)

    data = {
        "borrower": borrower,
        "lender": lender,
        "amount": amount,
        "prev_block": {"hash": get_hash(prev_block), "filename": prev_block},
    }

    current_block = BLOCKCHAIN_DIR + str(blocks_count + 1)
    with open(current_block, "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.write("\n")


def main():
    # write_block("Kate", "Linda", 100)
    check_integrity()


if __name__ == "__main__":
    main()
