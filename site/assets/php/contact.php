<?php

if (isset($_POST['submit'])) {
    $name = $_POST['name'];
    $mailFrom = $_POST['email'];
    $message = $_POST['message'];

    $mailTo = "contact@coopster.co.uk";
    $headers = "From: ".$mailFrom;
    $txt = "E-mail from ".$name.".\n\n".$message;

    mail($mailTo, "Contact on Coopster.co.uk", $txt, $headers);
    header("Location: ../../index.html");
}