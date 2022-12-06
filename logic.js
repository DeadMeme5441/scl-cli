const spawn = require("await-spawn");
const BufferList = require("bl");

const convert = async (in_encoding, out_encoding, in_word) => {
  try {
    const python = await spawn("python3", [
      "-u",
      "./scripts/convert.py",
      in_encoding,
      out_encoding,
      in_word,
    ]);
    // console.log(python.toString());
    return await python.toString();
  } catch (e) {
    // console.log(e.toString());
  }
};

const morph = async (in_encoding, out_encoding, in_word) => {
  try {
    const python = await spawn("python3", [
      "-u",
      "./scripts/morph.py",
      in_encoding,
      out_encoding,
      in_word,
    ]);
    // console.log(python.toString());
    return await python.toString();
  } catch (e) {
    // console.log(e.toString());
  }
};

const sandhi_split = async (in_encoding, out_encoding, in_word) => {
  try {
    const python = await spawn("python3", [
      "-u",
      "./scripts/sandhi_split.py",
      in_encoding,
      out_encoding,
      in_word,
    ]);
    // console.log(python.toString());
    return await python.toString();
  } catch (e) {
    // console.log(e.toString());
  }
};

const samaasa_split = async (in_encoding, out_encoding, in_word) => {
  try {
    const python = await spawn("python3", [
      "-u",
      "./scripts/samaasa_split.py",
      in_encoding,
      out_encoding,
      in_word,
    ]);
    // console.log(python.toString());
    return await python.toString();
  } catch (e) {
    // console.log(e.toString());
  }
};

const shloka_parse = async (in_encoding, out_encoding, in_shloka) => {
  let shloka_array = in_shloka.split(" ");
  let number = "";
  if (shloka_array[shloka_array.length - 1].match(/॥(.*)॥/g)) {
    number = shloka_array[shloka_array.length - 1].match(/॥(.*)॥/g)[0];

    shloka_array[shloka_array.length - 1] = shloka_array[
      shloka_array.length - 1
    ].replace(number, "");
  }
  let converted_array = await Promise.all(
    shloka_array.map((word) => {
      if (word == "।") {
        return word;
      } else {
        return convert(in_encoding, "WX", word).then((res) => {
          return res.toString().replace(/\r?\n|\r/g, "");
        });
      }
    })
  );
  let sandhi_array = await Promise.all(
    converted_array.map((word) => {
      if (word == "।") {
        return word;
      } else {
        return sandhi_split("WX", "Unicode", word).then((res) => {
          return res
            .toString()
            .replace(/\r?\n|\r/g, "")
            .split(",")[0];
          // console.log(res);
        });
      }
    })
  );
  let samaasa_array = await Promise.all(
    converted_array.map((word) => {
      if (word == "।") {
        return word;
      } else {
        return samaasa_split("WX", "Unicode", word).then((res) => {
          return res
            .toString()
            .replace(/\r?\n|\r/g, "")
            .split(",")[0];
          // console.log(res);
        });
      }
    })
  );

  let sandhi_shloka = "";
  let samaasa_shloka = "";

  sandhi_array.forEach((word) => {
    sandhi_shloka += word;
    if (word == "।") {
      sandhi_shloka += "\n";
    } else {
      sandhi_shloka += " ";
    }
  });
  sandhi_shloka += number;

  samaasa_array.forEach((word) => {
    samaasa_shloka += word;
    if (word == "।") {
      samaasa_shloka += "\n";
    } else {
      samaasa_shloka += " ";
    }
  });
  samaasa_shloka += number;
  // console.log(sandhi_shloka);
  // console.log(samaasa_shloka);
  return {
    original_shloka: in_shloka,
    sandhi_shloka: sandhi_shloka,
    samaasa_shloka: samaasa_shloka,
  };
};

module.exports = {
  convert,
  morph,
  sandhi_split,
  samaasa_split,
  shloka_parse,
};
