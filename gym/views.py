from django.shortcuts import render,HttpResponse,redirect

from FitFusion import settings

from .models import Event ,News , Contact  , Workout ,Gym,Member,Trainer ,NutritionPlan ,Feedback ,GymFacilities
from .forms import ApplicantDetailForm
from django.contrib import messages
from django.db.models import Q    


# Create your views here.
def home(request):
    news_list = News.objects.order_by('-news_time')[:5]#set limit by time 
    latest_event = Event.objects.order_by('-event_date').first()  # Latest event
    reviews = Feedback.objects.order_by('-date')[:5]
    context = {
    "notice_key": news_list, #pass news
    "event_key": latest_event,  # Pass only the latest event
    "feedback_key" : reviews, #pass feedback data
    
     }
    return render(request, 'gym/html/index.html',context)

def review(request):
   feed_list = Feedback.objects.order_by('-date')
   context={'feed_key':feed_list}
   return render(request,'gym/html/feed.html',context)

def event(request):
   
   event_list = Event.objects.order_by('-event_date')
   return render(request , 'gym/html/event.html',{'event_key':event_list})

def about(request):
   return render(request , 'gym/html/about.html')

def contact(request):
    if request.method=="GET":
     return render(request ,'gym/html/contact.html')
    #  #return HttpResponse("<h1> You Can contact us via our official Mail</h1>")
    if request.method == "POST":  # HTTP protocol sends user data using POST method
        # Use .get() to avoid KeyErrors
        user_name = request.POST.get("name", "Anonymous")  
        user_email = request.POST.get("email", "No Email Provided")
        user_message = request.POST.get("message", "").strip()  # Ensure no empty messages

        # Validate that message is not empty
        if not user_message:
            messages.error(request, "Message cannot be empty.")
            return render(request, "gym/html/contact.html")

        # Save to database
        contact_obj = Contact(name=user_name, email=user_email, message=user_message)
        contact_obj.save()

        # Show success message
        messages.success(request, "❤❤ Thank you for contacting us! We will reach out soon 😎😎")
        return redirect("contact")  # Redirect to prevent duplicate submissions

    # 🔴 Default return statement to handle unexpected cases
    return render(request, "gym/html/contact.html")

def demo(request):
   return render(request , 'gym/html/demo.html')

def workout_public(request):
   workout_list = Workout.objects.order_by('title')
   context = {
      'workout_key' : workout_list
   }
   return render(request , 'gym/html/workout_public.html' ,context)

def nutrition(request):
   nutrition_list = NutritionPlan.objects.all()
   context = {'nutrition_key' : nutrition_list}
   return render(request , 'gym/html/nutrition.html',context)

def bodybuilding(request):
   return render(request ,'gym/html/bodybuilding.html')

def cardio(request):
   return render(request ,'gym/html/cardio_train.html')

def HIIT(request):
   return render(request ,'gym/html/hiit_train.html')

def strength(request):
   return render(request ,'gym/html/strength_train.html')

def yoga(request):
   return render(request ,'gym/html/yoga_train.html')

def trainer_detail(request):
   trainer_list = Trainer.objects.order_by('name')[:6]
   context =  {'trainer_key' : trainer_list}
   return render(request , 'gym/html/trainer_details.html' ,context)



def career(request):
    if request.method == "GET":
        application = ApplicantDetailForm()
        gym_list = Gym.objects.all()
        context = {'form': application, 'gym_key': gym_list}  # Pass gym list to context
        return render(request, 'gym/html/career.html', context)
   
    if request.method == "POST":
        application = ApplicantDetailForm(request.POST, request.FILES)
        if application.is_valid():
            application.save()
            messages.success(request, 'Thank you for applying! We will contact you soon. 😊')
            return redirect('career')  # Ensure correct URL name or use reverse()




#import pagination for big search fields
from django.core.paginator import Paginator

def gym_locator(request, gym_name=None):  
    #  Fetch all gyms from the database
    gyms_queryset = Gym.objects.all()

    #  Filter by gym name if provided in the URL
    if gym_name:
        gyms_queryset = gyms_queryset.filter(gym_name__icontains=gym_name)

    #  Get the search query from GET parameter (gym_city)
    search_city = request.GET.get('gym_city')
    if search_city:
        gyms_queryset = gyms_queryset.filter(gym_city__icontains=search_city) #gyms_queryset--> Gym.objects.all()

    
    paginator = Paginator(gyms_queryset, 5)
    current_page_number = request.GET.get('page')
    gyms_page = paginator.get_page(current_page_number)

   
    context = {
        'gym_key': gyms_page,        
        'query': search_city,         
        'gym_name': gym_name          
    }

    return render(request, 'gym/html/gym_locator.html', context)


def gym_details(request , gym_id):
   gym = Gym.objects.get(gym_id=gym_id)
   #fetch data from GymFac.. table 
   #Then it fetches the related gym facilities from the GymFacilities table, filtering by this gym
   equip_list = GymFacilities.objects.filter(gym = gym).order_by('-body_part')
   context ={
      'equip_key': equip_list,
        'gym': gym
           }
   return render(request,'gym/html/gym_details.html',context)


def search_results(request):
   query = request.GET.get('key' ,'').strip()
   results = {} #dictionary to store the search results

   if query:
        #Q(gym__icontains=query)  ❌  # gym is a ForeignKey, this won't work
         news_results = News.objects.filter(Q(news_title__icontains=query) | Q(gym__gym_name__icontains=query))
         if news_results.exists(): 
           results['news'] = news_results #store the news results under 'news' key
         
         #seach result in Event model
         event_results = Event.objects.filter(Q(event_name__icontains=query) | Q(event_venue__icontains=query)| Q(gym_id__icontains=query))
         if event_results.exists():
            results['event']= event_results #store the event results under 'event' key
 
         gym_results = Gym.objects.filter(Q(gym_name__icontains=query) | Q(gym_city__icontains=query) | Q(address__icontains=query))
         if gym_results.exists():
            results['gym'] =gym_results #store gym results under 'gym' key
 
         trainer_results = Trainer.objects.filter(Q(gym__gym_name__icontains=query)| Q(name__icontains=query)| Q(email__icontains=query))
         if trainer_results.exists():
            results['trainer'] = trainer_results
 
         nutrition_results = NutritionPlan.objects.filter(Q(plan_type__icontains=query)| Q(meals__icontains=query))
         if nutrition_results.exists():
            results['nutrition'] = nutrition_results

         feedback_results = Feedback.objects.filter(Q(name__icontains=query)|Q(rating__icontains=query)|Q(feedback__icontains=query)) 
         if feedback_results.exists():
            results['feedback'] = feedback_results

         member_results = Member.objects.filter(Q(name__icontains=query)|Q(phone__icontains=query)|Q(email__icontains=query)|Q(state__icontains=query)| Q(city__icontains=query))
         if member_results.exists():
            results['member'] = member_results
         '''The .strip() method in Python is used to
           remove any leading and trailing whitespace
             (spaces, tabs, newlines) from a string.''' 

   return render(request , 'gym/html/search_results.html',{'query':query ,'results':results})
    

from django.core.mail import send_mail

def send_email_view(request):
    if request.method == 'GET':
       # Render form for GET request
       return render(request, 'gym/html/send_email.html')
       
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        to_email = request.POST.get('to_email')

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [to_email],
            fail_silently=False,
        )
        # Render success page after sending email
        return render(request, 'gym/html/success.html', {'to_email': to_email})
    
    

            

             

      








