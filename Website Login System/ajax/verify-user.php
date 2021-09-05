<?php
    define("__ACCESSIBLE__", true);
    require_once("../inc/config.php");
    
    if ($_SERVER["REQUEST_METHOD"] !== "POST") {
        header('Location:../index.php');
        exit();
    }

    $return = [];

    $user = Users::getUserByUsername($_POST["username"]);

    if ($user) {
        if (password_verify($_POST["password"], $user["password"])) {
            $_SESSION["user_id"] = $user["user_id"];
        } else {
            $return["error"] = "Invalid credentials";
        }
    } else {
        $return["error"] = "Invalid credentials";
    }

    echo json_encode($return);
?>