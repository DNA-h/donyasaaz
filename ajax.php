<?php
require_once('db.php');
$conn = db();
$title = trim($_POST['title']);
$sql = "SELECT * FROM `models_musicitem` where `name` LIKE '$title'";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
  echo "تکراری";
} else {
  echo "بدون تکرار";
}
die();