const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
    username: {
        type: String,
        required: true,
        maxLength: 16,
        minLength: 1,
    },
    password: {
        type: String,
        required: true,
        minLength: 1,
    }
}, { timestamps: true });

const User = mongoose.model("user", userSchema);
module.exports = User;