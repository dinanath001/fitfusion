from django.urls import path 
from . import views, member_views, gym_views

urlpatterns = [
    # -------------------- General Public Views --------------------
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('demo/', views.demo),
    path('career/', views.career, name='career'),
    path('event/', views.event, name='event'),
    path('review/', views.review, name='review'),
    path('search_results/', views.search_results, name='search_results'),

    # -------------------- Workout & Health Content --------------------
    path('trainer/', views.trainer_detail, name='trainer'),
    path('workout_public/', views.workout_public, name='workout_public'),
    path('bodybuilding/', views.bodybuilding, name='bodybuilding'),
    path('cardio/', views.cardio, name='cardio'),
    path('HIIT/', views.HIIT, name='HIIT'),
    path('strength/', views.strength, name='strength'),
    path('yoga/', views.yoga, name='yoga'),
    path('nutrition/', views.nutrition, name='nutrition'),

    # -------------------- Gym Location & Details --------------------
    path('gym_locator/', views.gym_locator, name='gym_locator'),
    path('gym_locator/<str:gym_name>/', views.gym_locator, name='gym_locator_with_name'),
    path('gym_details/', views.gym_details, name='gym_details'),
    path('gym_details/<str:gym_id>/', views.gym_details, name='gym_details'),

    # -------------------- Member Views --------------------
    path('register_member/', member_views.register_member, name='register_mem'),
    path('member_login/', member_views.member_login, name='member_login'),
    path('member_home/', member_views.member_home, name='member_home'),
    path('logout/', member_views.logout, name='logout'),
    path('edit_profile/', member_views.edit_profile, name='edit_profile'),
    path('feedback/', member_views.feedback, name='feedback'),
    path('query_doubt/', member_views.query_doubt, name='query_doubt'),
    path('view_answer/', member_views.view_answer, name='view_answer'),
    path('work_resource/', member_views.work_resource, name='work_resource'),
    path('view_notice/', member_views.view_notice, name='view_notice'),
    path('trainers/', member_views.trainers, name='trainers'),

    # ----- Messaging -----
    path('inbox/', member_views.inbox, name='inbox'),
    path('sent_message/', member_views.sent_message, name='sent_message'),
    path('compose_message/', member_views.compose_message, name='compose_message'),
    path('delete_message/<int:message_id>/', member_views.delete_message, name='delete_message'),
    # path('message_detail/', member_views.message_detail, name='message_detail'),  # optional

    # ----- Trainer Booking -----
    path('book_trainer/', member_views.book_trainer, name='book_trainer'),
    path('trainer_confirm/', member_views.trainer_confirmation, name='trainer_confirm'),

    # ----- Tools -----
    path('calorie_predictor/', member_views.calorie_predictor, name='calorie_predictor'),

    # -------------------- Gym Views --------------------
    path('register_gym/', gym_views.register_gym, name='register_gym'),
    path('gym_login/', gym_views.gym_login, name='gym_login'),
    path('logout/', gym_views.logout, name='logout'),
    path('gym_home/', gym_views.gym_home, name='gym_home'),
    path('edit_owner_profile/', gym_views.edit_owner_profile, name='edit_owner_profile'),

    # ----- Trainer Management -----
    path('add_trainer/', gym_views.add_trainer, name='add_trainer'),
    path('view_trainer/', gym_views.view_trainer, name='view_trainer'),
    path('delete_trainer/<int:trainer_id>/', gym_views.delete_trainer, name='delete_trainer'),

    # ----- Member Management -----
    path("view_members/", gym_views.view_members, name='view_members'),
    path('toggle-payment/<str:member_id>/', gym_views.toggle_payment_status, name="toggle_payment_status"),

    # ----- Nutrition & Workout -----
    path('add_nutrition/', gym_views.add_nutrition, name='add_nutrition'),
    path('add_workout/', gym_views.add_workout, name='add_workout'),

    # ----- Feed, Events, News -----
    path('view_feed/', gym_views.view_feed, name='view_feed'),
    path('add_news/', gym_views.add_news, name='add_news'),
    path('add_event/', gym_views.add_event, name='add_event'),

    # ----- Doubts / Query Handling -----
    path('query_handel/', gym_views.query_handel, name="query_handel"),
    path('manage_trainer_booking/', gym_views.manage_trainer_booking, name='manage_trainer_booking'),

    # ----- Equipment Management -----
    path('add_equipment/', gym_views.add_equipment, name='add_equipment'),
    path('view_equipments/', gym_views.view_equipment, name='view_equipments'),
    path('delete-equipment/<int:equipment_id>/', gym_views.delete_equipment, name='delete_equipment'),

    # ----- Applicants -----
    path('all_applicant/', gym_views.view_applicant, name='all_applicant'),
]
