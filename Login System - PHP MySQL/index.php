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
        <title>Home - My website</title>
    </head>
    <body>
        <?php require_once("inc/navbar.php"); ?>

        <div class="welcome-text">
            <div>
                <?php
                    if (isset($_SESSION["user_id"])) {
                        $user = Users::getUserByID($_SESSION["user_id"]);
                        $username = $user["username"];
                        
                        $creationDate = $user["creation_date"];
                        $dateObject = date_create($creationDate);
                        $date = date_format($dateObject, "M j, Y");
                        $time = date_format($dateObject, "H:i:s");

                        echo "You are logged in as <span>$username</span>. ";
                        echo "Your account was created on <span>$date at $time ";
                        echo date_default_timezone_get() . "</span>.";
                    } else {
                        echo "Welcome to my website.";
                    }
                ?>
            </div>
        </div>

    </body>
</html>