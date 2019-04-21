# Need Your Help (backend)

> Provides the api for the "need your help" survey website.

## End-points
- `auth/register/` user registration
- `auth/login/` user login
- `auth/logout/` user logout 
- `topics/` list or create topics
- `topics/<int:topic_id>/` retrieve, update or delete topic
- `topics/<int:topic_id>/questions/` lest or create questions
- `topics/<int:topic_id>/questions` 

Topic -> Survey -> Interviewee -> Responses
Topic -> TextAnswerableQuestion

topics/<int:topic_id>/questions/<int:question_id>/respond/
topics/<int:topic_id>/surveys/

{"first_name": "Denniel", "last_name": "Sadian", "text": "Yes, I like it."}
{"first_name": "Bon Bon", "last_name": "Sadian", "text": "Yes, I like it."}
{"first_name": "Bon Bon", "last_name": "Sadian"}
{"first_name": "Denniel Luis", "last_name": "Sadian", "text": ""}

Topic.objects.all()[0].multiplechoice_set.all()[0].choices.all()[0].count
Topic -> MultipleChoice -> Choice

topics/<int:topic_id>/multiplechoice/
topics/<int:topic_id>/multiplechoice/<int:id>/choices/
topics/<int:topic_id>/multiplechoice/<int:qid>/choices/<int:pk>/choose/


- Create two users:
    - Bon Bon and Denniel

- No one should be able to create topics, questions
  and choices if they're not autheticated.

- Bon Bon creates Online Learning topic.
    - Bon Bon creates two questions:
        - How does it help you?
        - What are its goods?
    - Bon Bon creates two multiple choices:
        - Where do you learn? -> multiple
            - YouTube
            - W3Schools
            - Sololearn
        - Is it good for learners?
            - Yes
            - No
- Bon Bon must be able to edit all things he created.
- Denniel, however, won't be.

- Denniel creates Web Development topic.
    - Denniel creates two questions:
        - Do you do web developemt?
        - Do you like it? Why?
        - What are the hindrances that you face?
    - Denniel creates two multiple choices:
        - Which one is better for backend?
            - Django
            - Flask
        - What front-end framework(s) do you use? -> multiple 
            - Vue
            - Angular
            - React
- Denniel must be able to edit all things he created.
- Bon Bon, however, won't be.

/topic/<int:topic_id>/result/