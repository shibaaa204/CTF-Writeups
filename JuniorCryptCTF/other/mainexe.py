import hashlib
import sys

def sha256(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()

def main():
    if len(sys.argv) < 2:
        print("Usage: ./main.py <password>")
        return

    correct_hash = "5bd3a5b6eb8d905499b19c9fc90cd447c892a571e83c0ef8a60f068ddc26c60a"
    input_password = sys.argv[1]
    input_hash = sha256(input_password)

    if input_hash == correct_hash:
        print("You are right! But flag isn't here :(")
    else:
        print("Wrong")

if __name__ == "__main__":
    main()
