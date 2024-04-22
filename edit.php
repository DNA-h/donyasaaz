<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>فرم ویرایش محصول</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.4/jquery.min.js"></script>

</head>
<?php 
require_once('db.php');
?>
<body dir="rtl">
    <div class="container">
        <div class="row">
            <div class="col-12">
                <?php 

                if(isset($_GET['id'])){
                    $product_id = intval(htmlspecialchars($_GET['id']));
                    $conn = db();
                    
    
                    $sql = "SELECT * FROM models_musicitem WHERE `id` =  $product_id ";
                    $result = $conn->query($sql);
                    $product_name = "";
                    $found = false;
                    $list_data = ""; 
                    if ($result->num_rows > 0) {
                        $found = true;
                        while($row = $result->fetch_assoc()) {
                            $product_name = $row['name'];
                            $sql2 = "SELECT * FROM models_link WHERE `parent_id` = ".$row['id']." ";
                            $result2 = $conn->query($sql2);
                            if ($result2->num_rows > 0) {
                                while($row2 = $result2->fetch_assoc()) {
                                    $list_data .= $row2['url'] ."\n";  
                                }
                            }
                        }
                    }
    
                    if($found){
                        ?>
                        <h2>فرم ویرایش <?= $product_name; ?></h2>
                        
                        <form class="mt-2 p-4 border border-1 rounded form" method="post" action="<?php echo htmlspecialchars($_SERVER['PHP_SELF']); ?>">
                            <input type="hidden" name="product_id" value="<?= $product_id;?>"/> 
                            <div class="form-group">
                                <label class="mt-2 fw-bold form-label" for="other_links">لینک در سایت های دیگر</label>
                                <p><b>هر لینک در یک خط با enter جدا کنید</b></p>
                                <textarea class="form-control"  name="other_links" id="other_links" rows="25"  required><?= $list_data ?></textarea>
                            </div>
    
                            
    
                            <div class="form-group">
                                <label class="mt-2 fw-bold form-label" for="password">رمز عبور</label>
                                <input class="form-control" type="password" id="password" name="password" required />
                            </div>
                            
                            <button class="btn btn-primary btn-rounded mt-3" type="submit">ثبت</button>
                        </form>
                        <?php
                    }else{
                        echo "محصول موجود نیست ! ";
                    }
                }else{

                }
                
                ?>
                
            </div>
        </div>
    </div>
    
    <?php

if( $_POST && isset($_POST['product_id'])){

    if($_POST['password'] == "saberi"){

        $product_id = trim($_POST['product_id']);
        $other_links = trim($_POST['other_links']);
        
        if(!empty($product_id) && !empty($other_links) ){
            
            $links_count = explode("\n",$other_links);
            $pure_links = [];
            foreach ( $links_count as $link){
                if(trim($link) != "" && strpos($link,"http") === 0){
                    $pure_links[] = trim($link);
                }
            }
            $conn = db();

            if(sizeof($pure_links)> 0){

                foreach($pure_links as $pure){
                    $query = "SELECT COUNT(*) AS count FROM models_link WHERE url = '$pure'";
    
                    if ($result = $conn->query($query)) {
                        // Fetch the result
                        $row = $result->fetch_assoc();
                        if ($row['count'] > 0) {
                             /// ALREADY EXISTS
                        } else {
                            $sql2 = "INSERT INTO models_link (created, modified, url , unseen , parent_id , is_active , reported , importance , is_bookmark)
                            VALUES (now(), now() , '$pure', 0 , $product_id , 1 , 0 , 100 , 0 )";
        
                            $conn->query($sql2);
        
                            echo "New Link created successfully.<br>";
                        }
                    }else{

                    }
                    
                }
                echo "<h1>ثبت موفق بود</h1>";
                echo "<p><a href='check.php'>بازگشت به لیست</a></p>";
            }else{
                echo "<h2>لینک بقیه سایتا رو نزدی</h2>";
            }
            
            $conn->close();
        }else{

        }
    }else{
        echo "<h2>پسورد اشتباهه</h2>";
    }

}
?>
</body>
</html>

