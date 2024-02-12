from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from .constants import course_type, course_status

# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, mobile_number, name, role='student', is_admin=False, password=None):
        if not mobile_number:
            raise ValueError('User must have a Mobile Number')
        user = self.model(
            mobile_number=mobile_number,
            name=name,
            role=role,
            is_admin=is_admin
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_teacher(self, mobile_number, name, role='teacher', is_admin=False, password=None):
        if not mobile_number:
            raise ValueError('User must have a Mobile Number')
        user = self.model(
            mobile_number=mobile_number,
            name=name,
            role=role,
            is_admin=is_admin
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
        
    def create_superuser(self, mobile_number, name, is_admin=True, password=None):
        """
        Creates and saves a Superuser with the given email, name and password.
        """
        user = self.create_user(
            mobile_number=mobile_number,
            name=name,
            role="admin",
            password=password,
            is_admin=is_admin
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# Custom User Model.
class User(AbstractBaseUser):
    mobile_number = models.CharField(max_length=15, unique = True)
    email = models.EmailField(        
        max_length=255,
        blank=True,
        null=True
        
    )
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=50,blank=True, null=True,choices=[('student', 'Student'),('teacher', 'Teacher'),('admin', 'Admin')])
    is_active=models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS=['name', 'is_admin']

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    



class Teacher(models.Model):
    approved_as_teacher = models.BooleanField(default=False)
    
    user = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, null=True)
    fullName = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    phone_number = models.CharField(("Phone Number: "), max_length=20, blank=True, null=True,unique=True)
    current_location = models.TextField(("Current Location"), choices=[('in_dhaka', 'Inside Dhaka'),('in_gazipur','Inside Gazipur'),('others','Others')], blank=True, null=True)
    current_address = models.TextField(blank=True, null=True)
    university_name = models.CharField(("University"), max_length=100, blank=True, null=True)
    department = models.CharField(("Department"), max_length=50, blank=True, null=True)    
    current_education_year = models.CharField(("Current Education Year:"), max_length=50, choices=[('1st_year', '1st Year'),('2nd_year', '2nd Year'),('3rd_year', '3rd Year'),('4th_year', '4th Year'),('graduated', 'Graduated'),('post_graduation_running', 'Enrolled In Postgraduation studies'),], blank=True, null=True)
    fb_link = models.CharField(("Facebook Link"), max_length=300, blank=True, null=True)
    interested_teaching_area = models.CharField(("Interested Teaching Segments"), max_length=50, choices=[('polytechnic','Polytechnic'),('class_6_to_12','Class 6-12'),('duet_admission','DUET Admission'),], blank=True, null=True)
    interested_subjects = models.CharField(("Interested Subjects"), max_length=50, choices=[('non_department',"Non Department"),('department',"Department")], blank=True, null=True)

    link_previous_class = models.CharField(("Previous Class Link Live or Recorded"), max_length=200, blank=True, null=True)    
    experience = models.IntegerField(blank=True, null=True)
    describe_your_experience = models.TextField(blank=True, null=True)

    cv = models.FileField(upload_to='teacher_cv', max_length=150, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']        


class CourseCategory(models.Model):
    name = models.CharField(choices=course_type, max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.course_category


class Course(models.Model):
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    teacher=models.ManyToManyField(Teacher)
    

    def __str__(self) -> str:
        return self.title
    

class CourseDetails(models.Model):    
    course=models.OneToOneField(Course,on_delete=models.SET_NULL,blank=True,null=True)
    enrolled_student=models.IntegerField()
    duration = models.DurationField() #this time duration in  hours
    videos=models.IntegerField()
    quiz=models.IntegerField()
    classes=models.IntegerField()
    price = models.IntegerField(default=0)
    description = models.TextField()
    short_message = models.TextField()

    def __str__(self) -> str:
        return self.course + self.course_category

class StudentModel(models.Model):
    user = models.ForeignKey(User, verbose_name=("User"), on_delete=models.CASCADE)        
    name=models.CharField(max_length=20,blank=True, null=True)    
    mobile_number=models.CharField(max_length=20,blank=True, null=True)    
    email=models.EmailField(max_length=200,blank=True, null=True)

class EnrollmentModel(models.Model):

    student=models.ForeignKey(StudentModel,on_delete=models.CASCADE)
    course=models.ForeignKey(Course, on_delete=models.SET_NULL,null=True,blank=True)
    date=models.DateField(auto_now_add=True)
    status=models.CharField(max_length=150, choices=course_status)