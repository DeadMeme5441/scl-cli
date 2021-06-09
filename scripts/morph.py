#!/usr/bin/env python3
import re
import sys
import pathlib
import subprocess
import convert

path = pathlib.Path(__file__).parent.absolute()
path = str(path.parents[0])


def get_morph(in_word, in_encoding, out_encoding):
    in_word = in_word.strip()
    in_word = in_word + "\n"

    if in_encoding != "WX":
        in_word = convert.convert_to_wx(in_encoding, in_word)

    all_morf_path = "lt-proc " + path + "/morph_bin/all_morf.bin "

    morph1 = subprocess.Popen(
        [all_morf_path],
        shell=True,
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    res, err = morph1.communicate(input=bytes(in_word, "utf-8"))

    try:
        res = res.decode("utf-8").rstrip("\n")
    except UnicodeDecodeError:
        res = str(res)

    in_word = re.sub(r"/", "=", res, 1)
    in_word = re.sub(r"^.*=\*.*", "", in_word, 1)
    in_word = re.sub(r".*=", "", in_word, 1)
    in_word = re.sub(r"^^", "", in_word, 1)

    modify_path = path + "/SHMT/prog/interface/modify.pl"
    modify = subprocess.Popen(
        [modify_path],
        shell=True,
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    res, err = modify.communicate(input=bytes(in_word, "utf-8"))

    try:
        res = res.decode("utf-8").rstrip("\n")
    except UnicodeDecodeError:
        res = str(res)

    in_word = re.sub(r"\/\/\+/\/", "", res)
    in_word = re.sub(r"\/$", "", in_word, 1)
    in_word = re.sub(r"^\/", "", in_word, 1)
    in_word = re.sub(r"\$", "", in_word)
    in_word = re.sub(r"<", "{", in_word)
    in_word = re.sub(r">", "}", in_word)
    in_word = re.sub(r":", " ", in_word)

    if out_encoding != "WX":
        output = convert.convert_from_wx(out_encoding, in_word)

    return output


if __name__ == "__main__":

    in_enc = sys.argv[1]
    out_enc = sys.argv[2]
    in_wd = sys.argv[3]

    print(get_morph(in_wd, in_enc, out_enc), flush=True)
