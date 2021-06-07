#!/usr/bin/env python3
import re
import sys
import pathlib
import subprocess
import convert

path = pathlib.Path(__file__).parent.absolute()
path = str(path.parents[0])


def split_samaasa(in_word, in_encoding, out_encoding):

    if in_encoding != "WX":
        in_word = convert.convert_to_wx(in_encoding, in_word)

    main_path = path + "/SHMT/prog/sandhi_splitter"
    bin_path = path + "/morph_bin/samAsa_splitter.bin"

    word_file = open(main_path + "/tmp.txt", "w")
    word_file.write(in_word)
    word_file.close()
    # print(path)
    # print(main_path)
    # print(bin_path)

    out = subprocess.run(
        [
            main_path + "/sandhi_samaasa_splitter.out",
            "-t",
            "-s",
            main_path + "/samAsa_words.txt",
            main_path + "/samAsa_rules.txt",
            "/usr/bin/lt-proc",
            bin_path,
            main_path + "/tmp.txt",
            "4",
        ],
        cwd=main_path,
        stdout=subprocess.PIPE,
    )

    output = out.stdout
    output = output.decode("utf-8")

    outfile = open("sam_output.txt", "w")
    outfile.write(output)
    outfile.close()

    ps = subprocess.run(
        ["tail", "-n", "+3", main_path + "/full_output"],
        cwd=main_path,
        stdout=subprocess.PIPE,
    )
    tmpout = open(main_path + "/sam_tmpout.txt", "w")
    tmpout.write(ps.stdout.decode("utf-8"))
    tmpout.close()

    out = subprocess.run(
        ["cut", "-f1", main_path + "/sam_tmpout.txt"],
        cwd=main_path,
        stdout=subprocess.PIPE,
    )

    finout = open(main_path + "/sam_finout.txt", "w")
    finout.write(out.stdout.decode("utf-8"))
    finout.close()
    output = ""

    with open(main_path + "/sam_finout.txt", "r") as finalout:
        for line in finalout:
            con = line.strip()
            output += convert.convert_from_wx(out_encoding, con)
            output += ","

    return output


if __name__ == "__main__":

    in_enc = sys.argv[1]
    out_enc = sys.argv[2]
    in_wd = sys.argv[3]

    print(split_samaasa(in_wd, in_enc, out_enc), flush=True)
