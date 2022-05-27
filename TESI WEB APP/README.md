# struttura progetto

## template
Templates or views, is the part that handles the presentation logic. In a web application, this part is usually an HTML template file, which is set by the controller. The function of view block is to the user. Section views does not have direct access to the model section.

## model
Model usually dealing directly with databases to manipulate data (insert, update, delete, search), handle validation from controller parts, but it can’t deal directly with the view section.

## controller
Controller is a part that regulates the relationship between the part of the model and the part of view, the functions controller of is to receive requests and data from the user then determine what the application will process. 

## static
Static is for saving files css, javascript, and also to save images. 

## config
Config is part of managing database configuration and other system configurations. 

---

`__init__.py`  is a constructor file that will read python files that are in the config folder
`server.py` which functions to run the server, create a controller and make a model. 