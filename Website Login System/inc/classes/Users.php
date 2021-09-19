<?php
    if (!defined("__ACCESSIBLE__")) {
        header('Location: ../../index.php');
        exit();
    }

    class Users {
        
        protected static $con;

        private function __construct() {
            try {
                self::$con = new PDO("mysql:host=localhost;dbname=mydb", "root", "");
                self::$con->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
            } catch (PDOException $e) {
                echo "Could not connect to database." . $e->getMessage();  
                exit(); 
            }
        }

        public static function getConnection() {
            if (!self::$con) {
                new Users();
            }
            return self::$con;
        }

        public static function getUserByUsername($username) {
            if (!self::$con) {
                new Users();
            }

            $user = self::$con->prepare("SELECT * FROM users WHERE username = :username LIMIT 1");
            $user->bindParam(":username", $username);
            $user->execute();
            return $user->fetch(PDO::FETCH_ASSOC);
        }

        public static function getUserByID($id) {
            if (!self::$con) {
                new Users();
            }

            $user = self::$con->prepare("SELECT * FROM users WHERE user_id = :user_id LIMIT 1");
            $user->bindParam(":user_id", $id);
            $user->execute();
            return $user->fetch(PDO::FETCH_ASSOC);
        }

        public static function addUser($username, $password) {
            if (!self::$con) {
                new Users();
            }

            if (self::getUserByUsername($username) != false) {
                return false;
            } else {
                $date = date("Y-m-d H:i:s"); // YYYY-MM-DD HH:MM:SS
                $add = self::$con->prepare("INSERT INTO users(username, password, creation_date) 
                                            VALUES(:username, :password, :creation_date)");
                $add->bindParam(":username", $username);
                $add->bindParam(":password", $password);
                $add->bindParam(":creation_date", $date);
                $add->execute();
                return true;
            }
        }
    }
?>