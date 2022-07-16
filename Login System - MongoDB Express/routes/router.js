const express = require('express');
const pages = require('./controllers/pages.js');
const auth = require('./controllers/auth.js');

const router = express.Router();

// web pages
router.get('/', pages.index);
router.get('/login', pages.loginForm);
router.get('/register', pages.registerForm);

// login system
router.post('/login', auth.login);
router.post('/register', auth.register);
router.post('/logout', auth.logout);

// 404
router.use(pages.notFound);

module.exports = router;