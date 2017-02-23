import bottle

@bottle.route('/')
def login():
    return ''' <!DOCTYPE html>
                    <html>
                    <head>
                    <link rel = "stylesheet" type = "text/css" href = "index.css">
                    <title>Data Mining</title>
                    <style>
                    input[type = text]{
                        
                    }
                    </style>
                    </head>
                    <body>
                    <div class = "logo">
                    <img id = "logo" src = "logo.png" alt = "Logo" width = "350" height = "250">
                    </div>
                    <div class = "anchor">
                        <table>
                            <tr>
                                <th>
                                    <div class="dropdown">
                                        <button onclick="myFunction()" class="dropbtn">Dropdown</button>
                                        <div id="myDropdown" class="dropdown-content">
                                            <a href="#home">Home</a>
                                            <a href="#about">About</a>
                                            <a href="#contact">Contact</a>
                                        </div>
                                    </div>
                                </th>
                                <th>
                                    <div class = "search">
                                        <form name = "form" action = "/test" method = "POST">
                                            <input type = "text" name = "search" placeholder = "Search..">
                                            <input name = "searchbutton" type = "submit"/>
                                        </form>
                                    </div>
                                </th>
                            </tr>
                        </table>
                    </div>

                    <script>
                    /* When the user clicks on the button, 
                    toggle between hiding and showing the dropdown content */
                    function myFunction() {
                        document.getElementById("myDropdown").classList.toggle("show");
                    }

                    // Close the dropdown if the user clicks outside of it
                    window.onclick = function(event) {
                      if (!event.target.matches('.dropbtn')) {

                        var dropdowns = document.getElementsByClassName("dropdown-content");
                        var i;
                        for (i = 0; i < dropdowns.length; i++) {
                          var openDropdown = dropdowns[i];
                          if (openDropdown.classList.contains('show')) {
                            openDropdown.classList.remove('show');
                          }
                        }
                      }
                    }
                    </script>

                    </body>
                    </html>
            '''

@bottle.route('/test', method="POST")
def formhandler():
    """Handle the form submission"""
    
    search = bottle.request.forms.get('search')
    
    message = "Hello " + search + "."
    
    return "<p>" + message + "</p>"

bottle.run(host='localhost', port=8080)