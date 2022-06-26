const mongoose = require("mongoose");

async function connect() {
  try {
    await mongoose.connect("mongodb://localhost:27017/name_db");
    console.log("Connect successful");
  } catch (error) {
    console.error(error);
  }
}

module.exports = { connect };
