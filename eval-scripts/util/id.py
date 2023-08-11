def get_ids_from_middle_in_oscillated(target_list: list):
    list_length = len(target_list)
    i_max = list_length - 1
    i_middle = int(list_length / 2)
    i_min = 0

    result = [i_middle]

    to_ascend = [i for i in range(i_middle, i_max + 1)]
    to_descend = [j for j in range(i_min, i_middle)]

    return result
