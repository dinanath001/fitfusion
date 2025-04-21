from django.db import models
from django.utils import timezone
from django.utils.timezone import now
from django.core.exceptions import ValidationError

# Model for Events
class Gym(models.Model):
    gym_id = models.CharField(max_length=50, primary_key=True)  # Unique ID for the gym
    password = models.CharField(max_length=128)  # Storing password (consider hashing it)
    owner_name =models.CharField(max_length=100)
    gym_name = models.CharField(max_length=100, unique=True)
    gym_city = models.CharField(max_length=50)
    contact = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=150)
    opening_hours = models.CharField(max_length=100, default='6:00 AM - 10:00 PM')
    gym_image = models.ImageField(upload_to='gym/gym_images', blank=True, null=True)
    payment = models.BooleanField(default=False)


    def __str__(self):
        return self.gym_name 

class Event(models.Model):
    gym_id = models.CharField(max_length=50, default="")
    event_name = models.CharField(max_length=100) 
    event_venue = models.CharField(max_length=150)  
    event_date = models.DateField(default=timezone.now) 
    event_description = models.TextField() 
    event_image = models.ImageField(upload_to='gym/event_images', blank=True, null=True)

    def __str__(self):
        return f"{self.event_name} - {self.event_date}"
    
#for Admin    
class News(models.Model):
    news_title = models.CharField(max_length=100)
    news_description = models.TextField() 
    news_time = models.DateTimeField(default=timezone.now) 
    news_by = models.CharField(max_length=100, default="FitFusion Team")
    gym = models.ForeignKey('Gym', on_delete=models.SET_NULL, blank=True, null=True)  # Foreign key to Gym model  

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"

    def __str__(self):
        return f"{self.news_by} - {self.news_title[:30]}"   

# Model for ContactUs
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(default=now)  

    def __str__(self):
        return f"Message from {self.name} ({self.email})"  

# Custom Validator for Image Size (Max 10MB)
def validate_image_size(image):
    max_size = 10 * 1024 * 1024  # 10MB in bytes
    if image.size > max_size:
        raise ValidationError("Image size should not exceed 10MB.")      

class Trainer(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='trainers', null=True, blank=True)
    name = models.CharField(max_length=100)  # No need for "null" as default
    email = models.EmailField(max_length=100, unique=True)
    gender = models.CharField(max_length=10, choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")])
    city = models.CharField(max_length=50)
    specialization = models.CharField(max_length=50, default="General Fitness")
    experience = models.TextField()
    about_trainer = models.TextField(blank=True, null=True)
    trainer_pic = models.ImageField(upload_to="gym/trainers", null=True, blank=True, validators=[validate_image_size])

    def __str__(self):
        return f"{self.name} - {self.specialization}"    

# Model for Public Workout Videos
class Workout(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(help_text="Brief description of the workout")
    video = models.FileField(upload_to='gym/work_video', null=True, blank=True)

    def get_video_source(self):
        if self.video:
            return self.video.url
        return None

    def __str__(self):
        return self.title

# Model for Job Applicants
class ApplicantDetail(models.Model):
    gym_id = models.CharField(max_length=50 ,default="")
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    email = models.CharField(max_length=100)
    about_user = models.TextField(default="")
    user_cv = models.FileField(upload_to='gym/user_cv', blank=True, null=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name 

# Model for Nutrition Plans (No Gym ForeignKey)
class NutritionPlan(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE , null=True, blank=True)
    PLAN_TYPES = [
        ("weight_loss", "Weight Loss"),
        ("muscle_gain", "Muscle Gain"),
        ("maintenance", "Maintenance"),
        ("custom", "Custom"),
    ]         

    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES, default="custom")
    calories_per_day = models.PositiveIntegerField(help_text="Total daily calorie intake")
    meals = models.TextField(help_text="Enter meal details (e.g., breakfast, lunch, dinner, snacks, etc.)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_plan_type_display()} Plan ({self.calories_per_day} kcal/day)"

# Model for Feedback (No Gym ForeignKey)
class Feedback(models.Model):
    name = models.CharField(max_length=40)
    age = models.IntegerField(default=18)  
    rating = models.CharField(max_length=20)
    feedback = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    gym = models.ForeignKey(Gym,  on_delete=models.SET_NULL,  blank=True,  null=True,  related_name='feedbacks')

    def __str__(self):
        return self.name
    
# Model for Gym Members
class Member(models.Model):
    member_id = models.CharField(max_length=45, primary_key=True)
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    email = models.CharField(max_length=100, unique=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    state = models.CharField(max_length=30, null=True, blank=True)
    city = models.CharField(max_length=20)
    address = models.TextField(max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to="gym/member", blank=True, null=True)
    
    # Gym Membership (One Gym at a Time)
    gym = models.ForeignKey(Gym, on_delete=models.SET_NULL, related_name='members', null=True, blank=True)
    payment = models.BooleanField(default=True)  # Membership Payment Status

    def __str__(self):
        return self.name    

# Model for Queries & Doubts
class QueryDoubt(models.Model):
    member = models.ForeignKey(Member,on_delete=models.CASCADE, default="")
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    question = models.TextField(max_length=200)
    question_date = models.DateField(default=timezone.now)
    answer = models.TextField(default="")
    answer_date = models.DateField(default=None, blank=True, null=True)

    def __str__(self):
        return self.name          

class ResourceWork(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='workout_resources')
    title = models.CharField(max_length=255,)
    WORKOUT_TYPES = [
        ('Strength', 'Strength Training'),
        ('Cardio', 'Cardio'),
        ('Flexibility', 'Flexibility'),
        ('Endurance', 'Endurance'),
        ('Balance', 'Balance'),
    ]
    
    workout_type = models.CharField(max_length=50, choices=WORKOUT_TYPES, default='Strength')
    description = models.TextField()
    video = models.FileField(upload_to='gym/workouts/videos/', null=True, blank=True)
    image = models.ImageField(upload_to='gym/workouts/images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
#for gym news/notice    
class GymNews(models.Model):
    gym_id = models.CharField(max_length=50 ,default="")#refrence to gym model
    news_title = models.CharField(max_length=100)
    news_description = models.TextField() 
    news_time = models.DateTimeField(default=timezone.now) 
    


    def __str__(self):
        return f"{self.news_title[:30]}"   

class Message(models.Model):
    sender = models.ForeignKey(Member, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(Member, related_name="received_messages", on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(default=now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender} to {self.receiver}" 

class GymFacilities(models.Model):
    gym = models.ForeignKey(Gym,related_name='facilities', on_delete=models.CASCADE)
    body_part = models.CharField(max_length=60 ,choices=[
        ('Chest', 'Chest'),
        ('Back', 'Back'),
        ('Legs', 'Legs'),
        ('Arms', 'Arms'),
        ('Shoulders', 'Shoulders'),
        ('Abs', 'Abs'),
        ('Full Body', 'Full Body'),
        ('Cardio', 'Cardio'),
        ('Flexibility', 'Flexibility'),
    ])
    equipment_name =models.CharField(max_length=100)
    equipment_image = models.ImageField(upload_to='gym/gym_facilities')

    def __str__(self):
        return f"{self.equipment_name} -{self.body_part}"



       