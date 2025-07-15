from django.shortcuts import redirect, render, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from PIL import Image, ImageTk, ImageEnhance, ImageOps, ImageFilter
from io import BytesIO
from django.core.files.base import ContentFile
import random
from django.conf import settings

from .models import InputImage
from .form import ImageForm
import os

# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

def signup(request):

    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            return render(request, "authentication/inpErr.html")
        else:
            myuser = User.objects.create_user(username, email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname

            myuser.save()
            messages.success(request, "Your account has been successsfully created.")

            return redirect('signin')

    return render(request, "authentication/signup.html")

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
    
        user = authenticate(username=username, password=pass1)
    
        if user is not None:
            login(request, user)
            fname = user.first_name
            return redirect('main')

        else:
            return render(request, "authentication/inpErr.html")

    return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('home')

def main(request):
    return render(request, "authentication\main.html")

def grayscale(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')

        if form.is_valid():
            images = request.FILES.getlist('image')  # Get the list of uploaded images

            augmented_images = []  # To store the augmented images and their URLs

            for uploaded_image in files:
                obj = form.save(commit=False)
                obj.image = uploaded_image  # Set the current image
                image = Image.open(uploaded_image)

                # Convert the image to grayscale
                gray_image = image.convert('L')

                # Apply random brightness level to grayscale image
                grayscale_level = random.uniform(0.5, 1.5)
                enhanced_gray_image = ImageEnhance.Brightness(gray_image).enhance(grayscale_level)

                # Save the augmented image
                grayscale_image_io = BytesIO()
                enhanced_gray_image.save(grayscale_image_io, format='JPEG')
                
                image_name = f"{uploaded_image.name.split('.')[0]}_GRAY.jpeg"
                obj.augmented_image.save(image_name, ContentFile(grayscale_image_io.getvalue()), save=False)
                

                # Store the URL of the augmented image to render later
                augmented_images.append(obj.augmented_image.url)

            obj.save()

            return render(request, "authentication/main.html", {"obj":obj, "augmented_image_url": obj.augmented_image.url})

    else:
        form = ImageForm()

    return render(request, "authentication/main.html", {"form": form})


def verticalFlip(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')  # Get all uploaded files

        flipped_images = []  # To store the URLs of flipped images

        for uploaded_image in files:
            obj = form.save(commit=False)

            obj.image = uploaded_image  # Set the current image
            image = Image.open(uploaded_image)

            # Perform vertical flip
            flipped_image = image.transpose(Image.FLIP_TOP_BOTTOM)

            if flipped_image.mode in ("RGBA", "LA"):
                flipped_image = flipped_image.convert("RGB")

            image_name = f"{uploaded_image.name.split('.')[0]}_flipped.jpeg"


            # Save the flipped image
            flipped_image_io = BytesIO()
            flipped_image.save(flipped_image_io, format='JPEG')

            obj.augmented_image.save(image_name, ContentFile(flipped_image_io.getvalue()), save=False)

            # Save the object (each image)
            obj.save()

            # Store the URL of the flipped image to display later
            flipped_images.append(obj.augmented_image.url)

        # Render the results, passing the list of flipped images
        return render(request, "authentication/main.html", {"obj":obj, "augmented_image_url": obj.augmented_image.url})

    else:
        form = ImageForm()

    return render(request, "authentication/main.html", {"form": form})


def horizontalFlip(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')  # Get all uploaded files

        flipped_images = []  # To store the URLs of flipped images

        for uploaded_image in files:
            obj = form.save(commit=False)

            obj.image = uploaded_image  # Set the current image
            image = Image.open(uploaded_image)

            # Perform vertical flip
            flipped_image = image.transpose(Image.FLIP_LEFT_RIGHT)

            image_name = f"{uploaded_image.name.split('.')[0]}_h-flipped.jpeg"


            # Save the flipped image
            flipped_image_io = BytesIO()
            flipped_image.save(flipped_image_io, format='JPEG')

            obj.augmented_image.save(image_name, ContentFile(flipped_image_io.getvalue()), save=False)

            # Save the object (each image)
            obj.save()

            # Store the URL of the flipped image to display later
            flipped_images.append(obj.augmented_image.url)

        # Render the results, passing the list of flipped images
        return render(request, "authentication/main.html", {"obj":obj, "augmented_image_url": obj.augmented_image.url})

    else:
        form = ImageForm()

    return render(request, "authentication/main.html", {"form": form})

def rotate(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')
        for uploaded_image in files:
            obj = form.save(commit=False)

            obj.image = uploaded_image  # Set the current image
            image = Image.open(uploaded_image)
            if image.mode in ("RGBA", "LA"):
                    image = image.convert("RGB")

            rotated_images = []

            
            for i in range(359):  # Loop 359 times to create 359 rotated images
                rotated_image = image.rotate(i, expand=True)  # Rotate the image by i degrees
            
                # Generate a unique image name for each rotated image
                image_name = f"{uploaded_image.name.split('.')[0]}_rotated_{i}.jpeg"
            
                rotated_image_io = BytesIO()
                rotated_image.save(rotated_image_io, format='JPEG')

                
            
                # No need to provide the full path here, Django handles it
                obj.augmented_image.save(image_name, ContentFile(rotated_image_io.getvalue()), save=False)
            
                # Store the URL of each rotated image to render later
                rotated_images.append(obj.augmented_image.url)


            obj.save()

            return render(request, "authentication/main.html", {"obj":obj, "augmented_image_url": obj.augmented_image.url})

    else:
        form = ImageForm()

    return render(request, "authentication/main.html", {"form": form})


def apply_random_color_filter(image):
    
    enhancer = ImageEnhance.Color(image)
    red_factor = random.uniform(0.5, 1.5)
    green_factor = random.uniform(0.5, 1.5)
    blue_factor = random.uniform(0.5, 1.5)
    filtered_image = enhancer.enhance(red_factor)
    filtered_image = ImageEnhance.Color(filtered_image).enhance(green_factor)
    filtered_image = ImageEnhance.Color(filtered_image).enhance(blue_factor)
    return filtered_image

def filter(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            uploaded_image = obj.image

            
            image = Image.open(uploaded_image)

            
            filtered_image = apply_random_color_filter(image)

            
            original_image_io = BytesIO()
            image.save(original_image_io, format='JPEG')
            obj.original_image.save(uploaded_image.name, ContentFile(original_image_io.getvalue()), save=False)

            
            filtered_image_io = BytesIO()
            filtered_image.save(filtered_image_io, format='JPEG')
            obj.augmented_image.save(uploaded_image.name, ContentFile(filtered_image_io.getvalue()), save=False)

            obj.save()

            return render(request, "authentication/main.html", {"obj": obj, "augmented_image_url": obj.augmented_image.url})

    else:
        form = ImageForm()

    return render(request, "authentication/main.html", {"form": form})


def random_crop(image, crop_width, crop_height):
    original_width, original_height = image.size

    # Ensure crop dimensions fit within the original image dimensions
    if crop_width > original_width or crop_height > original_height:
        raise ValueError("Crop dimensions exceed original image dimensions")

    max_x = original_width - crop_width
    max_y = original_height - crop_height

    # Random position for cropping
    x = random.randint(0, max_x)
    y = random.randint(0, max_y)

    # Perform the crop
    cropped_image = image.crop((x, y, x + crop_width, y + crop_height))

    return cropped_image

def crop(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            uploaded_image = obj.image

            # Open and convert the uploaded image to RGB immediately
            image = Image.open(uploaded_image)
            if image.mode in ("RGBA", "LA"):
                image = image.convert("RGB")

            # Define crop dimensions
            crop_width = 100  
            crop_height = 100

            # Perform random cropping
            cropped_image = random_crop(image, crop_width, crop_height)

            # Save the original image in a buffer
            original_image_io = BytesIO()
            image.save(original_image_io, format='JPEG')
            obj.original_image.save(
                uploaded_image.name,
                ContentFile(original_image_io.getvalue()),
                save=False
            )

            # Save the cropped image in a buffer
            cropped_image_io = BytesIO()
            cropped_image.save(cropped_image_io, format='JPEG')
            obj.augmented_image.save(
                uploaded_image.name,
                ContentFile(cropped_image_io.getvalue()),
                save=False
            )

            obj.save()

            return render(request, "authentication/main.html", {"obj": obj, "augmented_image_url": obj.augmented_image.url})

    else:
        form = ImageForm()

    return render(request, "authentication/main.html", {"form": form})
