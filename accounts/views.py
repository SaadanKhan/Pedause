from rest_framework.views import APIView
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token 
from .utils import *
from django.contrib.auth import login, logout
from django.utils import timezone
import random


class UserSignup(APIView):
    def post(self, request):
        try:
            serializer = CustomUserSerializer(data=request.data)
            if serializer.is_valid():                    
                serializer.save()

                return Response({
                    'success': True,
                    'message': 'Account Created Successfully',
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({
                'success': False,
                'message': serializer.errors,
                }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    def post(self, request):
        try:
            phone = request.data['phone']
            user_against_phone = CustomUser.objects.filter(phone=phone).first()

            print(user_against_phone)
            
            if user_against_phone:
                user_otp = random.randint(1111,9999)
                user_against_phone.otp = user_otp
                user_against_phone.otp_created_at = timezone.now()
                user_against_phone.save()

                send_message(user_otp, phone)

                return Response({
                   'success': True,
                   'account verified': user_against_phone.is_verified,
                   'message': 'OTP has been sent to your device',
                   'OTP': user_otp
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            else:
                user_otp = random.randint(1111,9999)
                new_user = CustomUser.objects.create(
                    otp = user_otp,
                    otp_created_at = timezone.now()
                )

                send_message(user_otp, phone)
                
                return Response({
                   'success': True,
                   'account verified': new_user.is_verified,
                   'message': 'Account created, OTP has been sent to your device',
                   'OTP': user_otp
                    }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
                return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTP(APIView):
    def post(self, request):
        try:
            otp = request.data['otp']
            user_against_otp = CustomUser.objects.filter(otp=otp).first()

            if user_against_otp:
                if is_valid_otp(user_against_otp) == True:
                    user_against_otp.is_verified = True
                    user_against_otp.save()
                    login(request, user_against_otp)

                    token, created = Token.objects.get_or_create(user=user_against_otp)
                    return Response({
                        'success': True,
                        'token': token.key,
                        'message': 'Verification Successful',
                        }, status=status.HTTP_200_OK)
                
                else:
                    return Response({
                       'success': False,
                       'message': 'OTP Expired',
                        }, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({
                   'success': False,
                   'message': 'Invalid OTP',
                    }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
                return Response({
                    'success': False,
                    'message': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)


class UserLogout(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.auth.delete()
            logout(request)

            return Response({
                'success': True,
                'message': 'Logout successful',
            }, status=status.HTTP_200_OK)
         
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST) 


class CreateUserProfile(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def patch(self, request):
        try:

            # You can't update your email address
            user_email = request.data.get('email', None)
            if user_email is not None:
                return Response({
                    'success': False,
                    'message': 'You cannot update your email address',
                }, status=status.HTTP_400_BAD_REQUEST)
                
            # You can't update your password from here
            user_password = request.data.get('password', None)
            if user_password is not None:
                return Response({
                    'success': False,
                    'message': 'You cannot update your password',
                }, status=status.HTTP_400_BAD_REQUEST)
            

            request_user = request.user
            user = CustomUser.objects.filter(email = request_user).first()

            if user:
                serializer = CustomUserSerializer(user, data=request.data, partial=True)
                
                if serializer.is_valid():
                    serializer.save()

                    return Response({
                        'success': True,
                        'message': 'Profile updated successfully',
                        'data': {
                            'user': serializer.data
                        },
                    }, status=status.HTTP_200_OK)

                return Response({
                    'success': False,
                    'message': 'Invalid data',
                    'errors': serializer.errors,
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                'success': False,
                'message': 'User does not exist',
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'success': False,
                'message': 'Error while updating',
                'error_detail': str(e),
            }, status=status.HTTP_400_BAD_REQUEST)


class UserSocialLogin(APIView):
    def post(self, request):
        try:
            user_apple_id = request.data.get('apple_id')
            user_name = request.data.get('name')
            user_phone = request.data.get('phone')
            user_acc_type = request.data.get('type')
            user_email = request.data.get('email')

            user_apple_id = user_apple_id if user_apple_id is not None else ""
            user_name = user_name if user_name is not None else ""
            user_phone = user_phone if user_phone is not None else ""
            user_acc_type = user_acc_type if user_acc_type is not None else ""
            user_email = user_email if user_email is not None else ""

            # initial check if email address exists or not
            if user_email:
                custom_user = CustomUser.objects.filter(email=user_email).first()
                social_user = SocialAccount.objects.filter(email = user_email).first()

                if custom_user and not social_user:
                    return Response({
                        'success': False,
                        'message': 'Account already exists',
                    },
                    status= status.HTTP_400_BAD_REQUEST)
                
            else:
                user_email = 'NotAnyEmail'

            if user_apple_id or user_email or user_phone:
                try:
                    social_user = SocialAccount.objects.get(email=user_email)
                except SocialAccount.DoesNotExist:
                    social_user = SocialAccount.objects.filter(apple_id=user_apple_id, apple_id__isnull=False).first()

                # If account exists
                if social_user is not None:

                    # For Google
                    if user_acc_type == 'google':
                        if user_email:
                            
                            user_obj = CustomUser.objects.filter(email=user_email).first()
                            user = SocialAccount.objects.filter(email=user_email).first()

                            print('.......')

                            if user.type == 'google':
                                
                                login(request, user_obj)

                                token, created = Token.objects.get_or_create(user=user_obj)
                                user_serializer = CustomUserSerializer(user_obj)

                                return Response({
                                    'success': True,
                                    'message': 'Login Success',
                                    'data': { 
                                        'token': token.key,
                                        'user': user_serializer.data,
                                        }
                                }, status=status.HTTP_200_OK)
                            
                            return Response({
                                'success': False,
                                'message': 'Not registered with this account',
                            }, status=status.HTTP_400_BAD_REQUEST) 
                        
                        return Response({
                                'success': False,
                                'message': 'Please enter your email',
                            }, status=status.HTTP_400_BAD_REQUEST)
                    
                    # For Apple
                    if user_acc_type == 'apple':
                        user = SocialAccount.objects.filter(apple_id=user_apple_id).first()
                        if user is not None:
                            user_obj = CustomUser.objects.filter(email=user.email).first()

                            if user.type == 'apple':
                                login(request, user_obj)

                                token, created = Token.objects.get_or_create(user=user_obj)
                                user_serializer = CustomUserSerializer(user_obj)

                                return Response({
                                    'success': True,
                                    'message': 'Login Success',
                                    'data': { 
                                        'token': token.key,
                                        'user': user_serializer.data,
                                        }
                                }, status=status.HTTP_200_OK)
                            
                            return Response({
                                'success': False,
                                'message': 'Not registered with this account',
                            }, status=status.HTTP_400_BAD_REQUEST) 
                        
                        return Response({
                            'success': False,
                            'message': 'Invalid apple id',
                        }, status=status.HTTP_400_BAD_REQUEST) 

                    # For Facebook
                    if user_acc_type == 'facebook':
                        user = SocialAccount.objects.filter(phone=user_phone).first()
                        if user is not None:
                            user_obj = CustomUser.objects.filter(email=user.email).first()

                            if user.type == 'facebook':
                                login(request, user_obj)

                                token, created = Token.objects.get_or_create(user=user_obj)
                                user_serializer = CustomUserSerializer(user_obj)

                                return Response({
                                    'success': True,
                                    'message': 'Login Success',
                                    'data': { 
                                        'token': token.key,
                                        'user': user_serializer.data,
                                        }
                                }, status=status.HTTP_200_OK)
                            
                            return Response({
                                'success': False,
                                'message': 'Not registered with this account',
                            }, status=status.HTTP_400_BAD_REQUEST) 
                        
                        return Response({
                            'success': False,
                            'message': 'Invalid apple id',
                        }, status=status.HTTP_400_BAD_REQUEST) 


                # If account does not exist, then create
                else:
                    
                    # If account type is Google
                    if user_acc_type == 'google':
                        # Create a new google account
                        if user_email and user_name and user_acc_type:
                            try:
                                serializer = SocialAccountSerializer(data=request.data)
                                user = SocialAccount.objects.filter(email=user_email).first()

                                if serializer.is_valid():
                                    serializer.save()

                                    login(request, user)

                                    token, created = Token.objects.get_or_create(user=user)
                                    user_serializer = CustomUserSerializer(user)

                                    return Response({
                                        'success': True,
                                        'message': 'Created a social account successfully',
                                        'data': { 
                                            'token': token.key,
                                            'user': user_serializer.data,
                                            }
                                    }, status=status.HTTP_200_OK)


                                return Response({
                                        'success': False,
                                        'message': 'Unable to create a new social account',
                                    },
                                    status= status.HTTP_400_BAD_REQUEST)
                            
                            except Exception as e:
                                return Response({
                                        'success': False,
                                        'message': str(e),
                                    },
                                    status= status.HTTP_400_BAD_REQUEST)
                            
                        else:
                            return Response({
                                    'success': False,
                                    'message': 'name, account type and email required',
                                },
                                status= status.HTTP_400_BAD_REQUEST)                       
                    
                    # If account type is Apple
                    if user_acc_type == 'apple':
                        # Create a new apple account
                        if user_email and user_name and user_acc_type and user_apple_id:
                            try:
                                serializer = SocialAccountSerializer(data=request.data)
                                user = SocialAccount.objects.filter(email=user_email).first()

                                if serializer.is_valid():
                                    serializer.save()

                                    login(request, user)

                                    token, created = Token.objects.get_or_create(user=user)
                                    user_serializer = CustomUserSerializer(user)

                                    return Response({
                                        'success': True,
                                        'message': 'Created a social account successfully',
                                        'data': { 
                                            'token': token.key,
                                            'user': user_serializer.data
                                            }
                                    }, status=status.HTTP_200_OK)


                                return Response({
                                        'success': False,
                                        'message': serializer.errors,
                                    },
                                    status= status.HTTP_400_BAD_REQUEST)
                            
                            except Exception as e:
                                return Response({
                                        'success': False,
                                        'message': str(e),
                                    },
                                    status= status.HTTP_400_BAD_REQUEST)
                            
                        else:
                            return Response({
                                    'success': False,
                                    'message': 'name, account type, email and apple id required',
                                },
                                status= status.HTTP_400_BAD_REQUEST)                       

                    # If account type is Facebook
                    if user_acc_type == 'facebook':
                        # Create a new apple account
                        if user_email and user_name and user_acc_type and user_phone:
                            try:
                                serializer = SocialAccountSerializer(data=request.data)
                                user = SocialAccount.objects.filter(phone=user_phone).first()

                                if serializer.is_valid():
                                    serializer.save()

                                    login(request, user)

                                    token, created = Token.objects.get_or_create(user=user)
                                    user_serializer = CustomUserSerializer(user)

                                    return Response({
                                        'success': True,
                                        'message': 'Created a social account successfully',
                                        'data': { 
                                            'token': token.key,
                                            'user': user_serializer.data
                                            }
                                    }, status=status.HTTP_200_OK)


                                return Response({
                                        'success': False,
                                        'message': 'Unable to create a new social account',
                                    },
                                    status= status.HTTP_400_BAD_REQUEST)
                            
                            except Exception as e:
                                return Response({
                                        'success': False,
                                        'message': str(e),
                                    },
                                    status= status.HTTP_400_BAD_REQUEST)
                            
                        else:
                            return Response({
                                    'success': False,
                                    'message': 'name, account type, email and phone required',
                                },
                                status= status.HTTP_400_BAD_REQUEST)                       

            return Response({
                'success': False,
                'message': 'Apple id, Email or Phone required ',
            },
            status= status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
                return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


