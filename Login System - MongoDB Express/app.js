const express = require("express");
const mongoose = require("mongoose");
const cookieParser = require('cookie-parser');
const expressSession = require('express-session');
const router = require('./routes/router');

const app = express();

// mongodb
const dbURI = "mongodb+srv://<username>:<password>@basic-express-login.lsp8qim.mongodb.net/<dbname>?retryWrites=true&w=majority";
mongoose.connect(dbURI, { useNewUrlParser: true, useUnifiedTopology: true})
    .then((res) => app.listen(8080))
    .catch((err) => console.log(err));

// view engine
app.set('view engine', 'ejs');

// static files
app.use(express.static('public'));

// middleware
app.use(express.urlencoded({extended: true}));
app.use(cookieParser());
app.use(expressSession({
    secret: "secret",
    saveUninitialized: true,
    cookie: {maxAge: 100 * 60 * 60 * 24},
    resave: false
}));

// router
app.use(router);