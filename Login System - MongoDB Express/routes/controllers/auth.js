const bcrypt = require('bcrypt');
const User = require('../../models/user');

const login = async (req, res) => {
    const username = req.body.user;
    const password = req.body.pass;

    const user = await User.findOne({username: username});
    if (!user) {
        res.render('login', {title: 'Login', error: "User does not exist"});
        return;
    }

    const match = await bcrypt.compare(password, user.password);
    if (!match) {
        res.render('login', {title: 'Login', error: "Incorrect Password"});
        return;
    }

    // login
    req.session.username = username;
    res.redirect('/');
}

const register = async (req, res) => {
    const username = req.body.user;
    const password = req.body.pass;

    // Username taken
    const taken = await User.exists({username: username});
    if (taken) {
        res.render('register', {title: 'Register', error: "Username is taken"});
        return;
    } 

    const hash = await bcrypt.hash(password, 11);
    try {
        await User.create({
            username: username,
            password: hash
        });
    } catch (e) {
        res.render('register', {title: 'Register', error: "Invalid Input"});
        return;
    }

    // login
    req.session.username = username;
    res.redirect('/');
}

const logout = (req, res) => {
    req.session.destroy();
    res.sendStatus(200);
}

module.exports = {
    login,
    register,
    logout
}