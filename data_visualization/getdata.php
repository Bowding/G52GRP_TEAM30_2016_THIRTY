<?php
    //connect to database to obtain info
    $servername = "localhost";
    $username = "root";
    $password = "123456";

    // Create connection
    $db = mysqli_connect($servername, $username);
      
    // Check connection
    if (!$db) {
      die("Connection failed: " . mysqli_connect_error()) . " <br/>";
    }
    else
    {
        echo "Connect to DB successfully!";
    }

    
    $links = "{source: \"Mickco\", target: \"Henry\", image: \"https://scholar.google.com/citations?view_op=view_photo&user=G0yAJAwAAAAJ&citpid=1\"},
    {source: \"Mickco\", target: \"Harry\", image: \"http://combiboilersleeds.com/images/person/person-8.jpg\"},
    {source: \"Henry\", target: \"Aiden\", image: \"http://combiboilersleeds.com/images/person/person-8.jpg\"},
    {source: \"Charlie\", target: \"Curry\", image: \"https://scholar.google.com/citations?view_op=view_photo&user=G0yAJAwAAAAJ&citpid=1\"},
    {source: \"Aiden\", target: \"Alex\", image: \"http://combiboilersleeds.com/images/person/person-8.jpg\"},
    {source: \"Mickco\", target: \"Charlie\", image: \"http://combiboilersleeds.com/images/person/person-8.jpg\"},
    {source: \"Mickco\", target: \"Curry\", image: \"http://combiboilersleeds.com/images/person/person-8.jpg\"},
    {source: \"Curry\", target: \"Jack\", image: \"http://combiboilersleeds.com/images/person/person-8.jpg\"},
    {source: \"Jack\", target: \"Alex\", image: \"http://combiboilersleeds.com/images/person/person-8.jpg\"},
    {source: \"Alex\", target: \"Aiden\", image: \"http://combiboilersleeds.com/images/person/person-8.jpg\"},
    {source: \"Harry\", target: \"Henry\", image: \"http://combiboilersleeds.com/images/person/person-8.jpg\"}";


    mysqli_close($db);  
    
    include "nodes_test2.html";

        
?>