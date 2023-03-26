# A Blogpost project made by Django

## Resume
- Class-based view
- Widget and field look-up
- Django ORM
- Form model

## Step
- Generate project named **'blogsite'** and create django's app named **'blog'**
- Create urls for 'blog', inject it to base urls
- Initialize models for blog such as **Post** and **Comment** with its fields and methods (first design what it looks like - attribut's fields, methods,...)
- Initialize model form in **forms.py** as app level, which are **PostForm** and **CommentForm**, associated with **Post** and **Comment** models, we can decorate its form's field by define a **widgets** attribut inside the **Meta** class
- Define views for **Post** and **Comment**:
    - with **Post**'s views: Design it by using class-based view, we have several different **Post**'s views: CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView
    - with **Comment**'s views: Design it by using function view as usual, but use **login_required** decorator to check the authentication
- Define **templates** and **static** directories as app level (not as project level) with some html pages