from django.shortcuts import render ,redirect
from django.contrib import messages
from django.utils import timezone
from .models import Feedback,Gym ,Member,QueryDoubt,Trainer ,ResourceWork ,GymNews ,Message , TrainerBooking
from .forms import UserQuery
from django.db.models import Q 

def feedback(request):
    if request.method=="GET":
           if "session_key" not in request.session.keys():
             return redirect("member_login")
        
           return render(request ,'gym/member/feedback.html')
    
    if request.method == "POST":
         # Get the gym from the logged-in member
        # selected_gym = member.gym  
        # Retrieve form data
        # user_name = request.POST.get('name', '')  
        user_age = request.POST.get('age', '')
        user_rating = request.POST.get('rating', '')
        user_feedback = request.POST.get('feedback', '')
         #geting member identity
        id = request.session["session_key"]
        member =Member.objects.get(member_id=id)
        selected_gym = member.gym # Get the gym from the member

        feedback_obj = Feedback(name=member,age=user_age, gym=selected_gym,rating=user_rating,feedback=user_feedback)
        feedback_obj.save()#ORM mapping with Feedback table fields
        messages.success(request,"Thanku for your valuable feedback , will consider this very soon😎😎")
        return redirect('feedback')
    
def register_member(request):
    if request.method=="GET":
        gyms = Gym.objects.all()  # Fetch all gyms
        return render(request,'gym/member/member_registration.html',{'gym_key':gyms})
    
    if request.method=='POST':
        user_id = request.POST['id']
        user_pass= request.POST['password']
        user_name = request.POST['name']
        user_phone = request.POST['phone']
        user_email=request.POST['email']
        user_gender = request.POST['gender']
        user_state= request.POST['state']
        user_city= request.POST['city']
        user_address=request.POST['address']
        user_pic = request.FILES['profile_picture']
        selected_gym_id = request.POST.get('gym')

        selected_gym = Gym.objects.filter(gym_id=selected_gym_id).first()
        mem_reg_obj = Member(
            member_id=user_id,
            password=user_pass,
            name=user_name,
            phone=user_phone,
            email=user_email,
            gender=user_gender,
            state=user_state,
            city=user_city,
            address=user_address,
            profile_picture=user_pic,
            gym=selected_gym
            )
        mem_reg_obj.date_joined = timezone.now()  
        mem_reg_obj.save()
        messages.success(request,'Thnkyou for Joining Us now you are part of our organization')
        return redirect(member_login)#logical name of view('we can also put urls(name='member_login')here)
    
def member_login(request):
    if request.method=='GET':
        return render(request,'gym/member/member_login.html')
    
    if request.method=='POST':
        mem_id = request.POST['id']
        mem_pass=request.POST['password']
        mem_list = Member.objects.filter(Q(member_id=mem_id) & Q(password=mem_pass)& Q(payment=True))# & Q(payment=True)
        size = len(mem_list)
        print('size is:',size)#if member_list.exists():
                         
    if size==1:#If size == 1, it means exactly one member exists with the given credentials.
        
        #This creates a session for the logged-in member.
        #The session_key stores the member’s ID, allowing Django to remember the user across different pages.
        #"role": "Member" ensures that this user is recognized as a member (useful for access control).
        request.session['session_key']=mem_id
        request.session['role']='Member'

        #Since member_list contains exactly one matching member, we extract that single object (from the query list).
        #Now, member_obj holds all details of the logged-in member.
        member_obj = mem_list[0]

        context = {'member_key' :member_obj}
        return render(request,'gym/member/member_home.html',context)
    
    else:
          messages.error(request,"Invalid user id and password or Your fees has been not deposited")#message.error is predifined tag
          return redirect("member_login")
    
    
def member_home(request):
    if request.method=='GET':
        if "session_key" not in request.session.keys():
            return redirect("member_login")

        id= request.session['session_key']
        mem_object=Member.objects.get(member_id=id)
        
        context={'member_key':mem_object}
        return render(request,'gym/member/member_home.html',context) 

def logout(request):
    if "session_key" not in request.session.keys():
            return redirect("member_login")
    
    else:
        del request.session['session_key']
        del request.session['role']
        return redirect('member_login')
    
def edit_profile(request):
    if request.method=='GET':
        if "session_key" not in request.session.keys():
            return redirect("member_login")
        else:
            id=request.session['session_key']
            member_obj = Member.objects.get(member_id=id)#member_id-->model field
            gyms = Gym.objects.all()
            context={'member_key':member_obj, #for showing all detail of member on editing form
                     'gym_key':gyms
                     }
            return render(request,'gym/member/edit_profile.html',context)
        
    if request.method=='POST':
        #taking data from forn controls
        user_name=request.POST['name']
        user_email=request.POST['email']
        user_phone=request.POST['phone']
        user_state=request.POST['state']
        user_city=request.POST['city']
        user_addr=request.POST['address']
        gym =request.POST['gym']

        #match id with session key
        #This line fetches the logged-in user's ID from the session.
        #"session_key" is the session variable that stores the member_id of the currently logged-in user.
        id = request.session['session_key']
        gym_obj = Gym.objects.get(gym_id=gym)  # Fetch selected gym
        Member.objects.filter(member_id=id).update(
            name=user_name,
            email=user_email,
            phone=user_phone,
            state=user_state,
            city=user_city,
            address=user_addr,
            gym=gym_obj #update gym field 
            )
        messages.success(request,'Profile update successful😀')
        return redirect("member_home")
         # Finds the member with the stored session ID and updates their profile.
         # Instead of fetching the object and saving it separately, .filter(member_id=id).update(...) updates the matching database row directly.
         # It updates the name, email, phone, state, city, and address fields with the new values the user entered.
         # Using .update() is more efficient than loading the object and calling .save().
    
def query_doubt(request):
    if request.method=='GET':
        if "session_key" not in request.session.keys():
            return redirect("member_login")
        
        else:
            user_form = UserQuery()
            context={'form_key':user_form}
            return render(request,'gym/member/query_doubt.html',context)

    if request.method=='POST': 
        
        id=request.session["session_key"]
        if id is None:
          return redirect('member_login')
        
        user_question=UserQuery(request.POST)#,request.FILES)
        if user_question.is_valid():
        
         user_doubt=user_question.save(commit=False) #data abhi save nhi hoga just put it on hold
         user_doubt.member_id=id #member_id-->member (but it work still)
         user_doubt.save()
         # user_question.save()
         messages.success(request,"Thankyou for your query we'll Answer you soon☺🙂🙂😊")
        return redirect('query_doubt')   
        #✅ Saves the form data but does NOT commit it to the database yet.
        #✅ The commit=False flag means we are creating an object but not saving it, so we can modify it before saving 
        #✅ Without commit=False, Django would have saved the form without the member_id, causing an error.
         #(✅ Assigns the current user's ID (from the session) to the member_id field of user_doubt.
         #✅ This links the query to the logged-in member.)

def view_answer(request):
    if "session_key" not in request.session.keys():
        return redirect("member_login")
    
    else:
        id= request.session['session_key']
        match_member = Member.objects.get(member_id=id)
        
        answer_list = QueryDoubt.objects.filter(member = match_member )#member --> has foreign key(to Member) in model
        '''answer_list = QueryDoubt.objects.filter(member_id=id) -->this is also work because member is linked to only one gym'''
        context = {'ans_key':answer_list}
        return render(request,'gym/member/view_ans.html',context)#now query is asked by member but answer will given by member's gym owner 
    
def work_resource(request):
    if 'session_key' not in request.session:
        return redirect('member_login')
    
    else:
        id = request.session['session_key']
        member = Member.objects.get(member_id=id)#
        match_gym = member.gym
        #fetch all workout who belong to members gym
        workout_resource = ResourceWork.objects.filter(gym=match_gym)
        context = {'workout_key': workout_resource}
        return render(request,'gym/member/workout_resource.html',context)
'''workout_resource = ResourceWork.objects.filter(gym=Member.objects.get(member_id=request.session["session_key"]).gym)'''#optional

def view_notice(request):
    if 'session_key' not in request.session:
        return redirect("member_login")
    else:
        id =request.session["session_key"]
        member = Member.objects.get(member_id=id)
        #now we match the data should come from registered gym of membr
        match_gym = member.gym
        #fetch all news which belong to logined register gym
        news_list = GymNews.objects.filter(gym_id=match_gym)
        context = {'news_key':news_list}
        return render(request,'gym/member/view_notice.html',context)
    
def trainers(request):
    if 'session_key' not in request.session:
        return redirect("member_login")
    else:
        id =request.session["session_key"]#identify the logined user
        member = Member.objects.get(member_id=id)
         #now we match the data should come from registered gym of membr
        match_gym = member.gym
        trainer_list=  Trainer.objects.filter(gym=match_gym)                      
        context = {'trainer_key':trainer_list}
        return render(request ,'gym/member/view_trainer.html',context)

def inbox(request):
    if 'session_key' not in request.session:
        return redirect("member_login")
    else:
        id =request.session["session_key"]#identify the logined user
        member = Member.objects.get(member_id=id)
        message_list = Message.objects.filter(receiver=member).order_by('-timestamp')
        context ={'message_key':message_list}
        return render(request , 'gym/message/inbox.html',context)

def sent_message(request):
    if 'session_key' not in request.session:
        return redirect("member_login")
    else:
        id =request.session["session_key"]#identify the logined user
        member = Member.objects.get(member_id=id)
        message_list = Message.objects.filter(sender=member).order_by('-timestamp')#filter by -- sender = member(logined member)
        context ={'message_key':message_list}
        return render(request , 'gym/message/sent.html',context)    

def compose_message(request):
    if request.method=="GET":
       if 'session_key' not in request.session:
         return redirect("member_login")
       else:
           id =request.session["session_key"]
           user_list =Member.objects.exclude(member_id=id) #fetch all users except the logged-in user.
           #user_list =Member.objects.all() -->optional hai as per need
           return render(request,'gym/message/compose.html',{'user_key':user_list})        
     
    if request.method=="POST":
        id =request.session["session_key"]#identify the logined user
        member = Member.objects.get(member_id=id)#used to identify sender 

        receiver_id = request.POST["receiver"]   
        message_content =request.POST["message"]
        receiver = Member.objects.get(member_id=receiver_id)#Finds the recipient using the member_id provided in the form. -->store the reciever id from template
        message_obj = Message(sender=member,receiver=receiver,message=message_content)
        message_obj.save()
        #return redirect('/inbox/')
        messages.success(request ,'message sent successfully😎')
        # return render(request ,'gym/message/compose.html') -->it save the same data again and again
        return redirect("compose_message")  

def delete_message(request ,message_id=None):
    if request.method=="POST": #post--> action perform from inbox.html
        if "session_key" not in request.session:
           return redirect("member_login")
        else:
          message = Message.objects.get(id=message_id)
          message.delete()
          messages.success(request ,'Deleted mssg')
          return redirect("inbox")

def book_trainer(request):
    if  request.method=="GET":
        if "session_key" not in request.session.keys():
            return redirect("member_login")
        id = request.session["session_key"]
        member =  Member.objects.get(member_id=id)
         #now we match the data should come from registered gym of membr
        match_gym = member.gym
        trainer_list = Trainer.objects.filter(gym=match_gym)
        return render(request,'gym/member/book_trainer.html',{'trainer':trainer_list})
    
    if request.method=="POST":
        id = request.session["session_key"]
        member =  Member.objects.get(member_id=id)

        trainer_id = request.POST['trainer_id']
        try:
          trainer = Trainer.objects.get(id=trainer_id)#If somehow the trainer_id is invalid (trainer not found), it will crash.
        except Trainer.DoesNotExist:
          messages.error(request, "Trainer not found!")
          return redirect("book_trainer")

        book_obj = TrainerBooking(member=member , trainer=trainer)
        book_obj.save()
        messages.success(request,'Booking request send successfully💪🏿')
        return redirect("book_trainer")
    
def trainer_confirmation(request):
    if "session_key" not in request.session:
        return redirect("member_login")
    else:
        id = request.session['session_key']
        match_member = Member.objects.get(member_id=id)

        booking_request = TrainerBooking.objects.filter(member=match_member , status='confirmed').first()
        return render(request,'gym/member/trainer_confirm.html',{'confirm_key':booking_request})    


import joblib
import os
from django.shortcuts import render, redirect
from django.conf import settings

# Load the saved ML model
model_path = os.path.join(settings.BASE_DIR, 'gym', 'ml_models', 'calorie_predictor_model.pkl')
calorie_model = joblib.load(model_path)

def calorie_predictor(request):
    if 'session_key' not in request.session:
        return redirect("member_login")

    if request.method == "POST":
        # Get form data
        age = int(request.POST['age'])
        weight = int(request.POST['weight'])  # kg
        height = int(request.POST['height'])  # cm
        gender = int(request.POST['gender'])  # 0 = Male, 1 = Female
        activity_level = int(request.POST['activity_level'])  # 1 = Low, 2 = Medium, 3 = High
        body_fat_percent = float(request.POST['body_fat_percent'])  # %
        sleep_hours = float(request.POST['sleep_hours'])  # hours per night

        # Derived feature: BMI
        height_m = height / 100
        bmi = weight / (height_m ** 2) #square  or pow(5,2)

        # Prepare input for the model
        user_input = [[
            age, weight, height, gender, activity_level, bmi, body_fat_percent, sleep_hours
        ]]

        # Predict calories
        predicted_calories = calorie_model.predict(user_input)[0]

        return render(request, 'gym/member/calorie_result.html',{'calories': int(predicted_calories)})

    # GET request
    return render(request, 'gym/member/calorie_form.html')


                                                    

          
                                
  
        
            


        
            









    


          
        
    
     
    
  



