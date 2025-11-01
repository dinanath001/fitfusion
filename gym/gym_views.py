from django.shortcuts import render ,redirect,get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import Gym, Trainer ,Member ,NutritionPlan ,ResourceWork ,Feedback ,QueryDoubt ,GymNews ,Event ,GymFacilities ,ApplicantDetail ,TrainerBooking
from .forms import TrainerForm 
from django.db.models import Q 

def register_gym(request):
    if request.method=='GET':
        return render(request,'gym/gym/gym_signup.html')
    
    if request.method=='POST':
        #take form data from server
        owner_id = request.POST['gym_id']
        owner_pass =request.POST['gym_password']
        Owner_Name = request.POST['owner_name']
        Gym_name =request.POST["name"]
        owner_city= request.POST["city"]
        owner_contact =request.POST["contact"]
        owner_address =request.POST['address']
        gym_pic = request.FILES.get('gym_image', None)
        #make Gym class object for saving from data
        gym_obj = Gym(gym_id=owner_id,password=owner_pass,owner_name=Owner_Name,gym_name=Gym_name,gym_city=owner_city,contact=owner_contact,address=owner_address,gym_image=gym_pic)
        #saving form data in Gym object
        gym_obj.save()
        messages.success(request,'Thankyou For Joining Our Fitness Organization😎')
        return redirect("gym_login")

def gym_login(request):
    if request.method=='GET':
        return render(request,'gym/gym/gym_login.html') 

    if request.method=="POST":
        owner_id = request.POST['gym_id']
        owner_pass =request.POST['password']
        gym_list = Gym.objects.filter(Q(gym_id=owner_id), Q(password=owner_pass))# ,Q(payment=True)
        size =len(gym_list)
        print('size is:',size)#if gym_list.exists():  

    if size ==1: #it means there is only one gym exists with the given credentials
        request.session['session_key']=owner_id
        request.session['role']="Gym"
        #This creates a session for the logged-in GymOwner.
        #role -->user is recognized as a GymOwner (useful for access control)
        owner_obj = gym_list[0]
        context ={'gym_owner':owner_obj}
        return render(request,'gym/gym/gym_home.html',context)
    
    else:
        messages.error(request,"Invalid Credentials or Your Gym is Black listed🙏🏿")
        return redirect("gym_login")
    
#this is use to go back to home page of identified user
   
def gym_home(request):
    if request.method=='GET':
        if 'session_key' not in request.session.keys():
           return redirect("gym_login")
        
        id =request.session['session_key']#session_key fetched in id
        gym_obj = Gym.objects.get(gym_id=id) #gym_id = id (match hoga) identified the real user
        context={'gym_owner':gym_obj}
        return render(request,'gym/gym/gym_home.html',context)

                         
def logout(request):
    if "session_key" not in request.session.keys():
            return redirect("gym_login")
    else:
        del request.session['session_key']
        request.session.flush() 
        del request.session['role']
        return redirect("gym_login")

def edit_owner_profile(request):
    if request.method=='GET':   
       if 'session_key' not in request.session.keys():
           return redirect("gym_login")
       else:
        id = request.session['session_key']
        gym_object = Gym.objects.get(gym_id=id)
        context = {'owner_key':gym_object}
        return render(request,'gym/gym/edit_profile.html',context)
    
    if request.method=='POST':
        gym_owner = request.POST['name']
        Gym_name =request.POST['gym_name']
        city =request.POST['city']
        contact =request.POST['phone']
        gym_address=request.POST['address']
        gym_pic = request.FILES.get('gym_image', None)

        id = request.session['session_key']
        gym_obj= Gym.objects.get(gym_id=id) 
        '''Uses .get() instead of .filter()
            filter() returns a QuerySet (which doesn't have .save())
              get() returns a single instance (which does have .save())'''
        gym_obj.owner_name = gym_owner
        gym_obj.gym_name = Gym_name
        gym_obj.gym_city = city
        gym_obj.contact = contact
        gym_obj.address = gym_address
        # Only update image if a new one is uploaded
        if gym_pic:
                gym_obj.gym_image = gym_pic
        gym_obj.save()  # Save the instance properly than update() method
        messages.success(request,'Profile update successful😀')
        return redirect("gym_home")

def add_trainer(request):
        if request.method=='GET':
            if "session_key" not in request.session:
                return redirect("gym_login")
            else:
                trainer_form =TrainerForm()
                context ={'form_key':trainer_form}
                return render(request,'gym/gym/trainer/add_trainer.html',context)
            
        
        if request.method=="POST":
            owner_id = request.session['session_key']#
            gym_obj= Gym.objects.get(gym_id=owner_id)
    
            train_form=TrainerForm(request.POST,request.FILES)#,request.FILES)
            if train_form.is_valid():
                trainer=train_form.save(commit=False) #data abhi save nhi hoga just put it on hold
                trainer.gym = gym_obj
                trainer.save()
    
                messages.success(request,"Trainer added successfully🙂🙂😊")
                return redirect('add_trainer')
           
def view_trainer(request):
    #  if request.method=="GET": 
          if "session_key" not in request.session:
                return redirect("gym_login")
          else:
            id= request.session['session_key']
            owner_gym = Gym.objects.get(gym_id=id)
            '''Your view_triner function retrieves all trainers belonging to
              the logged-in gym owner and displays them in view_trainer.html.'''
           # Fetch all trainers who belong to this gym
            trainer = Trainer.objects.filter(gym=owner_gym)
            return render(request, 'gym/gym/trainer/view_trainer.html', {'trainers': trainer})
               
                 

def delete_trainer(request ,trainer_id=None ):
    if "session_key" not in request.session:
        return redirect("gym_login")
    #id--> default primary key for trainer by Django
    trainer = get_object_or_404(Trainer, id=trainer_id)  # ✅ Ensures trainer exists, or shows 404#id--> automatically create id by django/
    trainer.delete()  # ✅ Deletes only this trainer

    messages.success(request, "Trainer deleted successfully!")
    return redirect("view_trainer")

def view_feed(request):
    if "session_key" not in request.session:
        return redirect('gym_login')
    else:
        id= request.session['session_key']
        owner_gym = Gym.objects.get(gym_id=id)
        #fetch all feddbak for this gym
        feed = Feedback.objects.filter(gym=owner_gym).order_by('-id') #→ Newest feedback first
        context={'feed_key':feed}
        return render(request,'gym/gym/view_feedback.html',context)

def view_members(request):
    if "session_key" not in request.session:
        return redirect("gym_login")
    else:
        id= request.session['session_key']
        owner_gym = Gym.objects.get(gym_id=id)
        #fetch all members who belong to this gym
        member_list =Member.objects.filter(gym=owner_gym)
        trainer_book = TrainerBooking.objects.filter(member__in= member_list)
        context={'member_key':member_list,
                  'trainer_key': trainer_book}
        return render(request,'gym/gym/view_members.html',context)


def toggle_payment_status(request, member_id=None):
    if "session_key" not in request.session:
        return redirect("gym_login")

    member = Member.objects.get(member_id=member_id)  # ✅ Fetch member using `member_id`(model->id,parameter->id)
    member.payment = not member.payment  # ✅ Toggle payment status
    member.save()

    messages.success(request, f"Payment status updated for {member.name}!")
    return redirect("view_members")  # Redirect back to the member list
    

def add_nutrition(request):
        if request.method=="GET":
           if "session_key" not in request.session:
              return redirect("gym_login")
           return render(request,"gym/gym/add_nutrition.html")

        if request.method=="POST":
            id  =request.session["session_key"]
            gym_owner =Gym.objects.get(gym_id=id)#for gym identification

            plan_typ = request.POST['plan_type']
            calories = request.POST["calories_per_day"]
            meal = request.POST["meals"]
            

            nutrition_obj = NutritionPlan(gym=gym_owner,plan_type=plan_typ,calories_per_day=calories,meals=meal)
            nutrition_obj.save()
            messages.success(request,'Nutrition added Successfully')
            return redirect("add_nutrition")
        
#now we r going to add workout for only gym members  so members can see their gym workout
def add_workout(request):
    if request.method=="GET":
        if "session_key" not in request.session:
          return redirect("gym_login")
        else:
           return render(request,"gym/gym/add_work_resource.html")
    
    if request.method=="POST":
        id = request.session["session_key"]#bind logined user identification in (id)
        gym_owner = Gym.objects.get(gym_id=id)#identify/match the Gym user by id in Gym table

        topic=request.POST['title']
        type =request.POST['workout_type']
        desc = request.POST['description']
        videos =request.FILES['video']
        image =request.FILES['image']

        work_obj = ResourceWork(gym=gym_owner,title=topic,workout_type=type,description=desc,video=videos,image=image)
        work_obj.save()
        messages.success(request,'Workout added Successfully')
        return redirect("add_workout")
    

    
def query_handel(request):
    if request.method=="GET":
        if 'session_key' not in request.session:
            return redirect("gym_login")
        else:
            id= request.session['session_key']
            owner_gym = Gym.objects.get(gym_id=id) 

            #fetch all query belong to gym's member
            query_list = QueryDoubt.objects.filter(member__gym=owner_gym)
            context = {'query_key' : query_list,}
            return render(request , 'gym/gym/query_ans.html',context)
        
    if request.method=='POST':
        query_id = request.POST.get("query_id")
        answer_text = request.POST.get("answer")

        id= request.session['session_key']#pass it again because it throws error(gym_owner is not defined -->in post method)
        owner_gym = Gym.objects.get(gym_id=id)

        query_member = QueryDoubt.objects.filter(id=query_id, member__gym=owner_gym).first()
        if query_member:
           query_member.answer = answer_text
           query_member.answer_date = timezone.now()
        
           query_member.save()
         # user_question.save()
           messages.success(request,"Thankyou for your valuable answer 🙂🙂😊")
           return redirect('query_handel')

'''now we will add news and event by gym owner / but event model has gym_id-->charfield so hm session_key se data leke then gym_id me bind kr denge''' 

def add_news(request):
    if request.method =="GET":
        if "session_key" not in request.session:
            return redirect("gym_login")
        return render(request,'gym/gym/add_news.html')

    if request.method=="POST":
        id= request.session['session_key']
        owner_gym = Gym.objects.get(gym_id=id) 

        notice = request.POST["news_title"]
        descr = request.POST["news_description"]

        news_obj = GymNews(gym_id=owner_gym,news_title=notice,news_description=descr)
        news_obj.save()
        messages.success(request,"Thnkyou for adding news😀")
        return redirect("add_news")
    
def add_event(request):
    if request.method =="GET":
        if "session_key" not in request.session:
            return redirect("gym_login")
        return render(request,'gym/gym/add_event.html')
    
    if request.method=="POST":
        id= request.session['session_key']
        owner_gym = Gym.objects.get(gym_id=id)
        #taking data form template form controls
        name = request.POST["event_name"]
        venue =request.POST["event_venue"]
        desc =request.POST["event_description"]
        image =request.FILES["event_image"]

        event_obj = Event(gym_id=owner_gym,event_name=name,event_venue=venue,event_description=desc,event_image=image)
        event_obj.save()
        messages.success(request,"Thnkyou for adding Event's😀")
        return redirect("add_event")
    
def add_equipment(request):
    if request.method=="GET":
        if "session_key" not in request.session:
           return redirect("gym_login")
        return render(request ,'gym/gym/add_equipment.html')

    if request.method=="POST":
        id = request.session["session_key"]
        owner_gym = Gym.objects.get(gym_id=id)
        #taking form inputs in variable
        '''equipment_name[] is a list. | Each equipment_imagesX[] is also a list of uploaded files.'''

        part = request.POST["body_part"]
        equip_name = request.POST.getlist("equipment_name[]")
        for i in range(1,6):  # For equipment1 to equipment5

           if i - 1 < len(equip_name):
            name = equip_name[i-1]

            image_field_name = f'equipment_images{i}[]'

            images = request.FILES.getlist(image_field_name)
            for img in images:
                eqip_obj = GymFacilities(gym = owner_gym ,body_part=part,equipment_name=name,equipment_image=img)# Single image per entry
                eqip_obj.save()
     
        messages.success(request,'Thnkyou for adding equipments💪🏿')    
        return redirect("add_equipment")
        '''This condition if i - 1 < len(equipment_names) prevents "IndexError"'''
        '''Checks GET vs POST method ✅

            Confirms session before allowing access ✅
            
            Retrieves the correct Gym object ✅
            
            Loops through equipment entries ✅
            
            Loops through multiple images per equipment ✅
            
            Saves each image individually for each equipment ✅
            
            Shows a success message and redirects ✅'''
        
def view_equipment(request):
     if request.method=="GET":
          if "session_key" not in request.session:
                return redirect("gym_login")
          else:
            id= request.session['session_key']
            owner_gym = Gym.objects.get(gym_id=id)
            '''Your view_equipment function retrieves all added equip.. belonging to
              the logged-in gym owner and displays them in view_trainer.html.'''
           # Fetch all equipments who belong to this gym
            equip_list = GymFacilities.objects.filter(gym=owner_gym)
            return render(request, 'gym/gym/view_equipment.html', {'equip_key': equip_list})
          
def delete_equipment(request ,equipment_id):
    if "session_key" not in request.session:
        return redirect("gym_login")
    else:
        equipments = GymFacilities.objects.get(id=equipment_id) #id-->primary_key autogenerated
        equipments.delete()

        messages.success(request,'Deleted equipment success...🙂')
        return redirect(view_equipment)#view-->logical fun name /gym_views.view_equipment/
    
def view_applicant(request):
    if "session_key" not in request.session:
        return redirect("gym_login")
    else:
        id = request.session["session_key"]
        owner_gym = Gym.objects.get(gym_id=id) #gym_id-->model field(pk)
        '''fetch all applications which applied for specific gym'''
        applicant_list = ApplicantDetail.objects.filter(gym_id = owner_gym.gym_id)#This compares string to string, which will work with your current model.
        return render(request,'gym/gym/view_applicants.html',{'appli_key':applicant_list})
        '''You're comparing a Gym object (owner_gym) to a string (gym_id) in ApplicantDetail.-->filter(gym_id = owner_gym)'''

def manage_trainer_booking(request):
    if request.method=="GET":
        if "session_key" not in request.session:
           return redirect('gym_login')
        else:
            id = request.session["session_key"]
            owner_gym = Gym.objects.get(gym_id=id)

            gym_trainers= Trainer.objects.filter(gym=owner_gym)
            booking_requests = TrainerBooking.objects.filter(trainer__in=gym_trainers).exclude(status='confirmed').order_by('-request_date')
            return render(request,'gym/gym/manage_trainer_booking.html',{'booking_key':booking_requests})
        '''.filter() gives multiple results (a queryset),
             .get() gives only one result (single object),           
             When you have multiple trainers, you must always use __in=, not just =.'''

    if request.method=="POST":
        request_id = request.POST["request_id"]
        status = request.POST['status']  # 'confirmed' or 'denied'
        booking_obj = TrainerBooking.objects.get(id = request_id)
        booking_obj.status= status
        if status == "confirmed":
            booking_obj.confirmation_date = timezone.now()
        booking_obj.save()
        messages.success(request, f'Booking {status} successfully!')
        return redirect("manage_trainer_booking")    
    












  



        
    
