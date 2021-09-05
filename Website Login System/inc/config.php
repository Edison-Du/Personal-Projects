<?php
    if (!defined("__ACCESSIBLE__")) {
        header('Location: index.php');
        exit();
    }

    if (!isset($_SESSION)) {
        session_start();
    }
	
    error_reporting(-1);
	ini_set('display_errors', 'On');

    include_once("classes/Users.php");
?>