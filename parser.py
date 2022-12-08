#!/usr/bin/env python3
import json
import sys
import pathlib
import requests
import grequests


def morph_list(
    in_encoding,
    out_encoding,
    file_name,
):

    URL = "http://localhost:8080/morph/word"
    main_path = str(pathlib.Path(__file__).parent.absolute())
    file_path = main_path + "/" + file_name.split("./")[1]
    res_dict = {}
    with open(file_path, "r") as file_path:
        for line in file_path:
            line = line.replace("\n", "")
            data = {
                "in_encoding": in_encoding,
                "out_encoding": out_encoding,
                "in_word": line,
            }
            res = requests.post(url=URL, json=data)
            res = res.json()
            res_dict[line] = res["output"]

    output_path = (
        main_path
        + "/"
        + "output"
        + "/"
        + file_name.split("/")[-1].split(".")[0]
        + "_output.txt"
    )
    with open(output_path, "w", encoding="utf-8") as outfile:
        for key in res_dict:
            finkey = convert(in_encoding, out_encoding, key)
            if res_dict[key] == "":
                outfile.write("**" + finkey + "  =>  " + "(Unknown)\n")
            else:
                outfile.write("*" + finkey + "  =>  " + res_dict[key] + "\n")

        print("Finished.")


def shloka_parse(
    in_encoding,
    out_encoding,
    file_path,
):

    URL = "http://localhost:8080/shloka"
    main_path = str(pathlib.Path(__file__).parent.absolute())
    file_path = main_path + "/" + file_path
    shloka_array = []

    with open(file_path, "r") as file_path:
        shloka = ""
        for line in file_path:
            shloka += line.replace("\n", "") + " "
            if "॥" in line:
                shloka_array.append(shloka.strip())
                shloka = ""

    print(shloka_array)
    shloka_dict_array = []

    for shloka in shloka_array:
        data = {
            "in_encoding": in_encoding,
            "out_encoding": out_encoding,
            "in_shloka": str(shloka),
        }
        shloka_dict_array.append(data)
    print(shloka_dict_array)

    reqs = (
        grequests.post(
            URL,
            json={
                "in_encoding": in_encoding,
                "out_encoding": out_encoding,
                "in_shloka": str(shloka),
            },
        )
        for shloka in shloka_array
    )

    results = grequests.map(reqs, size=len(shloka_array))

    res_array = []
    for res in results:
        res_array.append(res.json)

    for res in res_array:
        with open("parsed_result.txt") as outfile:
            outfile.write(res["original_shloka"] + "\n")
            outfile.write("Sandhi Split\n")
            outfile.write(res["sandhi_shloka"] + "\n")
            outfile.write("Samaasa Split\n")
            outfile.write(res["samaasa_shloka"] + "\n")
            outfile.write("\n")


def convert(in_encoding, out_encoding, in_word):

    URL = "http://localhost:8080/convert/word"
    data = {
        "in_encoding": in_encoding,
        "out_encoding": out_encoding,
        "in_word": in_word,
    }
    res = requests.post(url=URL, json=data)
    res = res.json()
    output = res["output"]

    return output


if __name__ == "__main__":

    option = sys.argv[1]
    in_enc = sys.argv[2]
    out_enc = sys.argv[3]
    in_file = sys.argv[4]

    encoding_list = ["WX", "VH", "KH", "SLP", "Itrans", "Unicode", "IAST"]

    if in_enc not in encoding_list:
        raise ValueError(
            "Input Encoding must be one of the following : WX, VH, KH, SLP, Itrans, Unicode, IAST"
        )
    if out_enc not in encoding_list:
        raise ValueError(
            "Output Encoding must be one of the following : WX, VH, KH, SLP, Itrans, Unicode, IAST"
        )
    if in_file == "":
        raise TypeError("File path cannot be null")

    if option == "Morph":
        morph_list(in_enc, out_enc, in_file)
    elif option == "Shloka":
        shloka_parse(in_enc, out_enc, in_file)
