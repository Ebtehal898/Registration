from django.db import models
from datetime import datetime
import re

# Create your models here.
class UserManager(models.Manager):
    
    def validate(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        current_date= datetime.now().date()
        errors = {}
        email_list=self.filter(email=postData['email'])

        #---------------------- First Name Validation ------------------------
        if len(postData['first_name']) <2:
            errors["first_name_long"] = "First name should be at least 2 characters."
        if postData['first_name'].isalpha() == False:
            errors['first_name_alph'] = "First name must be letters only"

        #---------------------- Last Name Validation -------------------------
        if len(postData['last_name']) <2:
            errors["last_name"] = "Last name should be at least 2 characters."
        if postData['last_name'].isalpha() == False:
            errors['last_name'] = "Last name must be letters only."

        #---------------------- Email Validation -------------------------
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"    
        if len(email_list)>0:
                errors["email_uniqe"] = "This email is already exist."

        #---------------------- Birthday Validation ---------------------------
        if len(postData["birthday"])>1: 
            if datetime.strptime(postData['birthday'], "%Y-%m-%d").date() >= current_date:
                errors["birthday"] = "Invalid Birth Date!"  
            elif int( (current_date - datetime.strptime(postData['birthday'], "%Y-%m-%d").date() ).days / 365.25)<13:
                print ("The age is ",int( (current_date - datetime.strptime(postData['birthday'], "%Y-%m-%d").date() ).days / 365.25))
                errors["age"] = "Your age should be at least 13 years old!" 

                
        #---------------------- Password Validation -------------------------
        if len(postData['password']) <8 or len(postData['confirm_pass'])<8 :
            errors["password"] = "Password should be at least 8 characters."
        
        #---------------------- Confirm Password Validation -------------------
        if len(postData['password']) >8 and len(postData['confirm_pass'])>8 :
            if postData['password'] != postData['confirm_pass']:
                errors['confirm_pass'] = "Passwords are not matched!"

        
        return errors
    #************************************* [validate_login] ***************************************
    def validate_login(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}

        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!" 
        
        if len(postData['password']) <8:
            errors["password"] = "Password should be at least 8 characters."
        
        return errors
    

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    birthday= models.DateField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()   

    def __repr__ (self):
        return f"<User object: First Name = {self.first_name} , Last Name = {self.last_name} , Email = {self.email}, Birthday ={self.birthday}>"
