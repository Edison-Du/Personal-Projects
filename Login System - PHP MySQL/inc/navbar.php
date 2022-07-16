<?php
    if (!defined("__ACCESSIBLE__")) {
        header('Location: ../index.php');
        exit();
    }
    
    if (isset($_SESSION["user_id"])) {
        echo "
            <div class=\"navbar\">
                <a href=\"index.php\">Home</a>
                <a href=\"logout.php\">Logout</a>
            </div>
        ";
    } else {
        echo "
            <div class=\"navbar\">
                <a href=\"index.php\">Home</a>
                <a href=\"login.php\">Login</a>
            </div>
        ";
    }
?>