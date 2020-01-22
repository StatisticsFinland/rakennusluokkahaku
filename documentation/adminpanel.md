# A quick guide to the admin panel

### The tables

The tables used on each page are sortable, searchable and pageable. This means that the tables can be sorted by each attribute. The search on the other hand will allow you to search for any term/string in the table.


### Question Groups

The question groups tab lets you add new group questions and edit existing ones. At the top of the view you'll find a dropdown form that adds a new group question. The new group requires a key (preferrably an integer but strings work as well), name, and a question in the three supported languages.

Below the edit form is the list of all existing groups. Every group attribute can be edited simply by clicking on it.

### Sessions

The sessions tab has a few functionalities:
You can view the selected class of each session, and view the question-answer chain that the user has clicked.
There is a slider-checkbox that allows you to filter out all sessions that do not have a selected class - eg a null value on the foreign key table reference.
There is also a "Hidden" feature, which allows for modifying the sql statement to take into acount the minimum amount of answers required to be visible.
This can be accessed by <url of backend>/801fc3r __?min=15__ (without a space)
Or by navigating to the sessions view by clicking the "Sessions" tab, and then manually typing ?min=(insert minimum value) into the URL bar.

By clicking on any of the fields of a session, you are greeted by a different view, where you can then see what attributes got what answer, and at what timestamp.

### Attributes

From the attributes tab you can view all the existing attributes, and group attributes with the existing grouping ID's. It is possible to edit all the fields of an attribute, and toggling wether or not you want an attribute to be active (and used in calculations etc.). You can also attach an attribute to any of the existing groups, which can be viewed from a dropdown menu.
It is possible as well to add new attributes through the view, but take extra care with the attribute name, question string and tooltip info fields (They are somewhat precise on syntax - but keep in mind you can easily edit the fields later without risk of breaking anything!)

### Building Classes

Like in the other tabs here you can create a new Building Class from the form at the top of the page. Though it's important to note that any added class needs to exist in the Statistics Finland API.
The table functions very similarly to the others, except for the "Class name" column. Clicking on a class name will reveal a new table with the attributes that the specific class has. From this table new attributes can be added to the class in question as well as their custom probabilities for the class in question.