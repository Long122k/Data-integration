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
  res.render("home", { items: db, values: req.body });
  console.log(req.body);
});

app.listen(3000, () => {
  console.log(`Server started http://localhost:3000`);
});
