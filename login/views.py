from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from django.db.models import Q
from login.form import LoginForm, RegisterForm, PropertyForm
from login.models import Property, PropertyImage


def login_view(request):
    """Handle user login with proper authentication"""
    if request.user.is_authenticated:
        return redirect('index1')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Create session
            messages.success(request, f'Welcome back, {user.username}! ✅')
            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('index1')
        else:
            messages.error(request, 'Invalid username or password. ❌')
    else:
        form = LoginForm()
    
    return render(request, 'login/loginpage.html', {'form': form, 'login_form': True})


def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


def register_view(request):
    """Handle user registration with password hashing"""
    if request.user.is_authenticated:
        return redirect('index1')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Automatically hashes password
            login(request, user)  # Auto-login after registration
            messages.success(request, 'Registration successful! Welcome! ✅')
            return redirect('index1')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = RegisterForm()
    
    return render(request, 'login/loginpage.html', {'form': form, 'register_form': True})


def index1(request):
    """Display home page - requires login"""
    # Get featured properties
    featured_properties = Property.objects.filter(is_available=True)[:6]
    context = {
        'user': request.user,
        'properties': featured_properties,
    }
    return render(request, 'login/index1.html', context)


@login_required(login_url='login')
def sale(request):
    """Display property posting page - requires login"""
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.seller = request.user
            property_obj.is_available = True
            property_obj.save()

            # Save image bytes directly into PostgreSQL—persists across Render restarts
            if 'images' in request.FILES:
                for image_file in request.FILES.getlist('images'):
                    try:
                        PropertyImage.objects.create(
                            property=property_obj,
                            image_data=image_file.read(),
                            content_type=image_file.content_type or 'image/jpeg',
                        )
                    except Exception:
                        pass  # skip on failure; property is already saved

            messages.success(request, f'Property posted successfully! 🎉 Your {property_obj.get_property_type_display()} in {property_obj.location} is now live.')
            return redirect('profile')  # PRG pattern—prevents double submit
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = PropertyForm()

    return render(request, 'login/sale.html', {'user': request.user, 'form': form})


def serve_property_image(request, image_id):
    """Serve a property image from bytes stored in the database."""
    img = get_object_or_404(PropertyImage, id=image_id)
    return HttpResponse(bytes(img.image_data), content_type=img.content_type)


def buy(request):
    """Display properties for purchase - requires login"""
    properties = Property.objects.filter(is_available=True)
    
    # Filter by property type if specified
    property_type = request.GET.get('type')
    if property_type:
        properties = properties.filter(property_type=property_type)
    
    # Filter by location if specified
    location = request.GET.get('location')
    if location:
        properties = properties.filter(location__icontains=location)
    
    # Filter by bedrooms if specified
    bedrooms = request.GET.get('bedrooms')
    if bedrooms:
        properties = properties.filter(bedrooms=bedrooms)
    
    # Filter by bathrooms if specified
    bathrooms = request.GET.get('bathrooms')
    if bathrooms:
        properties = properties.filter(bathrooms=bathrooms)
    
    # Filter by price range if specified
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        properties = properties.filter(price__gte=min_price)
    if max_price:
        properties = properties.filter(price__lte=max_price)
    
    # Search by keywords (location, description)
    search = request.GET.get('search')
    if search:
        properties = properties.filter(
            models.Q(location__icontains=search) | 
            models.Q(description__icontains=search)
        )
    
    # Get all unique locations from available properties (for filter dropdown)
    available_locations = Property.objects.filter(is_available=True).values_list('location', flat=True).distinct().order_by('location')
    
    context = {
        'properties': properties,
        'available_locations': available_locations,
        'user': request.user,
    }
    return render(request, 'login/buy.html', context)


@login_required(login_url='login')
def profile_view(request):
    """Display user profile with their properties"""
    user = request.user
    user_properties = Property.objects.filter(seller=user).order_by('-created_at')
    
    # Calculate statistics
    total_listings = user_properties.count()
    active_listings = user_properties.filter(is_available=True).count()
    total_value = sum(prop.price for prop in user_properties)
    
    context = {
        'user': user,
        'properties': user_properties,
        'total_listings': total_listings,
        'active_listings': active_listings,
        'total_value': total_value,
    }
    return render(request, 'login/profile.html', context)


@login_required(login_url='login')
def edit_profile_view(request):
    """Edit user profile"""
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        messages.success(request, 'Profile updated successfully! ✅')
        return redirect('profile')
    
    return render(request, 'login/edit_profile.html', {'user': request.user})


def property_detail_view(request, property_id):
    """Display detailed view of a single property.
    The property owner can always view it; others only see available ones.
    """
    try:
        property_obj = Property.objects.get(id=property_id)
        # Non-owners can only see available properties
        if not property_obj.is_available:
            if not request.user.is_authenticated or request.user != property_obj.seller:
                messages.error(request, 'Property not found or no longer available.')
                return redirect('buy')
    except Property.DoesNotExist:
        messages.error(request, 'Property not found or no longer available.')
        return redirect('buy')

    images = property_obj.images.all()

    context = {
        'property': property_obj,
        'images': images,
        'seller': property_obj.seller,
    }
    return render(request, 'login/property_detail.html', context)


@login_required(login_url='login')
def delete_property(request, property_id):
    """Delete a property listing — only the owner can do this."""
    property_obj = get_object_or_404(Property, id=property_id, seller=request.user)
    if request.method == 'POST':
        property_obj.delete()
        messages.success(request, 'Property deleted successfully.')
    return redirect('profile')