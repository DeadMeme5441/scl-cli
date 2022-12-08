import sys
import pathlib
import requests
import grequests


def main(in_file):
    main_path = str(pathlib.Path(__file__).parent.absolute())

    input_path = main_path + "/" + "files" + "/" + in_file.split("/")[-1]

    output_path = (
        main_path
        + "/"
        + "output"
        + "/"
        + in_file.split("/")[-1].split(".")[0]
        + "_output.txt"
    )

    final_output = (
        main_path
        + "/"
        + "final_output"
        + "/"
        + in_file.split("/")[-1].split(".")[0]
        + "_output.txt"
    )
    input_words = []

    with open(input_path, "r") as in_file:
        for line in in_file:
            line = line.replace("\n", "")
            word = convert("WX", "Unicode", line)
            input_words.append(word)

    output_words = {}

    with open(output_path, "r") as out_file:
        for line in out_file:
            word, morphology = line.replace("\n", "").split("=>")
            word = word.strip().replace("*", "")
            morphology = morphology.strip()
            output_words[word] = morphology

    print(len(output_words))

    with open(final_output, "w", encoding="utf-8") as final_out:
        for word in input_words:
            final_out.write(word + " => " + output_words[word] + "\n")


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

    in_file = sys.argv[1]

    main(in_file)
