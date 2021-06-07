const express = require("express");
const { spawn } = require("child_process");
const bodyParser = require("body-parser");
const app = express();
const port = 3000;

app.use(bodyParser.json());

app.post("/convert/word", (req, res) => {
  let { in_encoding, out_encoding, in_word } = req.body;

  var dataToSend;
  var dataErr;

  const python = spawn("python3", [
    "-u",
    "./scripts/convert.py",
    in_encoding,
    out_encoding,
    in_word,
  ]);

  python.stdout.on("data", function (data) {
    console.log("Output : " + data);
    dataToSend = data.toString();
    dataToSend = dataToSend.replace(/\r?\n|\r/g, "");
  });

  python.stderr.on("data", function (data) {
    console.log("Error : " + data);
    dataErr = data.toString();
  });

  python.on("close", (code) => {
    if (code === 0) {
      res.json({
        status: 200,
        output: dataToSend,
      });
    } else {
      res.json({
        status: 500,
        output: dataToSend,
        error: dataErr,
      });
    }
  });
});

app.post("/morph/word", (req, res) => {
  let { in_encoding, out_encoding, in_word } = req.body;

  var dataToSend;
  var dataErr;

  const python = spawn("python3", [
    "-u",
    "./scripts/morph.py",
    in_encoding,
    out_encoding,
    in_word,
  ]);

  python.stdout.on("data", function (data) {
    console.log("Output : " + data);
    dataToSend = data.toString();
    dataToSend = dataToSend.replace(/\r?\n|\r/g, "");
  });

  python.stderr.on("data", function (data) {
    console.log("Error : " + data);
    dataErr = data.toString();
  });

  python.on("close", (code) => {
    if (code === 0) {
      res.json({
        status: 200,
        output: dataToSend,
      });
    } else {
      res.json({
        status: 500,
        output: dataToSend,
        error: dataErr,
      });
    }
  });
});

app.post("/sandhi/split/word", (req, res) => {
  let { in_encoding, out_encoding, in_word } = req.body;

  var dataToSend;
  var dataErr;
  var dataFromScript;

  const python = spawn("python3", [
    "-u",
    "./scripts/sandhi_split.py",
    in_encoding,
    out_encoding,
    in_word,
  ]);

  python.stdout.on("data", function (data) {
    console.log("Output : " + data);
    dataFromScript = data.toString();
    dataFromScript = dataFromScript.replace(/\r?\n|\r/g, "");
    dataToSend = dataFromScript.split(",");
  });

  python.stderr.on("data", function (data) {
    console.log("Error : " + data);
    dataErr = data.toString();
  });

  python.on("close", (code) => {
    if (code === 0) {
      res.json({
        status: 200,
        output: dataToSend,
      });
    } else {
      res.json({
        status: 500,
        output: dataToSend,
        error: dataErr,
      });
    }
  });
});
app.post("/samaasa/split/word", (req, res) => {
  let { in_encoding, out_encoding, in_word } = req.body;

  var dataToSend;
  var dataErr;
  var dataFromScript;

  const python = spawn("python3", [
    "-u",
    "./scripts/samaasa_split.py",
    in_encoding,
    out_encoding,
    in_word,
  ]);

  python.stdout.on("data", function (data) {
    console.log("Output : " + data);
    dataFromScript = data.toString();
    dataFromScript = dataFromScript.replace(/\r?\n|\r/g, "");
    dataToSend = dataFromScript.split(",");
  });

  python.stderr.on("data", function (data) {
    console.log("Error : " + data);
    dataErr = data.toString();
  });

  python.on("close", (code) => {
    if (code === 0) {
      res.json({
        status: 200,
        output: dataToSend,
      });
    } else {
      res.json({
        status: 500,
        output: dataToSend,
        error: dataErr,
      });
    }
  });
});

app.listen(port, () => console.log(`Example app listening on port ${port}!`));
