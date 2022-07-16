<?php
    define("__ACCESSIBLE__", true);
    require_once("inc/config.php");
?>
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, intial-scale=1.0">
        <link rel="stylesheet" href="assets/css/style.css">
        <script defer src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
        <script defer src="assets/js/login.js"></script>
        <title>Login - My website</title>
    </head>
    <body>
        <?php require_once("inc/navbar.php"); ?>

        <div class="form-container">
            <form id="login-form">
                <div>Login</div>

                <label for="username">Username</label> <br>
                <input type="text" name="username" required="required" placeholder="Enter your username"> <br>

                <label for="password">Password</label> <br>
                <input type="password" name="password" required="required" placeholder="Enter your password"> <br>

                <div id="form-error" style="display: none;"></div>
                <input type="submit" name="submit" value="LOGIN"> <br>

                <div>
                    Don't have an account?
                    <a href="register.php">Register here.</a>
                </div>
            </form>
        </div>

    </body>
</html>