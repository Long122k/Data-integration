const axios = require("axios");
const express = require("express");
const hbs = require("express-handlebars");
const path = require("path");
const app = express();
const db = require("./db/test");
var cookieParser = require("cookie-parser");
app.use(express.json());
var handlebars = hbs.create({
  extname: ".hbs",
});
app.engine(".hbs", handlebars.engine);
app.set("view engine", "hbs");
app.set("views", path.join(__dirname, "resources/views"));
app.use(express.static(path.join(__dirname, "public")));
app.use(express.urlencoded());

// db.connect();
function getNumber(string) {
  let number = "";
  for (let i in string) {
    let c = string[i];
    if ((c >= 0 && c <= 9) || c == ".") number = number + c;
  }
  return number + "đ";
}
app.get("/", function (req, res) {
  res.render("home");
});
// app.get("/home/True", function (req, res) {
//   console.log(req.params.search);
//   var data = Object.values("body", req.body);
//   var results = data.filter((item) => {
//     return item !== "None";
//   });
//   var items = [];
//   const text_search = results.join(" ");
//   // console.log(req.params.sort);
//   // axios.get(`http://localhost:8001/${text_search}/True`).then(function (resp) {
//   //   items = resp.data;
//   //   // req.body = items[1];
//   //   // items[3] = getNumber(items[3]);
//   //   for (let i in items[0]) {
//   //     items[0][i]["price"] = getNumber(items[0][i]["price"]);
//   //     // console.log(items[i]);
//   //   }
//   //   // console.log(items[3]);
//   //   // var array = items[0];
//   //   // array.sort((a, b) => (a.price > b.price ? 1 : -1));
//   //   return res.render("home", { items: items[0], values: items[1] });
//   // });
//   console.log(data);
//   console.log(text_search);
// });

app.post("/", function (req, res) {
  // const text_search = `${req.body.search} ${req.body.branch} ${req.body.storage} ${req.body.size} ${req.body.camera} ${req.body.price} ${req.body.ram}`;
  console.log(req.body.search);
  const sort = req.body.sort;
  // var data = Object.values(req.body.search);
  // var results = data.filter((item) => {
  //   return item !== "None";
  // });
  // var items = [];
  // const text_search = results.join(" ");

  const text_search = req.body.search;
  axios.get(`http://localhost:8001/${text_search}`).then(function (resp) {
    items = resp.data;
    console.log(items);
    // req.body = items[1];
    // items[3] = getNumber(items[3]);
    for (let i in items[0]) {
      items[0][i]["price"] = getNumber(items[0][i]["price"]);
      // console.log(items[i]);
    }
    console.log(items[0]);
    console.log(sort);
    var array = items[0];
    console.log(array);
    if (sort === "asc") {
      array.sort((a, b) => (a.price > b.price ? 1 : -1));
    } else {
      array.sort((a, b) => (a.price > b.price ? -1 : 1));
    }
    return res.render("home", { items: items[0], values: text_search });
  });
});

app.listen(3000, () => {
  console.log(`Server started http://localhost:3000`);
});
