<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>چک کردن محصولات</title>
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
                        <label class="mt-2 fw-bold form-label" for="product_name">نام محصول</label>
                        <input class="form-control" type="text" name="product_name" id="product_name" required />
                    </div>
                    

                    <div class="form-group">
                        <label class="mt-2 fw-bold form-label" for="password">پسورد</label>
                        <input class="form-control" type="text" name="password" id="password" required />
                    </div>
                    
                    <button class="btn btn-primary btn-rounded mt-3" type="submit">ثبت</button>
                </form>
            </div>
        </div>
    </div>
    

</body>
</html>
<!-- <script>
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
</script> -->

<?php
require_once('db.php');
if( $_POST && isset($_POST['product_name'])){

    if($_POST['password'] == "google"){

        $product_name = trim($_POST['product_name']);
                
        if(!empty($product_name)){
            
           
            $conn = db();
            $text = $product_name;
            $sql = "SELECT * FROM models_musicitem WHERE `name` LIKE '%$text%' ";
            

            $result = $conn->query($sql);

            if ($result->num_rows > 0) {
                // output data of each row
                while($row = $result->fetch_assoc()) {
                    echo "<div class='row'>"."<h1>".$row['name']."</h1>"."</div>";
                    $sql2 = "SELECT * FROM models_link WHERE `parent_id` = ".$row['id']." ";
                    $result2 = $conn->query($sql2);
                    if ($result2->num_rows > 0) {
                        echo "<ul>";
                        while($row2 = $result2->fetch_assoc()) {
                            echo "<li>"."<a href='".$row2['url']."' target='_blank'>".$row2['url']."</a>"."</li>";
                        }
                        echo "</ul>";
                    }else{
                        echo "زیر مجموعه ندارد.";
                    }
                }
            } else {
                echo "پیدا نشد!";
            }
           
           
            
            $conn->close();
        }
    }else{
        echo "<h2>پسورد اشتباهه</h2>";
    }

}

