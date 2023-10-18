<?php 
function db(){
    $servername = "localhost";
    $username = "root";
    $password = "HolyDance";
    $dbname = "donyasaaz";

    // Create connection
    $conn = new mysqli($servername, $username, $password, $dbname);
    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    return $conn;
}