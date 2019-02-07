from typing import List


def flat(some_list: List[List]) -> List:
    return [item for sublist in some_list for item in sublist]
