const express = require("express");
const { spawn } = require("child_process");

const {
  convert,
  morph,
  sandhi_split,
  samaasa_split,
  shloka_parse,
} = require("./logic.js");

const bodyParser = require("body-parser");
const app = express();
const port = 3000;

app.use(bodyParser.json());

app.post("/convert/word", (req, res) => {
  let { in_encoding, out_encoding, in_word } = req.body;
  convert(in_encoding, out_encoding, in_word)
    .then((result) => {
      res.json({
        status: 200,
        output: result.replace(/\r?\n|\r/g, ""),
        error: "",
      });
    })
    .catch((err) => {
      res.json({
        status: 500,
        output: "",
        error: err.toString(),
      });
    });
});

app.post("/morph/word", (req, res) => {
  let { in_encoding, out_encoding, in_word } = req.body;
  morph(in_encoding, out_encoding, in_word)
    .then((result) => {
      res.json({
        status: 200,
        output: result.replace(/\r?\n|\r/g, ""),
        error: "",
      });
    })
    .catch((err) => {
      res.json({
        status: 500,
        output: "",
        error: err.toString(),
      });
    });
});

app.post("/sandhi/split", (req, res) => {
  let { in_encoding, out_encoding, in_word } = req.body;
  sandhi_split(in_encoding, out_encoding, in_word)
    .then((result) => {
      res.json({
        status: 200,
        output: result.replace(/\r?\n|\r/g, "").split(","),
        error: "",
      });
    })
    .catch((err) => {
      res.json({
        status: 500,
        output: "",
        error: err.toString(),
      });
    });
});

app.post("/samaasa/split", (req, res) => {
  let { in_encoding, out_encoding, in_word } = req.body;
  samaasa_split(in_encoding, out_encoding, in_word)
    .then((result) => {
      res.json({
        status: 200,
        output: result.replace(/\r?\n|\r/g, "").split(","),
        error: "",
      });
    })
    .catch((err) => {
      res.json({
        status: 500,
        output: "",
        error: err.toString(),
      });
    });
});

app.post("/shloka", (req, res) => {
  let { in_encoding, out_encoding, in_shloka } = req.body;

  shloka_parse(in_encoding, out_encoding, in_shloka)
    .then((result) => {
      res.send(result);
    })
    .catch((err) => {
      console.log(err);
    });
});

app.listen(port, () => console.log(`Example app listening on port ${port}!`));
