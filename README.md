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
7. django-taggit package
8. django taggit are using a weird text input field that is accepting any string and getting or creating values based on the comma separatd values, this can be done if you override the clean method of the char fiel
9. we can import from a parent module using ..
10. in creating custom tags, you will use the name of the file you created to import the template tags
11. new template tag type (inclusion_tag)
12. storing template tags return value in a variable that you can use later with with
13. in the sitemap class you can have a lastmod method that can update each object with the update time for example
14. what are RSS or Atom feeds and how to add them to my site
15. you can import any built in tempalte filter from django.template.defaultfilters and use it as a normal function, the same applies to defaulttags from django.template.defaulttags
16. you can pass --output to dumpdata instead of >>, also you can use --indent=2 for example to pretify or -Xutf8 for encoding
17. Stemming is the process of reducing words to their word stem, base, or root form.
18. triagram similarity is an algorithm for finding how many three characters repeated in the same word and used in search
