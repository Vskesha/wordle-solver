import json
import random
from pathlib import Path

from colorama import init as init_colorama, Fore

init_colorama()

WORDS_JSON_FILE_PATH = Path(__file__).parent.joinpath("words/words.json")

GUESS_COMMAND = Fore.YELLOW + "filter CCCCC XXXXX " + Fore.GREEN + """- For filtering words.
                     CCCCC - 5 characters word (case insensitive)
                     XXXXX - where X is one of:
                         0 - letter is not present in the word
                         1 - letter is on wrong position
                         2 - letter is on correct position
"""
HELP = (Fore.BLUE + "Available commands: \n" +
Fore.YELLOW + "help               " + Fore.GREEN + "- Display this help message\n" +
Fore.YELLOW + "start              " + Fore.GREEN + "- Start a new game\n" +
Fore.YELLOW + "quit               " + Fore.GREEN + "- Exit the game\n" +
Fore.YELLOW + "exit               " + Fore.GREEN + "- Exit the game\n" +
Fore.YELLOW + "show N             " + Fore.GREEN + "- Show N random words that fit.\n" +
GUESS_COMMAND)



def get_words_from_json(
        json_file_path: str | Path,
        min_length: int = 1,
        max_length: int = 100,
        upper_case: bool = True,
) -> list[str]:
    try:
        with open(json_file_path, "r", encoding="utf-8") as file:
            json_data = json.load(file)
            return [
                word.upper() if upper_case else word.lower()
                for word in json_data.keys()
                if min_length <= len(word) <= max_length
            ]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []
    except Exception:
        return []


def get_words_from_txt(txt_file_path: str | None) -> str:
    ...


def show_words(words: list[str], num_words: int = 10) -> None:
    if not words:
        print(Fore.RED + "No more words to show." + Fore.GREEN)
        return

    random.shuffle(words)
    print(Fore.CYAN + "\n".join(words[:num_words]) + Fore.GREEN)


def main():
    words = get_words_from_json(WORDS_JSON_FILE_PATH, 5, 5)
    random.shuffle(words)

    print(HELP)

    while True:
        command = input(">>> ").lower()

        if command.startswith("help"):
            print(HELP)

        elif command.startswith("start"):
            main()
            break

        elif command in ("quit", "exit"):
            print(Fore.GREEN + "Goodbye!")
            break

        elif command.startswith("show"):
            splitted = command.split()
            num_words = 10
            if len(splitted) > 1 and splitted[1].isdigit():
                num_words = int(splitted[1])
            show_words(words, num_words)

        elif command.startswith("filter"):
            splitted = command.split()
            if len(splitted) != 3:
                print(Fore.RED + "Invalid command. Please use the format:")
                print(GUESS_COMMAND)
                continue
            elif len(splitted[1]) != 5 or len(splitted[2]) != 5:
                print(Fore.RED + "Invalid word length. Words must be 5 characters long.")
                print(GUESS_COMMAND)
                continue
            elif any(digit not in "012" for digit in splitted[2]):
                print(Fore.RED + "Invalid guess. Guess must contain only 0, 1, or 2.")
                print(GUESS_COMMAND)
                continue

            _, quess, presence = splitted
            for i, char, pres in zip(range(5), quess.upper(), presence):
                if pres == "0":
                    words = [
                        word for word in words
                        if char not in word
                    ]
                elif pres == "1":
                    words = [
                        word for word in words
                        if char in word and word[i] != char
                    ]
                elif pres == "2":
                    words = [
                        word for word in words
                        if word[i] == char
                    ]

            show_words(words, 10)

        else:
            print(Fore.RED + "Invalid command. Please use the format:")
            print(HELP)


if __name__ == '__main__':
    main()
