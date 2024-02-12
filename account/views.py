from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account.models import User,Teacher,StudentModel,EnrollmentModel
from account.models import CourseCategory,Course
from rest_framework_simplejwt.tokens import RefreshToken
from account.renderers import UserRenderer
from account.serializers import UserRegistrationSerializer,UserLoginSerializer,TeacherRegistrationSerializer,StudentSerializer, EnrollmentModelSerializer,UserSerializer
from django.contrib.auth import authenticate
from .serializers import TeacherSerializer,CategorySerializer,StudentUserSerializer,ApprovedTeacherSerializer,AdminSerializer, CourseSerializer
from rest_framework.generics import get_object_or_404, ListCreateAPIView, RetrieveUpdateDestroyAPIView,ListAPIView
from rest_framework.permissions import AllowAny, IsAdminUser,IsAuthenticated
# Create your views here.

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

#user registration as a student
class UserRegistration(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format= None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token, 'user':UserSerializer(user).data, 'message':'Registration Successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# user login view
class UserLogin(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, *args, **kwargs):        
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            mobile_number = serializer.data.get('mobile_number')
            password = serializer.data.get('password')
            user = authenticate(request, mobile_number=mobile_number, password=password)
            
            token = get_tokens_for_user(user)            
            if user is not None:
                return Response({'token':token, 'user':UserSerializer(user).data, "msg": 'Login Successful'},status=status.HTTP_200_OK)
            else:
                print("user is not present")
                return Response({'errors':'Your credentials are not valid'}, status=status.HTTP_400_BAD_REQUEST)
                    
        else:
            print("serializer error: ",serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# retrieve all users who are students
class StudentUserListView(ListAPIView):
    queryset = User.objects.filter(role='student')
    serializer_class = StudentUserSerializer

# retrieve all users who are teachers
class TeacherUserListView(ListAPIView):
    queryset = User.objects.filter(role='teacher')
    serializer_class = ApprovedTeacherSerializer

# retrieve all users who are admin
class AdminListView(ListAPIView):
    queryset = User.objects.filter(role='admin')
    serializer_class = AdminSerializer


# Teacher views
class TeacherListCreateView(ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class TeacherRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

  

class TeacherApproveView(APIView):    
    def get(self, request, pk):
        print("view called with pk: ", pk)
        teacher = get_object_or_404(Teacher, pk=pk)    

        # create a user instance
        user_data = {
             'mobile_number': teacher.phone_number,
            'name': teacher.fullName,
            'is_admin': False,
            "role":'teacher',
            "password": teacher.phone_number,
            "password2":teacher.phone_number,
        }

        user_serializer = TeacherRegistrationSerializer(data=user_data)        
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        # create instance of Teacher Model
        teacher_model_data = {
            'user':user.id
        }

        teacher.approved_as_teacher = True
        teacher.user= user
        teacher.save()

        return Response({
            "message":"successfully approved Teacher"
            # 'user':UserRegistration(user).data, 'teacher': TeacherSerialize(teacher).data
        }, status=status.HTTP_201_CREATED)


# retrieve Student from student model
class SingleStudent(APIView):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        student = StudentModel.objects.filter(user=user).first()
        serializer = StudentSerializer(instance=student)        
        return Response({'student': serializer.data}, status=status.HTTP_200_OK)


# retrieve Teacher from Teacher model
class SingleTeacher(APIView):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        teacher = Teacher.objects.filter(user=user).first()
        serializer = TeacherSerializer(instance=teacher)    
        return Response({'teacher': serializer.data}, status=status.HTTP_200_OK)



# Course Category views 
class CategoryListCreateView(ListCreateAPIView):
    queryset = CourseCategory.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class CategoryRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = CourseCategory.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class CourseListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class TeacherWiseCourses(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(pk=teacher_id)
        courses = Course.objects.filter(teacher=teacher)
        serializer = CourseSerializer(instance=courses, many=True)        
        return Response({'courses': serializer.data}, status=status.HTTP_200_OK)


class EnrollmentModelView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, student_id=None):
        if student_id:
            student = StudentModel.objects.get(pk=student_id)
            enrollments = EnrollmentModel.objects.filter(student=student)
            serializer = EnrollmentModelSerializer(enrollments, many=True)
            return Response({'student_courses':serializer.data}, status=status.HTTP_200_OK)
        else:
            enrollments = EnrollmentModel.objects.all()
            serializer = EnrollmentModelSerializer(enrollments, many=True)
            return Response(serializer.data)

    def post(self, request,):
        serializer = EnrollmentModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
