# Create your views here.
from models import *
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.utils import timezone
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
import sys
import datetime
import json

def index(request):
    dictionary = {'active': 'home'}
    if request.user.is_authenticated():
        user = request.user
        dictionary['user'] = user
    return render_to_response('narrow-bootstrap-template.html', dictionary, context_instance=RequestContext(request))

def new_tree(request):
    if request.user.is_authenticated():
        user = request.user
    else:
        user = None
    if request.method == 'POST':
        print >>sys.stderr, request.POST
        if 'private' in request.POST and request.POST['private'] == 'on':
            private = True
        else:
            private = False
        name = request.POST['name']
        url = name.replace(' ', '-')[:30]
        if url in Tree.objects.all().values_list('url'):
            url = url + str(len(Tree.objects.filter(name = name)))
        tree = Tree(
            name = name,
            url = url,
            user = user,
            private = private,
            number_nodes = 1,
            number_words = 2)
        print >>sys.stderr, tree
        tree.save()
        messages.success(request, 'Tree Created')
        first_node = Node(
            tree = tree,
            nest_level = 0,
            order = 0,
            content = 'Start editing!')
        first_node.save()
        return HttpResponseRedirect('/tree/'+ tree.url)
    return HttpResponseRedirect('/my_trees')


def edit_tree(request, tree_url, nest_level = 0):
    dictionary = {}
    tree = Tree.objects.get(url = tree_url)
    nodes = Node.objects.filter(tree = tree).order_by('order')
    nodes_processed = []
    for node in nodes:
        modified_level = node.nest_level - nest_level
        if modified_level >= 0:
            nodes_processed.append([node, modified_level])
    dictionary['tree'] = tree
    dictionary['nodes'] = nodes_processed
    print>> sys.stderr, dictionary
    return render_to_response('tree-new.html', dictionary, context_instance=RequestContext(request))

def save_tree(request, tree_id, anonymous = False):
    print >>sys.stderr, request.POST
    if request.user.is_authenticated() and anonymous == False:
        messages.info(request, 'Anonymous Trees will be editable by anyone.  Login or Register before saving to make it private')
    try:
        tree = Tree.objects.get(pk = tree_id)
    except:
        messages.error('Tree doesn\'t exist')
    
    data = json.loads(request.POST['data'])
    items =  data['items']
    number_items = int(request.POST['number_items'])
    item_ids = []
    item_contents = []
    item_nest_level = []
    item_order = []
    number_words = 0
    #delte all nodes
    Node.objects.filter(tree = tree).delete()
    for i in range(0,number_items):
        item = items[i]
        number_words = number_words + len(item['content'].split(' '))
        n = Node(tree = tree,
                 nest_level = item['nest_level'],
                 order = item['order'],
                 content = item['content'])
        n.save()
    tree.number_nodes = number_items
    tree.number_words = number_words
    tree.save()
    return HttpResponse('True')

def delete_tree(request, tree_id):
    tree = Tree.objects.get(pk = tree_id)
    if request.user.is_authenticated() and tree.user == request.user:
        tree.delete()
    return HttpResponseRedirect('/my_trees')
    

def user_detail(request, user_id):
    user = User.objects.get(pk = user_id)
    user_trees = Tree.objects.get(user = user)
    dictionary = {'user': user, 'trees': user_trees}
    return render_to_response('about.html', dictionary, context_instance=RequestContext(request))

def login_user(request):
    if request.method == 'POST': # If the form has been submitted...
        form = LoginForm(request.POST) # A form bound to the POST data
        print >>sys.stderr, form.is_valid()
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            print >>sys.stderr, 'is_valid'
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            u = authenticate(username=username, password=password)
            if u is not None:
                login(request, u)
            else:
                messages.error(request, 'Incorrect username or password, please try again.')
                return redirect('/')
            messages.info(request, 'Logged in')
            return redirect('/') # Redirect after POST
    else:
        form = LoginForm() # An unbound form

    return render_to_response('base.html', {
        'form': form,
    }, context_instance=RequestContext(request))

def logout_user(request):
    logout(request)
    return redirect('/')

def new_user(request):
    dictionary = {'active': 'join'}
    if request.method == 'POST': # If the form has been submitted...
        form = UserForm(request.POST) # A form bound to the POST 
        print >>sys.stderr, form.errors
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            print >>sys.stderr, 'is_valid'
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.create_user(username, email, password)
            except:
                dictionary['error'] = 'Username is taken'
            u = authenticate(username=username, password=password)
            if u is not None:
                login(request, u)
            return HttpResponseRedirect('/my_trees') # Redirect after POST
            print user
    else:
        form = UserForm() # An unbound form
    dictionary['form'] = form
    return render_to_response('new_user.html', dictionary, context_instance=RequestContext(request))

def user_trees(request):
    dictionary = {'active': 'my_trees'}
    if request.user.is_authenticated():
        user = request.user
        dictionary['user'] = user
        trees = Tree.objects.filter(user = user)
        dictionary['trees'] = trees
    if request.method == 'POST': # If the form has been submitted...
        form = TreeForm(request.POST) # A form bound to the POST 
        print >>sys.stderr, form.errors
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            print >>sys.stderr, 'is_valid'
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                tree = Tree()
            except:
                print >>sys.stderr, 'error'
            return HttpResponseRedirect('/') # Redirect after POST
            print user
    else:
        form = UserForm() # An unbound form
    dictionary['form'] = form
    return render_to_response('user_trees.html', dictionary, context_instance=RequestContext(request))


    
def example(request):
    dictionary = {}
    dictionary['active'] = 'example'
    if request.user.is_authenticated():
        user = request.user
        dictionary['user'] = user
    return render_to_response('example.html', dictionary, context_instance=RequestContext(request))