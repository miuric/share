from typing import List


# region 前置后置截取后字符串
def sub_str(ori_words: str, start_words: List[str], end_words: List[str]) -> str:
    pos_s = _start_str_pos(ori_words, start_words)
    pos_e = _end_str_pos(ori_words, end_words)

    new_str = ori_words[pos_s: pos_e].strip()

    return new_str


# endregion

# region 前置
def _start_str_pos(ori_words: str, start_words: List[str]) -> int:
    sw_last = ''
    sw_pos_tmp = 0

    for sw in start_words:
        temp_pos = ori_words.rfind(sw)
        if temp_pos > sw_pos_tmp:
            sw_last = sw
            sw_pos_tmp = temp_pos

    sw_pos = 0 if not sw_last else sw_pos_tmp + len(sw_last)

    return sw_pos


# endregion


# region 后置
def _end_str_pos(ori_words: str, end_words: List[str]) -> int:
    ew_first = ''
    ew_pos_tmp = len(ori_words)

    for ew in end_words:
        temp_pos = ori_words.find(ew)
        if temp_pos < ew_pos_tmp:
            ew_first = ew
            ew_pos_tmp = temp_pos

    ew_pos = len(ori_words) if not ew_first else ew_pos_tmp
    return ew_pos
# endregion
