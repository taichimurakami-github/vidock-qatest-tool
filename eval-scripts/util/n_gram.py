import numpy as np


def __split_text(n: int, text: str) -> list[str]:
    return [text[i : i + n] for i in range(len(text) - (n - 1))]


def __get_ngvec_dict(n: int, text: str):
    ngram_vector = {}
    for i in range(len(text) - (n - 1)):
        if text[i : i + n] in ngram_vector.keys():
            ngram_vector[text[i : i + n]] += 1
        else:
            ngram_vector[text[i : i + n]] += 1

    return ngram_vector


def __merge_ngvector_keys(ngvec_1: dict, ngvec_2: dict) -> tuple[dict, dict]:
    for key in ngvec_2.keys():
        if key not in ngvec_1.keys():
            ngvec_1[key] = 0

    for key in ngvec_1.keys():
        if key not in ngvec_2.keys():
            ngvec_2[key] = 0

    assert len(ngvec_1.keys()) == len(ngvec_2.keys())

    return ngvec_1, ngvec_2


def __get_ngvec_cosine(ngram_vec_dict1: dict, ngram_vec_dict2: dict):
    sorted(ngram_vec_dict1.items(), key=lambda pair: pair[0])
    sorted(ngram_vec_dict2.items(), key=lambda pair: pair[0])
    arr1 = np.array(
        [
            i[1]
            for i in sorted(ngram_vec_dict1.items(), key=lambda pair: pair[0])
        ]
    )
    arr2 = np.array(
        [
            i[1]
            for i in sorted(ngram_vec_dict2.items(), key=lambda pair: pair[0])
        ]
    )
    if arr1.shape == arr2.shape:
        return np.dot(arr1, arr2.transpose()) / (
            np.linalg.norm(arr1) * np.linalg.norm(arr2)
        )
    else:
        raise ValueError("Data fmt is different.")


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


def get_similarity_score(text1: str, text2: str, n=2) -> float:
    if len(text1) == 0 or len(text2) == 0:
        # print(
        #     f"WARNING: Text_list is empty. list1:{text1_list} , list2:{text2_list}"
        # )
        return 0

    # splitting text by 2-words (for bi-gram)
    text1_list = __split_text(n, text1)
    text2_list = __split_text(n, text2)

    # Check the text length and change the order before performing n-gram,
    # to take care if one of the texts are included in the another one.
    if len(text2_list) > len(text1_list):
        _tmp = text1_list
        text1_list = text2_list
        text2_list = _tmp

    score, _ = __get_ngram_score(text1_list, text2_list)

    return score


def get_text_vector(text1: str, text2: str, n=2) -> list[int]:
    text1_ngvec = __get_ngvec_dict(n, text1)
    text2_ngvec = __get_ngvec_dict(n, text2)

    __merge_ngvector_keys(text1_ngvec, text2_ngvec)

    return __get_ngvec_cosine(text1_ngvec, text2_ngvec)

    get_text_vector()
