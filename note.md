Employ user authentication in React with Django REST Framework
------

# Django tips
+ Numeric for Django Template
```
{% for i in "x"|rjust:"10" %}
    <option value="{{ forloop.counter }}">{{ forloop.counter }}</option>		
{% endfor %}
```

+ Error_messages in template:
```
{% if messages %}
{% for message in messages %}
    <div class="alert {% if message.tags %} alert-{{ message.tags }}{% endif %}">{{ message|safe }}</div>
{% endfor %}
{% endif %}
```
or put error_message in paramters and show it in the template:
```
{% if error_message %}
    <p><strong>{{ error_message }}</strong></p>
{% endif %}
```

+ Add login form at navbar:
```
<form class="navbar-form navbar-right" role="form" action="{% url 'mysite_login' %}"
    method="post" accept-charset="utf-8">
  <div class="form-group">
    <input type="text" placeholder="Username" class="form-control" name="username">
  </div>
  <div class="form-group">
    <input type="password" placeholder="Password" class="form-control" name="password">
  </div>
  {% csrf_token %}
  <button type="submit" class="btn btn-success">Sign in</button>
</form>
```

+ Collapsive panel:
```
{% for key, values in esm_dict.items %}
    <div class="panel panel-default">
        <div class="panel-heading panel-heading-esm{{ key }}" role="tab" id="headingEsm{{ key }}">
            <h4 class="panel-title">
            <span class="collapsed" role="button" data-toggle="collapse" data-parent="#accordion" href="#collapse{{ key }}" aria-expanded="false" aria-controls="collapseTwo">
                {{ values }}
                </span>
            </h4>
        </div>
        <div class="panel-body">
            <div id="collapse{{ key }}" class="panel-collapse collapse" role="tabpanel" aria-labelledby="heading{{ key }}">
                <div class="text-center">
                    <img src="{% static 'ecocases/esms/esm'|concat_string:key|concat_string:'.png' %}" class="img-rounded esm_img" alt="">
                </div>
                <button class="btn btn-info pull-right"><a href="{% static 'ecocases/esms/esm'|concat_string:key|concat_string:'.pdf' %}">Download PDF</a></button>
            </div>
        </div>
    </div>
{% endfor %}
```