from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField

from pages.helpers import random_code_generator

###
# Models for the user all platform users
# These users include admins, trainers and trainees
###
User = get_user_model()

class BaseUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(blank=True)

class Admin(BaseUser):
    """
    Represents an admin user in the system.

    Attributes:
        BaseUser: The base class for the Admin class.

    Methods:
        __str__: Returns a string representation of the admin user.

    Returns:
        str: The string representation of the admin user.

    Example:
        ```python
        admin = Admin()
        admin.user = user
        print(admin)
        # Output: "John Doe admin"
        ```
    """
    ...
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} admin"

class Trainer(BaseUser):
    """
    Represents a trainer user in the system.

    Attributes:
        BaseUser: The base class for the Trainer class.

    Methods:
        __str__: Returns a string representation of the trainer user.

    Returns:
        str: The string representation of the trainer user.

    Example:
        ```python
        trainer = Trainer()
        trainer.user = user
        print(trainer)
        # Output: "John Doe trainer"
        ```
    """
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} trainer"

class Trainee(BaseUser):
    """
    Represents a trainee user in the system.

    Attributes:
        BaseUser: The base class for the Trainee class.

    Methods:
        __str__: Returns a string representation of the trainee user.

    Returns:
        str: The string representation of the trainee user.

    Example:
        ```python
        trainee = Trainee()
        trainee.user = user
        print(trainee)
        # Output: "John Doe trainee"
        ```
    """
    business_name = models.CharField(max_length=300)
    cohort = models.ForeignKey('pages.Cohort',
                                on_delete=models.SET_NULL,
                                null=True, blank=True)
    notes = models.TextField()
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} trainee"
    
###
# Models for Cohorts and Topics
###
class Cohort(models.Model):
    """
    Represents a training cohort in the system.

    Args:
        models.Model: The base class for the Cohort model.

    Attributes:
        name (CharField): The name of the cohort.
        start_date (DateField): The start date of the cohort.
        end_date (DateField): The end date of the cohort.
        description (TextField): The description of the cohort.
        trainers (ManyToManyField): The trainers associated with the cohort.

    Example:
        ```python
        cohort = Cohort()
        cohort.title = "Python Fundamentals"
        cohort.start_date = date(2022, 1, 1)
        cohort.end_date = date(2022, 1, 31)
        cohort.description = "A comprehensive course on Python programming."
        cohort.trainers.add(trainer1, trainer2)
        cohort.save()
        ```
    """
    COUNTRIES = (
        (0, 'Uganda'),
        (1, 'Kenya'),
        (2, 'Jamaica')
    )
    
    title = models.CharField(max_length=300)
    country = models.SmallIntegerField(choices=COUNTRIES, default=0)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    code = models.CharField(max_length=10, default=random_code_generator, unique=True)
    trainers = models.ManyToManyField(Trainer, 
                                      related_name='cohort_trainers',
                                      blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        _country = [country[1] for country in self.COUNTRIES if\
            self.country == country[0]]
        try:
            return f"{self.title} ({_country[0]})"
        except:
            return self.title
    
    
class Topic(models.Model):
    """The Topic class uses the Django models.Model class as a base class. It defines the following fields:

    name: A character field to store the name of the topic.
    
    description: A text field to store the description of the topic.
    
    created_by: A foreign key field to associate the topic with the user who created it.
    
    trainers: A many-to-many field to associate the topic with multiple trainers.
    
    cohort: A foreign key field to associate the topic with a cohort.
    
    Coupling and Cohesion
    The Topic model has a high cohesion as it represents a single concept of a topic in a learning cohort.
    The created_by field has a coupling with the User model through the foreign key relationship.
    The trainers field has a coupling with the Trainer model through the many-to-many relationship.
    The cohort field has a coupling with the Cohort model through the foreign key relationship.
    Single Responsibility Principle
    The code follows the Single Responsibility Principle as it defines the fields and relationships for the Topic model, which is its primary responsibility.
    There are no pieces that need to be extracted into a separate function as the code is defining the model structure.
    Unusual Things
    The trainers field has null=True and blank=True attributes, allowing it to be optional.
    The cohort field has null=True and blank=True attributes, allowing it to be optional.
    """
    name = models.CharField(max_length=300)
    description = models.TextField()
    created_by = models.ForeignKey(User, null=True, related_name='topic_author',
                                   on_delete=models.SET_NULL)
    trainers = models.ManyToManyField(Trainer, 
                                      related_name='prog_trainers',
                                      blank=True)
    cohort = models.ForeignKey(Cohort,
                                on_delete=models.SET_NULL,
                                null=True, blank=True)
    
    def __str__(self):
        return f"{self.name}"


class Messages(models.Model):
    """
    Represents a message in the system.

    Attributes:
        topic (ForeignKey): The topic associated with the message.
        title (CharField): The title of the message.
        message (TextField): The content of the message.
        sender (ForeignKey): The user who sent the message.
        datetime (DateTimeField): The date and time when the message was sent.

    Example:
        ```python
        message = Messages()
        message.topic = topic
        message.title = "Important Announcement"
        message.message = "Please be informed that the meeting has been rescheduled."
        message.sender = user
        message.datetime = datetime.now()
        message.save()
        ```
    """
    topic = models.ForeignKey(Topic, related_name='message_topic',
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    message = models.TextField()
    sender = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    date_time = models.DateTimeField()
    
class Bot(models.Model):
    STATUS = (
        (0, 'Inactive'),
        (1, 'Active')
    )
    name = models.CharField(max_length=300)
    description = models.TextField()
    status = models.SmallIntegerField(choices=STATUS, default=0)
    cohort = models.ForeignKey(Cohort,
                                on_delete=models.SET_NULL,
                                null=True, blank=True)
    bot_code = models.CharField(max_length=10, default=random_code_generator, unique=True)
    
    def __str__(self):
        return self.name
    
class Content(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
    content_order = models.IntegerField()
    bot_response = models.TextField()
    bot_question = models.TextField()
    

class UserNote(models.Model):
    name = models.CharField(max_length=300, default='user note')
    phone = models.CharField(max_length=300, null=True)
    notes = models.CharField(max_length=300, null=True)
    notes_type = models.CharField(max_length=300, null=True)
    time_created = models.CharField(max_length=300, null=True)
    
    class Meta:
        managed = False
  

class UserReminders(models.Model):
    name = models.CharField(max_length=300, default='user reminders')
