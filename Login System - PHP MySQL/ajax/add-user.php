<?php
    define("__ACCESSIBLE__", true);
    require_once("../inc/config.php");
    
    if ($_SERVER["REQUEST_METHOD"] !== "POST") {
        header('Location:../index.php');
        exit();
    }

    $return = [];

    $username = preg_replace("/[^a-zA-Z0-9]/", "", $_POST["username"]);
    $password = password_hash($_POST["password"], PASSWORD_DEFAULT);

    if ($username !== $_POST["username"]) {
        $return["error"] = "Your username should only contain letters or numbers.";
    } else if (!Users::addUser($username, $password)) {
        $return["error"] = "That username is already taken.";
    } else {
        $_SESSION["user_id"] = Users::getUserByUsername($_POST["username"])["user_id"];
    }

    echo json_encode($return);
?>