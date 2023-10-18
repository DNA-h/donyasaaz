<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>فرم ثبت محصول</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.4/jquery.min.js"></script>

</head>
<body dir="rtl">
    <div class="container">
        <div class="row">
            <div class="col-12">
                <h2>فرم  ثبت</h2>

                <form class="mt-2 p-4 border border-1 rounded form" method="post" action="<?php echo htmlspecialchars($_SERVER['PHP_SELF']); ?>">
                    <div class="form-group">
                        <label class="mt-2 fw-bold form-label" for="product_name">نام اصلی محصول</label>
                        <input class="form-control" type="text" name="product_name" id="product_name" required />
                    </div>
                    <p class="status-product">وضعیت : <b class="data"></b></p>
                    <div class="form-group">
                        <label class="mt-2 fw-bold form-label" for="product_link">لینک محصول در دنیای ساز</label>
                        <input class="form-control" type="text" name="product_link" id="product_link" required />
                    </div>
                    


                    <div class="form-group">
                        <label class="mt-2 fw-bold form-label" for="product_image">لینک عکس محصول در دنیای ساز</label>
                        <input class="form-control" type="text" name="product_image" id="product_image" required />
                    </div>
                    



                    <div class="form-group">
                        <label class="mt-2 fw-bold form-label" for="other_links">لینک در سایت های دیگر</label>
                        <p><b>هر لینک در یک خط با enter جدا کنید</b></p>
                        <textarea class="form-control"  name="other_links" id="other_links" required></textarea>
                    </div>

                    

                    <div class="form-group">
                        <label class="mt-2 fw-bold form-label" for="password">رمز عبور</label>
                        <input class="form-control" type="password" id="password" name="password" required />
                    </div>
                    
                    <button class="btn btn-primary btn-rounded mt-3" type="submit">ثبت</button>
                </form>
            </div>
        </div>
    </div>
    

</body>
</html>
<script>
    jQuery(document).ready(function($){
        jQuery("#product_name").keyup(function($){
            var title = jQuery(this).val();
            jQuery(".status-product .data").text("درحال لود ...");
            jQuery.post("ajax.php",
            {
                title: title,
            },
            function(data, status){
                jQuery(".status-product .data").text(data);
            });
        })
    });
</script>

<?php
require_once('db.php');
if( $_POST && isset($_POST['product_name'])){

    if($_POST['password'] == "yahoo"){

        $product_name = trim($_POST['product_name']);
        $product_link = trim($_POST['product_link']);
        $product_image = trim($_POST['product_image']);
        $other_links = trim($_POST['other_links']);
        
        if(!empty($product_name) && !empty($product_link) &&!empty($product_image) &&!empty($other_links) ){
            
            $links_count = explode("\n",$other_links);
            $pure_links = [];
            foreach ( $links_count as $link){
                if(trim($link) != "" && strpos($link,"http") === 0){
                    $pure_links[] = trim($link);
                }
            }
            $conn = db();

            if(sizeof($pure_links)> 0){
                $sql = "INSERT INTO models_musicitem (created, modified, name , url , image , is_active , price)
                VALUES (now(), now() , '$product_name', '$product_link' , '$product_image' , 1 , -1)";
    
                if ($conn->query($sql) === TRUE) {
    
                    $last_id = $conn->insert_id;
                    echo "New record created successfully.<br>";

                    foreach($pure_links as $pure){
                        $sql2 = "INSERT INTO models_link (created, modified, url , unseen , parent_id , is_active , reported , importance , is_bookmark)
                        VALUES (now(), now() , '$pure', 0 , $last_id , 1 , 0 , 100 , 0 )";

                        $conn->query($sql2);

                        echo "New Link created successfully.<br>";
                    }
                   
    
    
                   
    
                } else {
                    echo "Error: " . $sql . "<br>" . $conn->error;
                }

            }else{
                echo "<h2>لینک بقیه سایتا رو نزدی</h2>";
            }
            
            $conn->close();
        }
    }else{
        echo "<h2>پسورد اشتباهه</h2>";
    }

}

