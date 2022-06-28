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

app.get("/", function (req, res) {
  res.render("home");
});

app.post("/", function (req, res) {
  // const text_search = `${req.body.search} ${req.body.branch} ${req.body.storage} ${req.body.size} ${req.body.camera} ${req.body.price} ${req.body.ram}`;
  var data = Object.values(req.body);
  var results = data.filter((item) => {
    return item !== "None";
  });
  var items = [];
  const text_search = results.join(" ");
  axios.get(`http://localhost:8001/${text_search}`).then(function (resp) {
    items = resp.data;
    return res.render("home", { items: items });
  });
});

app.listen(3000, () => {
  console.log(`Server started http://localhost:3000`);
});
