remove_non_ascii = lambda text: "".join(
    char for char in text if 31 < ord(char) & ord(char) < 127
)

remove_cp932 = lambda text: text.encode("cp932", "ignore").decode("cp932")


def split_text(n: int, text: str) -> list[str]:
    return [text[i : i + n] for i in range(len(text) - (n - 1))]


def __get_ngram_score(text1_list: list[str], text2_list: list[str]) -> float:
    total_check_count = 0
    equal_count = 0

    for text1_word in text1_list:
        total_check_count = total_check_count + 1
        equal_flag = 0
        for text2_word in text2_list:
            if text1_word == text2_word:
                equal_flag = 1
        equal_count = equal_count + equal_flag

    return equal_count / total_check_count, (equal_count, total_check_count)


def get_ngram_score(text1: str, text2: str, n=2) -> float:
    if len(text1) == 0 or len(text2) == 0:
        # print(
        #     f"WARNING: Text_list is empty. list1:{text1_list} , list2:{text2_list}"
        # )
        return 0

    # splitting text by 2-words (for bi-gram)
    text1_list = split_text(n, text1)
    text2_list = split_text(n, text2)

    # Check the text length and change the order before performing n-gram,
    # to take care if one of the texts are included in the another one.
    if len(text2_list) > len(text1_list):
        _tmp = text1_list
        text1_list = text2_list
        text2_list = _tmp

    score, _ = __get_ngram_score(text1_list, text2_list)

    return score
