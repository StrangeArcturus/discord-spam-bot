from uuid import uuid4


def sum_of_string(string: str) -> int:
    char_answer = 0
    for i in string:
        char_answer += ord(i)
    string = str(char_answer)
    string = str(sum(map(int, list(string))))
    answer = 0
    for i in string:
        answer += int(i)
    return answer


def check_key_on_pretty(key: str) -> bool:
    return sum_of_string(key) == 8 and len(key) > 7


def generate_pretty_uuid() -> str:
    while True:
        uuid = str(uuid4())
        if check_key_on_pretty(uuid):
            print(f'finally: {uuid}')
            return uuid
        print(uuid, sum_of_string(uuid))


if __name__ == "__main__":
    print("generation unique password...")
    print(generate_pretty_uuid())
