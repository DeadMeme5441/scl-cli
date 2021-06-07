"""
File that handles all conversions to wx form - use this with file arguments on CLI
Arguments : Input Encoding, Input Word
Output : Converted Word to wx form
"""
import sys
import pathlib
import subprocess

path = pathlib.Path(__file__).parent.absolute()
path = str(path.parents[0])
path = path + "/converters"
norm_path = path + "/SHMT/prog/Normalisation"


def convert_to_wx(encoding, in_word):
    in_word = in_word.strip()
    in_word = in_word + "\n"
    conversion_prog = ""

    if encoding == "VH":
        conversion_prog = path + "/velthuis-wx.out"
    elif encoding == "KH":
        conversion_prog = path + "/kyoto_ra.out"
    elif encoding == "SLP":
        conversion_prog = path + "/slp2wx.out"
    elif encoding == "Itrans":
        conversion_prog = path + "/itrans_ra.out"
    elif encoding == "Unicode":
        conversion_prog = path + "/utf82wx.sh"
    elif encoding == "IAST":
        conversion_prog = path + "/utf8roman2wx.out"

    proc = subprocess.Popen(
        [conversion_prog],
        shell=True,
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    res, err = proc.communicate(input=bytes(in_word, "utf-8"))
    res = res.decode("utf-8").rstrip("\n")
    err = err.decode("utf-8").rstrip("\n")

    return res


def convert_from_wx(encoding, in_word):

    in_word = in_word.strip()
    in_word = in_word + "\n"
    conversion_prog = ""
    if encoding == "VH":
        conversion_prog = path + "/wx-velthuis.out"
    elif encoding == "KH":
        conversion_prog = path + "/ra_kyoto.out"
    elif encoding == "SLP":
        conversion_prog = path + "/wx2slp.out"
    elif encoding == "Itrans":
        conversion_prog = (
            path
            + "/ra_itrans.out | "
            + path
            + "/rm__between_vowels.out | "
            + path
            + "/ri"
        )
    elif encoding == "Unicode":
        conversion_prog = path + "/wx2utf8.sh"
    elif encoding == "IAST":
        conversion_prog = path + "/wx2utf8roman.out"

    proc = subprocess.Popen(
        [conversion_prog],
        shell=True,
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    res, err = proc.communicate(input=bytes(in_word, "utf-8"))
    try:
        res = res.decode("utf-8").rstrip("\n")
    except UnicodeDecodeError:
        res = str(res)

    err = err.decode("utf-8").rstrip("\n")

    return res


def normalize(in_word):

    proc = subprocess.Popen(
        [norm_path + "/get_std_spelling.out"],
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )

    res, err = proc.communicate(input=bytes(in_word, "utf-8"))
    output = res.decode("utf-8").rstrip("\n")

    return output


if __name__ == "__main__":

    in_encoding = sys.argv[1]
    out_encoding = sys.argv[2]
    in_word = sys.argv[3]

    encoding_list = ["WX", "VH", "KH", "SLP", "Itrans", "Unicode", "IAST"]

    if in_encoding not in encoding_list:
        raise ValueError(
            "Input Encoding must be one of the following : WX, VH, KH, SLP, Itrans, Unicode, IAST"
        )
    if out_encoding not in encoding_list:
        raise ValueError(
            "Output Encoding must be one of the following : WX, VH, KH, SLP, Itrans, Unicode, IAST"
        )
    if in_word == "":
        raise TypeError("Input word must be a non-null string literal")

    if out_encoding == "WX":
        print(convert_to_wx(in_encoding, in_word), flush=True)
    elif out_encoding != "WX":
        print(convert_from_wx(out_encoding, in_word), flush=True)
