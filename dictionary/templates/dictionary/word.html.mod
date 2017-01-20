
{% extends "baselayout.html" %}

{% block pagetitle %}{{ settings_site_title }} - Sign for {{ translation.translation }} {% endblock %}


{% block jqueryready %}


{% endblock %}

{% block script %}
    function replay() {
        $f('player').play();
    }
{% endblock %}

{% block content %}
<div id='publicsign' class="view-{{ viewname }}">
    {% if feedbackmessage %}
    <div id="feedbackmessage">
        <p class='alert alert-info'>
            {{ feedbackmessage }}
        <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button></p>
    </div>
    {% endif %}

    <div id="signinfo" class='navbar navbar-default navbar-collapse'>

        <div class='btn-group'>
            {% if SIGN_NAVIGATION %}

                {% if navigation.prev %}
                <a class='btn navbar-btn btn-default' href="{% url 'dictionary:gloss' navigation.prev.idgloss %}?lastmatch={{lastmatch}}">&laquo; <span class='hidden-xs'>Previous Sign</span></a>

                {% endif %}

                <button class='btn navbar-btn'>Sign {{glossposn}} of {{glosscount}} <span class='hidden-xs'>in the Auslan Dictionary</span></button>

                {% if navigation.next %}
                <a class="btn navbar-btn btn-default"
                   href="{% url 'dictionary:gloss' navigation.next.idgloss %}?lastmatch={{lastmatch}}"><span class='hidden-xs'>Next Sign</span> &raquo;</a>
                {% endif %}
             {% else %}

             {% endif %}
        </div>


        <div class='pull-right'>
            {% if viewname == "words" %}
            <span class='navbar-text'>Matches for the word <em>{{ translation.translation }}</em></span>
            <div class='btn-group'>
            {% for i in matches %}
                {% ifequal i n %}
                <button type='button' class='btn btn-primary navbar-btn'>{{i}}</button>
                {% else %}
                <a type='button' class='btn btn-default navbar-btn' href="{{translation.translation}}-{{i}}">{{i}}</a>
                {% endifequal %}
            {% endfor %}
            </div>
            {% else %}
                {% if lastmatch %}
                <a class='btn btn-default navbar-btn' href="{% url 'dictionary:word' lastmatch %}">Return to Matches</a>
                {% endif %}
            {% endif %}
        </div>


        <div class='btn-group'>
           {% if perms.dictionary.search_gloss %}
           <a id='editbutton' class='btn btn-default navbar-btn' href="{% url 'dictionary:admin_gloss_view' pk=gloss.id %}">Detail View</a>
           {% endif %}
        </div>

    </div>

    <div id="definitionblock">
        <div class='col-md-4 region-left'>
            {% comment %}
            <div id="videocontainer">
               <div id="player">
                  <iframe id='videoiframe' scrolling="no" frameborder='0' allowfullscreen="allowfullscreen"
                          src="{% url 'video.views.iframe' gloss.pk %}">
                  </iframe>
               </div>
               <div id="replay"></div>
            </div>
           {% endcomment %}

            <div id="keywords">
                 <p><strong>Keywords:</strong>
                 {% for kwd in allkwds %}
                   {% ifequal translation.translation kwd.translation %}<b>{{ kwd.translation }}</b>{% else %}{{ kwd.translation }}{% endifequal %}{% if not forloop.last %},{% endif %}
                 {% endfor %}
                 </p>
            </div>

            {% if viewname == "words" %}
            <div id="feedback">
                <ul>
                    {% ifequal viewname "words" %}
                    <li><a href="{% url 'feedback:wordfeedback' translation.translation n %}">Provide feedback about this sign</a></li>
                    {% else %}
                    <li><a href="{% url 'feedback:glossfeedback' gloss.pk %}">Provide feedback about this sign</a></li>
                    {% endifequal %}

                    <li><a href="{% url 'feedback:missingsign' %}">Report a missing sign</a></li>
                    <li><a href="{% url 'feedback:generalfeedback' %}">Provide general site feedback</a></li>
                </ul>
            </div>
            {% endif %}
        </div>


        {% if regional_template_content %}
        <div  class='col-md-12'>
          {{ regional_template_content }}
        </div>
        {% endif %}

        {% if DEFINITION_FIELDS and gloss.published_definitions %}
        <div  class='col-md-8'>
            <h2>Sign Definition</h2>

            {% for deftype in DEFINITION_FIELDS %}

                 {% regroup gloss.published_definitions by role as roles %}

                 {% for role in roles %}

                      {% ifequal deftype role.grouper %}

                          <h3>{{role.list.0.get_role_display}}</h3>

                          <ol>
                          {% for def in role.list %}
                            <li>{{def.text}}</li>
                          {% endfor %}
                          </ol>

                      {% endifequal %}
                 {% endfor %}
            {% endfor %}

        </div>
        {% endif %}

        {% if viewname == "words" %}
        <div class='col-md-3 region-right'>
            {% if regions|length > 0 %}
            <div id="states">
                <div>
                {% for image in dialect_image %}
                    <img src="{% static image %}" alt="Region">
                {% endfor %}
                </div>
            </div>

            <div>
                <h4>Sign Distribution</h4>
                <table class="table table-condensed">
                  {% for region in regions %}
                  <tr>
                    <td>
                      {{ region.dialect.name }}
                    </td>
                    <td>
                      {{ region.traditional|yesno:" traditional," }}
                    </td>
                    <td>
                        {{ region.frequency }}
                    </td>
                  </tr>
                  {% endfor %}
                </table>
            </div>
            {% endif %}
        </div>
        {% endif %}

    </div>

</div>

{% endblock %}
