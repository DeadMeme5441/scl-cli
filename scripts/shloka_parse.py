#!/usr/bin/env python3
import re
import sys
import pathlib
import subprocess
import convert
import morph
import sandhi_split
import samaasa_split

path = pathlib.Path(__file__).parent.absolute()
path = str(path.parents[0])


def parse_shloka(in_encoding, out_encoding, in_shloka):

    shloka_array = re.split(r"\s|\|", in_shloka)
    number = re.search("\॥(.*)\॥", shloka_array[-1]).group()
    shloka_array[-1] = re.sub("\॥(.*)\॥", "", shloka_array[-1])
    print(shloka_array)

    final_array = []
    for word in shloka_array:
        res = convert.convert_to_wx(in_encoding, word)
        res = convert.normalize(res)
        print(res)
        final_array.append(res)

    print(final_array)

    sandhi_array = []
    samaasa_array = []

    for word in final_array:
        print(word)
        try:
            san_res = sandhi_split.split_sandhi(word, "WX", "WX").split(" ")[0]
        except IndexError:
            san_res = ""
        if san_res == "":
            san_res = word
        sandhi_array.append(san_res)

    for word in final_array:
        print(word)
        try:
            sam_res = samaasa_split.split_samaasa(word, "WX", "WX").split(" ")[0]
        except IndexError:
            sam_res = ""
        if sam_res == "":
            sam_res = word
        sandhi_array.append(sam_res)

    sandhi_result = ""
    samaasa_result = ""

    for word in sandhi_array:
        word = convert.convert_from_wx(out_encoding, word)
        sandhi_result += word
        sandhi_result += " "
        if word == "।":
            sandhi_result += "\n"

    for word in samaasa_array:
        word = convert.convert_from_wx(out_encoding, word)
        samaasa_result += word
        samaasa_result += " "
        if word == "।":
            samaasa_result += "\n"

    return sandhi_result + "||" + samaasa_result


if __name__ == "__main__":

    in_enc = sys.argv[1]
    out_enc = sys.argv[2]
    in_shlk = sys.argv[3]

    print(parse_shloka(in_enc, out_enc, in_shlk))
