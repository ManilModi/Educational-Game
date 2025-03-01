from django.shortcuts import render, redirect
from django.shortcuts import (get_object_or_404, render, HttpResponseRedirect)
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth import login, logout,authenticate
from django.contrib import messages
from .forms import LoginForm, UserRegistrationForm,AdminUserCreationForm
from .forms import LoginForm, UserRegistrationForm,AdminUserCreationForm,PasswordChangeForm, DeleteUserForm
from .forms import PasswordChangeForm, generate_random_password
from django.core.mail import send_mail
from .models import Userstable, Roles,UserRole
from .decorators import role_required
import os
import folium
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from django.conf import settings
import plotly.graph_objects as go
import plotly.io as pio
from datetime import datetime, timedelta
import xgboost as xgb

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                user = Userstable.objects.get(username=username)

                if user.password == password:  # (Consider hashing passwords)
                    # Fetch the user's role
                    user_role = UserRole.objects.get(user=user)
                    role_name = user_role.role.role_names  # Get the role name

                    # Store in session
                    request.session['user_id'] = user.id
                    request.session['user_role'] = role_name


                    if role_name == "Admin":
                        return redirect('admin_dashboard')
                    elif role_name == "Government Engineer":
                        return redirect('govt_dashboard')
                    elif role_name == "Normal User":
                        return redirect('normal_dashboard')
                else:
                    messages.error(request, "Invalid credentials")
            except Userstable.DoesNotExist:
                messages.error(request, "User does not exist")
            except UserRole.DoesNotExist:
                messages.error(request, "User role not assigned")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form}) 

# User Logout View
def user_logout(request):
    request.session.flush()  # Clear session
    return redirect('login')

def about(request):
    return render(request, 'about.html') 

# Dashboard Views
@role_required(allowed_roles=['Admin'])
def admin_dashboard(request):
    if 'user_id' not in request.session:
        return redirect('login')  # Force login if not authenticated
    return render(request, 'admin_dashboard.html')

@role_required(allowed_roles=['Government Engineer'])
def govt_dashboard(request):
    if 'user_id' not in request.session:
        return redirect('login')  # Force login if not authenticated
    return render(request, 'govt_dashboard.html')

@role_required(allowed_roles=['Normal User'])
def normal_dashboard(request):
    if 'user_id' not in request.session:
        return redirect('login')  # Force login if not authenticated
    return render(request, 'normal_dashboard.html')

@role_required(allowed_roles=['Entrepreneur'])
def entrepreneur_dashboard(request):
    if 'user_id' not in request.session:
        return redirect('login')  # Force login if not authenticated
    return render(request, 'entrepreneur_dashboard.html')

@role_required(allowed_roles=['Researcher'])
def researcher_dashboard(request):
    if 'user_id' not in request.session:
        return redirect('login')  # Force login if not authenticated
    return render(request, 'researcher_dashboard.html')

def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # messages.success(request, "Account created successfully!")
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

def creatRroles(request):
    roles = ['Normal User', 'Entrepreneur', 'Researcher', 'Government Engineer', 'Admin']
    for role in roles:
        Roles.objects.get_or_create(role_names=role)
    return HttpResponse("<h1>Roles created successfully<h1>")


# Admin-Only View to Create Admin & Govt. Engineers
@role_required(allowed_roles=['Admin'])
def admin_create_user(request):
    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # messages.success(request, "Admin/Govt. Engineer account created! Credentials sent via email.")
            return redirect('admin_dashboard')
    else:
        form = AdminUserCreationForm()

    return render(request, 'admin_create_user.html', {'form': form})

def unauthorized_access(request):
    return render(request, 'unauthorized.html')  # Create unauthorized.html template

@role_required(allowed_roles=['Admin'])
def update_credential(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']

            try:
                user = Userstable.objects.get(username=username)

                # Generate a random password
                new_password = generate_random_password()

                # Update password in plain text as per your requirement
                user.password = new_password
                user.save()

                # Send the new password via email (only if Admin/Gov Engineer)
                send_mail(
                    subject='Your Password Has Been Updated',
                    message=f'Your new password is: {new_password}',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[username],  # Using username as email
                    fail_silently=False,
                )

                messages.success(request, f'Password updated and emailed to {username}')
                return redirect('admin_dashboard')

            except Userstable.DoesNotExist:
                messages.error(request, 'User not found.')

    else:
        form = PasswordChangeForm()

    return render(request, 'change_password.html', {'form': form})

@role_required(allowed_roles=['Admin'])
def delete_user(request):
    if request.method == 'POST':
        form = DeleteUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']

            try:
                user = Userstable.objects.get(username=username)
                
                user_email = user.username

                user.delete()

                send_mail(
                    subject='Your Account Has Been Deleted',
                    message='Your account has been removed by the administrator.',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user_email],
                    fail_silently=False,
                )

                messages.success(request, f'User {username} has been deleted.')
                return redirect('admin_dashboard')

            except Userstable.DoesNotExist:
                messages.error(request, 'User not found.')

    else:
        form = DeleteUserForm()

    return render(request, 'delete_user.html', {'form': form})

def p_home(request):
    return render(request, "index_p.html")


@role_required(allowed_roles=['Admin', 'Government Engineer', 'Researcher', 'Entrepreneur'])
def residential_clusters(request):

    data_path = os.path.join(settings.BASE_DIR, 'myapp', 'data')
    tdf = pd.read_csv(os.path.join(data_path, 'ResidentialAreas_Here_Final.csv'))
    rdf = pd.read_csv(os.path.join(data_path, 'ResidentialAreasNeighbourhood_Here_Final.csv'))

    X = np.array(rdf.drop(['lat', 'lon'], axis=1))

    pca = PCA(n_components=3)
    X_pca = pca.fit_transform(X)

    optimal_clusters = 3
    kmeans = KMeans(n_clusters=optimal_clusters, init='k-means++', max_iter=1000, n_init=125, random_state=0)
    y_kmeans = kmeans.fit_predict(X_pca)
    rdf['cluster'] = y_kmeans

    # Define cluster labels and colors
    cluster_info = {
        0: {'color': 'red', 'label': 'High Electricity Demand'},
        1: {'color': 'orange', 'label': 'Medium Electricity Demand'},
        2: {'color': 'green', 'label': 'Low Electricity Demand'}
    }

    this_map = folium.Map(prefer_canvas=True)
    mapping = {tuple(xy): name for name, xy in zip(tdf['name'], zip(tdf['lat'], tdf['lon']))}

    for _, row in rdf.iterrows():
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=2,
            weight=5,
            color=cluster_info[row['cluster']]['color'],
            popup=mapping.get((row['lat'], row['lon']), "Unknown Location")
        ).add_to(this_map)

    this_map.fit_bounds(this_map.get_bounds())

    # Adding a legend to the map
    legend_html = '''
     <div style="position: fixed; 
                 bottom: 50px; left: 50px; width: 250px; height: 120px; 
                 background-color: white; z-index:9999; padding: 10px;
                 border-radius: 10px; box-shadow: 2px 2px 6px rgba(0,0,0,0.3);">
     <h4>Cluster Legend</h4>
     <p style="margin: 0;"><span style="color:red; font-weight:bold;">●</span> High Electricity Demand</p>
     <p style="margin: 0;"><span style="color:orange; font-weight:bold;">●</span> Medium Electricity Demand</p>
     <p style="margin: 0;"><span style="color:green; font-weight:bold;">●</span> Low Electricity Demand</p>
     </div>
    '''
    
    this_map.get_root().html.add_child(folium.Element(legend_html))

    map_html = this_map._repr_html_()

    return render(request, 'residential_clusters.html', {'map_html': map_html, 'cluster_info': cluster_info})




@role_required(allowed_roles=['Admin', 'Government Engineer', 'Normal User', 'Researcher', 'Entrepreneur'])
def electricity_demand_plot(request):
    dataset_path = os.path.join(os.path.dirname(__file__), 'data', 'dummy_electricity_data.csv')

    if not os.path.exists(dataset_path):
        return render(request, 'electricity_demand_hourly.html', {'error': 'Dataset not found!'})

    # Load dataset with exception handling
    try:
        df = pd.read_csv(dataset_path, parse_dates=['timestamp'])
    except Exception as e:
        return render(request, 'electricity_demand_hourly.html', {'error': f'Error loading dataset: {str(e)}'})

    # Get selected date from request
    selected_date = request.GET.get('date', '2023-01-01')

    try:
        selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
    except ValueError:
        return render(request, 'electricity_demand_hourly.html', {'error': 'Invalid date format! Use YYYY-MM-DD.'})

    # Filter dataset for the selected date
    df_day = df[df['timestamp'].dt.date == selected_date]

    if df_day.empty:
        return render(request, 'electricity_demand_hourly.html', {'error': 'No data found for the selected date!'})

    # Select only required columns
    df_selected = df_day[['timestamp', 'electricity_demand', 'solar_generation']].copy()
    df_table_html = df_selected.to_html(classes="table table-striped table-dark", index=False)

    # Identify peak and lowest electricity demand points
    peak_point = df_day.loc[df_day['electricity_demand'].idxmax()]
    lowest_point = df_day.loc[df_day['electricity_demand'].idxmin()]

    # Create a Plotly figure
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_day['timestamp'], y=df_day['electricity_demand'],
        mode='lines+markers', name='Electricity Demand',
        line=dict(color='purple'),
        marker=dict(size=4)
    ))

    fig.add_trace(go.Scatter(
        x=[peak_point['timestamp'], lowest_point['timestamp']],
        y=[peak_point['electricity_demand'], lowest_point['electricity_demand']],
        mode="markers",
        marker=dict(color='red', size=10, symbol='circle'),
        name="Highlighted Points"
    ))

    fig.add_annotation(
        x=peak_point['timestamp'], y=peak_point['electricity_demand'],
        text=f"Peak: {peak_point['electricity_demand']:.2f}",
        showarrow=True, arrowhead=2, ax=30, ay=-40, bgcolor="yellow"
    )

    fig.add_annotation(
        x=lowest_point['timestamp'], y=lowest_point['electricity_demand'],
        text=f"Lowest: {lowest_point['electricity_demand']:.2f}",
        showarrow=True, arrowhead=2, ax=-30, ay=40, bgcolor="lightgreen"
    )

    fig.update_xaxes(
        tickformat="%H:%M",
        tickangle=45
    )

    fig.update_layout(
        title=f"Electricity Demand for {selected_date}",
        xaxis_title="Time of Day",
        yaxis_title="Electricity Demand",
        template="plotly_white",
        width=1200,
        height=500
    )

    graph_html = pio.to_html(fig, full_html=False)

    return render(request, 'electricity_demand_hourly.html', {
        'plot_div': graph_html,
        'df_table_html': df_table_html,
        'selected_date': selected_date
    })

@role_required(allowed_roles=['Admin', 'Government Engineer', 'Normal User', 'Researcher', 'Entrepreneur'])
def electricity_demand_plot_daily(request):
    dataset_path = os.path.join(os.path.dirname(__file__), 'data', 'dummy_electricity_daily_data.csv')

    if not os.path.exists(dataset_path):
        return render(request, 'electricity_demand_daily.html', {'error': 'Dataset not found!'})

    try:
        df = pd.read_csv(dataset_path, parse_dates=['timestamp'])
    except Exception as e:
        return render(request, 'electricity_demand_daily.html', {'error': f'Error loading dataset: {str(e)}'})

    selected_date = request.GET.get('date', '2023-01-01')

    if not selected_date:
        return render(request, 'electricity_demand_daily.html', {'error': 'Please provide a date!'})

    try:
        selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
    except ValueError:
        return render(request, 'electricity_demand_daily.html', {'error': 'Invalid date format! Use YYYY-MM-DD.'})

    end_date = selected_date + timedelta(days=30)

    df_30_days = df[(df['timestamp'].dt.date >= selected_date) & (df['timestamp'].dt.date <= end_date)]

    if df_30_days.empty:
        return render(request, 'electricity_demand_daily.html', {'error': 'No data found for the selected period!'})

    # Filter required columns
    df_filtered = df_30_days[['timestamp', 'electricity_demand', 'solar_generation']]

    # Plotly graph
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_30_days['timestamp'], y=df_30_days['electricity_demand'],
        mode='lines+markers', name='Electricity Demand',
        line=dict(color='purple'),
        marker=dict(size=4)
    ))

    fig.update_xaxes(
        tickformat="%b %d",
        tickangle=45
    )

    fig.update_layout(
        title=f"Electricity Demand from {selected_date} to {end_date}",
        xaxis_title="Date",
        yaxis_title="Electricity Demand",
        template="plotly_white",
        width=1200,
        height=500
    )

    graph_html = pio.to_html(fig, full_html=False)

    # Convert Selected Columns to HTML Table
    df_table_html = df_filtered.to_html(classes="table table-bordered table-striped table-dark", index=False)

    return render(request, 'electricity_demand_daily.html', {
        'plot_div': graph_html,
        'selected_date': selected_date,
        'df_table_html': df_table_html  # Pass the filtered table to the template
    })

@role_required(allowed_roles=['Admin', 'Government Engineer', 'Normal User', 'Researcher', 'Entrepreneur'])
def electricity_demand_plot_monthly(request):
    dataset_path = os.path.join(os.path.dirname(__file__), 'data', 'dummy_electricity_monthly_data.csv')

    if not os.path.exists(dataset_path):
        return render(request, 'electricity_demand_monthly.html', {'error': 'Dataset not found!'})

    try:
        df = pd.read_csv(dataset_path, parse_dates=['timestamp'])
    except Exception as e:
        return render(request, 'electricity_demand_monthly.html', {'error': f'Error loading dataset: {str(e)}'})

    selected_date = request.GET.get('date', '2023-01-01')

    try:
        selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
    except ValueError:
        return render(request, 'electricity_demand_monthly.html', {'error': 'Invalid date format! Use YYYY-MM-DD.'})

    end_date = selected_date + timedelta(days=365)

    df_12_months = df[(df['timestamp'].dt.date >= selected_date) & (df['timestamp'].dt.date <= end_date)]

    if df_12_months.empty:
        return render(request, 'electricity_demand_monthly.html', {'error': 'No data found for the selected period!'})

    peak_point = df_12_months.loc[df_12_months['electricity_demand'].idxmax()]
    lowest_point = df_12_months.loc[df_12_months['electricity_demand'].idxmin()]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_12_months['timestamp'], y=df_12_months['electricity_demand'],
        mode='lines+markers', name='Electricity Demand',
        line=dict(color='purple'),
        marker=dict(size=4)
    ))

    fig.add_trace(go.Scatter(
        x=[peak_point['timestamp'], lowest_point['timestamp']],
        y=[peak_point['electricity_demand'], lowest_point['electricity_demand']],
        mode="markers",
        marker=dict(color='red', size=10, symbol='circle'),
        name="Highlighted Points"
    ))

    fig.add_annotation(
        x=peak_point['timestamp'], y=peak_point['electricity_demand'],
        text=f"Peak: {peak_point['electricity_demand']:.2f}",
        showarrow=True, arrowhead=2, ax=30, ay=-40, bgcolor="yellow"
    )

    fig.add_annotation(
        x=lowest_point['timestamp'], y=lowest_point['electricity_demand'],
        text=f"Lowest: {lowest_point['electricity_demand']:.2f}",
        showarrow=True, arrowhead=2, ax=-30, ay=40, bgcolor="lightgreen"
    )

    fig.update_xaxes(
        tickformat="%b %Y",
        tickangle=45
    )

    fig.update_layout(
        title=f"Electricity Demand from {selected_date} to {end_date}",
        xaxis_title="Month",
        yaxis_title="Electricity Demand",
        template="plotly_white",
        width=1200,
        height=500
    )

    graph_html = pio.to_html(fig, full_html=False)

    # Convert DataFrame to HTML table (only required columns)
    df_table_html = df_12_months[['timestamp', 'electricity_demand', 'solar_generation']].to_html(classes="table table-striped table-dark", index=False)

    return render(request, 'electricity_demand_monthly.html', {
        'plot_div': graph_html,
        'selected_date': selected_date,
        'df_table_html': df_table_html
    })


MODEL_PATH = os.path.join(os.path.dirname(__file__), 'data', 'xgb_regressor.json')

def load_xgboost_model():
    if not os.path.exists(MODEL_PATH):
        return None

    model = xgb.XGBRegressor()
    model.load_model(MODEL_PATH)
    return model

@role_required(allowed_roles=['Admin', 'Government Engineer'])
def electricity_demand_prediction(request):
    dataset_path = os.path.join(os.path.dirname(__file__), 'data', '2025 testset.csv')

    if not os.path.exists(dataset_path):
        return render(request, 'electricity_demand_prediction.html', {'error': 'Dataset not found!'})

    df = pd.read_csv(dataset_path, parse_dates=['timestamp'])

    # Get the selected date from the form
    selected_date = request.GET.get('date', None)
    
    if not selected_date:  # Default only if no date is provided
        selected_date = '2025-01-01'

    try:
        selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
    except ValueError:
        return render(request, 'electricity_demand_prediction.html', {'error': 'Invalid date format! Use YYYY-MM-DD.'})

    df_day = df[df['timestamp'].dt.date == selected_date]

    if df_day.empty:
        return render(request, 'electricity_demand_prediction.html', {'error': 'No data found for the selected date!', 'selected_date': selected_date})

    model = load_xgboost_model()
    if model is None:
        return render(request, 'electricity_demand_prediction.html', {'error': 'Prediction model not found in myapp/data/!', 'selected_date': selected_date})

    # Extract features
    df_day['year'] = df_day['timestamp'].dt.year
    df_day['month'] = df_day['timestamp'].dt.month
    df_day['hour_of_day'] = df_day['timestamp'].dt.hour
    df_day['is_weekend'] = df_day['timestamp'].dt.dayofweek >= 5

    features = ['temperature', 'solar_generation', 'is_holiday', 'year', 'month', 'is_weekend']

    if not all(col in df_day.columns for col in features):
        return render(request, 'electricity_demand_prediction.html', {'error': 'Required features missing in dataset!', 'selected_date': selected_date})

    X_test = df_day[features]

    df_day['predicted_demand'] = model.predict(X_test)

    peak_point = df_day.loc[df_day['predicted_demand'].idxmax()]
    lowest_point = df_day.loc[df_day['predicted_demand'].idxmin()]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_day['timestamp'], y=df_day['predicted_demand'],
        mode='lines+markers', name='Predicted Electricity Demand',
        line=dict(color='purple'),
        marker=dict(size=4)
    ))

    fig.add_trace(go.Scatter(
        x=[peak_point['timestamp'], lowest_point['timestamp']],
        y=[peak_point['predicted_demand'], lowest_point['predicted_demand']],
        mode="markers",
        marker=dict(color='red', size=10, symbol='circle'),
        name="Highlighted Points"
    ))

    fig.add_annotation(
        x=peak_point['timestamp'], y=peak_point['predicted_demand'],
        text=f"Peak: {peak_point['predicted_demand']:.2f}",
        showarrow=True, arrowhead=2, ax=30, ay=-40, bgcolor="yellow"
    )

    fig.add_annotation(
        x=lowest_point['timestamp'], y=lowest_point['predicted_demand'],
        text=f"Lowest: {lowest_point['predicted_demand']:.2f}",
        showarrow=True, arrowhead=2, ax=-30, ay=40, bgcolor="lightgreen"
    )

    fig.update_xaxes(
        tickformat="%H:%M",
        tickangle=45
    )

    fig.update_layout(
        title=f"Predicted Electricity Demand for {selected_date}",
        xaxis_title="Time of Day",
        yaxis_title="Electricity Demand",
        template="plotly_white",
        width=1400,
        height=600
    )

    graph_html = pio.to_html(fig, full_html=False)

    # Convert predicted DataFrame to HTML table for display
    df_day_display = df_day[['timestamp', 'predicted_demand']].to_html(classes="table table-striped text-white", index=False)

    return render(request, 'electricity_demand_prediction.html', {
        'plot_div': graph_html,
        'selected_date': selected_date,
        'predicted_table': df_day_display
    })