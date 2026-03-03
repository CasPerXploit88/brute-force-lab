import string
import time
from itertools import product

charset = string.ascii_letters + string.digits + string.punctuation
TIMEOUT = 30

def load_wordlist():
    try:
        with open("wordlist.txt", "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                yield line.strip()
    except FileNotFoundError:
        return

def dictionary_attack(target):
    attempts = 0
    start = time.time()

    for word in load_wordlist():
        attempts += 1
        if word == target:
            duration = round(time.time() - start, 4)
            return {
                "found": True,
                "password": word,
                "attempts": attempts,
                "time_taken": duration,
                "method": "Dictionary Attack",
                "strength": rate_strength(target),
                "timeout": False
            }

    duration = round(time.time() - start, 4)
    return {
        "found": False,
        "attempts": attempts,
        "time_taken": duration,
        "method": "Dictionary Attack",
        "strength": rate_strength(target),
        "timeout": False
    }

def brute_force(target, max_length=8):
    attempts = 0
    start = time.time()

    for length in range(1, max_length + 1):
        for combo in product(charset, repeat=length):
            if time.time() - start > TIMEOUT:
                duration = round(time.time() - start, 4)
                return {
                    "found": False,
                    "attempts": attempts,
                    "time_taken": duration,
                    "method": "Brute Force",
                    "strength": rate_strength(target),
                    "timeout": True
                }

            guess = ''.join(combo)
            attempts += 1

            if guess == target:
                duration = round(time.time() - start, 4)
                return {
                    "found": True,
                    "password": guess,
                    "attempts": attempts,
                    "time_taken": duration,
                    "method": "Brute Force",
                    "strength": rate_strength(target),
                    "timeout": False
                }

    duration = round(time.time() - start, 4)
    return {
        "found": False,
        "attempts": attempts,
        "time_taken": duration,
        "method": "Brute Force",
        "strength": rate_strength(target),
        "timeout": False
    }

def smart_crack(target):
    dict_result = dictionary_attack(target)
    if dict_result["found"]:
        return dict_result
    brute_result = brute_force(target)
    return brute_result

def rate_strength(password):
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)

    score = 0
    if length >= 4: score += 1
    if length >= 6: score += 1
    if has_upper: score += 1
    if has_digit: score += 1
    if has_symbol: score += 1

    if score <= 1:
        return "Very Weak"
    elif score == 2:
        return "Weak"
    elif score == 3:
        return "Moderate"
    elif score == 4:
        return "Strong"
    else:
        return "Very Strong"

def log_result(password, result):
    import os
    os.makedirs("results", exist_ok=True)
    with open("results/logs.txt", "a") as f:
        f.write(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}]\n")
        f.write(f"Password Length : {len(password)} characters\n")
        f.write(f"Method Used     : {result['method']}\n")
        f.write(f"Found           : {result['found']}\n")
        f.write(f"Timeout         : {result['timeout']}\n")
        f.write(f"Attempts        : {result['attempts']}\n")
        f.write(f"Time Taken      : {result['time_taken']}s\n")
        f.write(f"Strength        : {result['strength']}\n")
        f.write("-" * 40)