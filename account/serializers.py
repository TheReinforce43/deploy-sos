from rest_framework import serializers
from account.models import User,Teacher,CourseCategory,Course,StudentModel,EnrollmentModel

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'},write_only=True)

    class Meta:
        model = User
        fields =  ['id','mobile_number','name', 'password', 'password2']
        extra_kwargs = {'password':{'write_only':True}}

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError("Password and confirm password does not match")
        return attrs
    
    def create(self, validate_data):
        validate_data.pop('password2', None)
        user = User.objects.create_user(**validate_data)

        # create the student model
        StudentModel.objects.create(
            user=user,
            name=user.name,
            mobile_number=user.mobile_number,
            email = user.email
        )

        return user


class TeacherRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'},write_only=True)

    class Meta:
        model = User
        fields =  ['mobile_number','name', 'password', 'password2']
        extra_kwargs = {'password':{'write_only':True}}

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError("Password and confirm password does not match")
        return attrs
    
    def create(self, validate_data):
        validate_data.pop('password2', None)
        return User.objects.create_teacher(**validate_data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','mobile_number','email','name','role','created_at','updated_at']
    
class UserLoginSerializer(serializers.ModelSerializer):
    mobile_number = serializers.CharField(max_length=20)
    class Meta:
        model = User
        fields = ['id','mobile_number', 'password']


class StudentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'mobile_number', 'email', 'name', 'role', 'created_at', 'updated_at']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentModel
        fields = "__all__"

    

class ApprovedTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'mobile_number', 'email', 'name', 'role', 'created_at', 'updated_at']

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'mobile_number', 'email', 'name', 'role', 'created_at', 'updated_at']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','mobile_number','name','role']
    

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model= Teacher
        fields = "__all__"



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class EnrollmentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrollmentModel
        fields = '__all__'
    
