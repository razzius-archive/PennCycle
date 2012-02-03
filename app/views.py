# Create your views here.
from app.models import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django import forms


class SignupForm(forms.ModelForm):
  class Meta:
    model = Student

def index(request):
  m = 'Sign up <a href="#">here</a>'
  
  context = {
      'message': m,
  }
  return render_to_response('index.html', context)

def signup(request):
  video_embed = "<object style="height: 390px; width: 640px"><param name="movie" value="http://www.youtube.com/v/1eFDra1XimA?version=3&feature=player_profilepage"><param name="allowFullScreen" value="true"><param name="allowScriptAccess" value="always"><embed src="http://www.youtube.com/v/1eFDra1XimA?version=3&feature=player_profilepage" type="application/x-shockwave-flash" allowfullscreen="true" allowScriptAccess="always" width="640" height="360"></object>"
  waiver_text = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. In lectus lectus, rutrum eget venenatis non, ornare sit amet elit. Donec sit amet lorem ut felis lacinia bibendum. Nulla auctor, dolor at scelerisque consectetur, magna velit pretium odio, vitae egestas orci eros vitae est. Sed sagittis porttitor dictum. Suspendisse vel lorem ut dolor vestibulum fermentum. Sed vestibulum mauris quis diam pellentesque nec viverra turpis pellentesque. Nam metus est, tempus nec scelerisque nec, scelerisque at erat."""
  scripts = """<script>
    $(function () {
     $('#myTab').tab('show')
    })
  </script>"""

  if request.method == 'POST':
    form = SignupForm(request.POST)
    if form.is_valid():
      # Process the data in form.cleaned data
      form.save()
      return HttpResponseRedirect('/thanks/')
      #return render_to_response('thanks.html', {})
  else:
    form = SignupForm()

  context = {
      'video_embed': video_embed,
      'waiver_text': waiver_text,
      'scripts': scripts,
      'form': form,
  }
  context_instance = RequestContext(request, context)
  return render_to_response('signup.html', context_instance)

def thanks(request):
  return render_to_response('thanks.html', {})

#def signup(request):
#  m = "Sign up for PennCycle"
#  form = SignupForm()
#  c = {}
#  c.update(csrf(request))
#  csrfContext = RequestContext(request)
#  c = {
#      'message': m,
#      'form': form,
#  }
#  c.update(csrf(request))
#  return render_to_response('signup.html', c)
