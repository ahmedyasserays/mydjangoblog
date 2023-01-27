# My Django Blog
This is a project that i'm creating while reading Django 4 by example book by Antonio Melé

This is a simple blog project but i'll be listing new concepts that I learn here

1. The difference between db_index=True and models.Index
2. when i was reading the second chapter i noticed the {{ post.get_absolute_url }} and i knew previously that we can call a method on a template without the parentheses so i tried to add a parameter to a function then i found that this will not work and this if the function of a template tag of a template filter so i had a detailed look the the built in template tags and filters and found these new ones that I thought they may be very useful but i didn't know them before

    1. {% cycle 'row1' 'row2' %}
    2. {% firstof var1 var2 var3 %}
    3. interesting attribues in for loop
        1. {% for obj in list reversed %}
        2. forloop.counter  
        3. forloop.counter0  
        4. forloop.revcounter  
        5. forloop.revcounter0  
        6. forloop.first  
        7. forloop.last  
        8. forloop.parentloop


    4. {% ifchanged %} this is used in a loop and will render the content only if it was changed than the loop before or it can depend on a variable and only renders content if this variable was changed from the previous loop

    5. the {% regroup %} is a complicated tag that i saw before but i didn't completely understood it but now i got it. it just groups items with a grouper :)

    6. |floatformat this can be usefull when are working with mony or big numbers 

    7. json_script Safely outputs a Python object as JSON, wrapped in a script tag, ready for use with JavaScript.

    8. |slice this slices an iterable

3. paginator exceptions that are raised when we ask for page that doesn't exist or non integer
4. If your form data does not validate, cleaned_data will contain only the valid fields.
5. novalidate html attribute can be usefull while testing backend validations
5. http required decorators: require_GET, require_POST and also there is a condition decarator that can be used to return 304
6. calling .count method in template tag multiple time can be optimized using the {% with %} template tag
