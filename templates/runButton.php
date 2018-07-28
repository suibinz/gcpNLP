<?php
if ($_GET['run']) {
  # This code will run if ?run=true is set.
  exec("python3 getSentiment.py");
}
?>
