
// Make sure these redirect to hoem page if the user is logged in. (load dashboard instead of index as well)
// Change this file to web pages, make separate files for post requests...

const index = (req, res) => {
    if (req.session.username) {
        res.render('dashboard', {title: "Home", username: req.session.username});
        return;
    }
    res.render('index', {title: "Home"});
}

const loginForm = (req, res) => {
    if (req.session.username) {
        res.redirect("/");
        return;
    }
    res.render('login', {title: "Login"});
}

const registerForm = (req, res) => {
    if (req.session.username) {
        res.redirect("/");
        return;
    }
    res.render('register', {title: "Register"});
}

const notFound = (req, res) => {
    res.status(404).render('404', {title: "404 Not Found"});
}

module.exports = {
    index,
    loginForm,
    registerForm,
    notFound
}