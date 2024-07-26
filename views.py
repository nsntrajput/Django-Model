from django.shortcuts import render, redirect
from .forms import DataFileForm
from .models import DataFile
from .forms import SelectColumnsForm
from .models import UploadedFile
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64
import urllib.parse
from django.contrib.auth.decorators import login_required
import matplotlib
matplotlib.use('agg')
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
import urllib
from django.utils.html import escapejs


@login_required

def upload_file(request):
    if request.method == 'POST':
        form = DataFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('file_list')
    else:
        form = DataFileForm()
    return render(request, 'dataapp/upload.html', {'form': form})


def file_list(request, file_id):
    uploaded_file = UploadedFile.objects.get(id=file_id)
    file_path = uploaded_file.file.path
    file_extension = file_path.split('.')[-1]
    if file_extension == 'xlsx':
        engine = 'openpyxl'
    elif file_extension == 'xls':
        engine = 'xlrd'
    else:
        raise ValueError(f'Unsupported file extension: {file_extension}')
    df = pd.read_excel(file_path, engine=engine)
    if request.method == 'POST':
        form = SelectColumnsForm(request.POST)
        if form.is_valid():
            selected_columns = form.cleaned_data['columns']
            graph_type = form.cleaned_data['graph_type']
            request.session['selected_columns'] = selected_columns
            request.session['graph_type'] = graph_type
            return redirect('dataapp:visualize_data')
    else:
        form = SelectColumnsForm()
        form.fields['columns'].choices = [(col, col) for col in df.columns]
    return render(request, 'dataapp/file_list.html', {'form': form, 'data': escapejs(df.to_html(classes='table table-striped'))})


@login_required

def visualize_data(request, file_id):
    file = DataFile.objects.get(id=file_id)
    df = pd.read_excel(file.file.path)
    columns = df.columns.tolist()
    
    graph_2d = ""
    graph_3d = ""
    visualization_type = '2D'  # Default value

    if request.method == 'POST':
        selected_columns = request.POST.getlist('columns')
        filter_column = request.POST.get('filter_column')
        filter_value = request.POST.get('filter_value')
        visualization_type = request.POST.get('visualization_type')
        
        if selected_columns:
            df = df[selected_columns]
        if filter_column and filter_value:
            df = df[df[filter_column] == filter_value]
        
        if visualization_type == '3D' and len(selected_columns) >= 3:
            fig = px.scatter_3d(df, x=selected_columns[0], y=selected_columns[1], z=selected_columns[2])
            graph_3d = fig.to_html(full_html=False, default_height=500)
        elif visualization_type == '2D' and len(selected_columns) >= 2:
            plt.figure(figsize=(10, 6))
            sns.scatterplot(data=df, x=selected_columns[0], y=selected_columns[1])
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            string = base64.b64encode(buf.read())
            graph_2d = 'data:image/png;base64,' + urllib.parse.quote(string)
    
    return render(request, 'dataapp/visualize.html', {
        'df': df.to_html(),
        'columns': columns,
        'graph_2d': graph_2d,
        'graph_3d': graph_3d,
        'visualization_type': visualization_type
    })


class LoginView(LoginView):
    template_name = 'dataapp/login.html'

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'dataapp/register.html'
    success_url = '/'
