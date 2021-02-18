import urllib.request
from time import time

# import docker
import json
import psutil
import platform
import docker
import os
import random
# import time
# from elevate import elevate
from flask import Flask, render_template, request, make_response, url_for, redirect, flash
from flask_login import login_user, logout_user, current_user, login_required
from flask_wtf import FlaskForm
from werkzeug.urls import url_parse
from wtforms import SelectField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
# from os import path

from hurry.filesize import size
from app.byte2human import bytes2human

from app import app, db
from app.forms import LoginForm, ChangePasswordForm, TextForm, DockerfileForm, \
    Dockerfiles, Container_Run
from app.models import User
from flask_toastr import Toastr

toastr = Toastr(app)


# from flask_bootstrap import Bootstrap



# from datetime import datetime
# import datetime

UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
address_remote = '127.0.0.1:2375'
# address_remote = '192.168.55.2:2375'

@app.route('/')
@app.route('/index')
@login_required
def index():
    global address_remote

    counter = 0

    data_2 = urllib.request.urlopen("http://"+ address_remote +"/images/json").read()
    output_2 = json.loads(data_2)

    data = urllib.request.urlopen("http://"+ address_remote +"/containers/json?all=true").read()
    output = json.loads(data)

    container_id = output[counter]['Id']
    container_id_short = container_id[:12]

    # data1 = urllib.request.urlopen("http://0.0.0.0:2375/containers/" + container_id_short + "/top?ps_args=aux").read()
    # data1 = urllib.request.urlopen("http://127.0.0.1:2375/containers/" + container_id_short + "/top?ps_args=aux").read()
    # output_1 = json.loads(data1)

    return render_template("index3.html", len=len(output), output=output, output_2=output_2,
                           len2=len(output_2))

# output_1=output_1
@app.route('/images', methods=['post', 'get'])
@login_required
def index_images():
    global address_remote
    # short table
    # No, ID, Label,

    # full table
    # No, ID, Date, Repotags, Label, Size

    # client = docker.from_env()
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    # cli = APIClient(base_url='tcp://127.0.0.1:2375')
    message = ''
    if request.method == 'POST':
    
        container = request.form.get('container')
        if container != None:
            client.containers.run(container)
            message = "container '" + container + "' berhasil di jalankan"
        else:
            message = "your data must fill"

    data = urllib.request.urlopen("http://"+ address_remote +"/images/json").read()
    output = json.loads(data)
    return render_template("images.html", len=len(output), output=output)

@app.route('/images/build', methods=['post', 'get'])
@login_required
def image_build():
    global address_remote
    random1 = random.randint(1000, 9999)
    random2 = str(random1)
    client = docker.APIClient(base_url='tcp://'+ address_remote)
    # form = Dockerfiles()
    # if form.validate_on_submit:
    #     for filename in request.files.getlist('files'):
    #
    # form = Dockerfiles(csrf_enable=False)
    # print(form.dockerfile.data)
    if request.method == 'POST':
        # files = request.files.getlist['file[]']
        path1 = app.config['UPLOAD_FOLDER'] + "/" + random2
        if os.path.exists(path1) == False:
            os.makedirs(path1)
        for file in request.files.getlist('file[]'):
            # os.mkdir(path1)
            # filename = secure_filename(file.filename)
            filename = file.filename
            file.save(os.path.join(path1, filename))
        # if filename == "Dockerfile":
        #     a = [line for line in client.build(path=path1, rm=True, tag='coba:coba1')]
        #     a
            # print(a)
        for find in os.listdir(path1):
            if find == "Dockerfile":
            # if find.endswith(".txt"):
                a = [line for line in client.build(path=path1, rm=True, tag='coba_nginx:latest')]
                a

    # form = UploadForm()
    # if form.validate_on_submit():
    #     for filename in request.files.getlist('photo'):
    #         name = hashlib.md5('admin' + str(time.time())).hexdigest()[:15]
    #         photos.save(filename, name=name + '.')
    #     success = True
    # else:
    #     success = False

    return render_template('images-build.html')
    # client = docker.from_env()
    # # cli = APIClient(base_url='tcp://127.0.0.1:2375')
    # message = ''
    # form = DockerfileForm()
    # if request.method == 'POST':
    #     container = request.form.get('container')
    #     if container != None:
    #         client.containers.run(container)
    #         message = "container '" + container + "' berhasil di jalankan"
    #     else:
    #         message = "your data must fill"
    # if form.validate_on_submit():
    #     if form.dockerfile() != None:
    #
    # return render_template('run.html', message=message, form=form)


@app.route('/containers')
@login_required
def index_container():
    global address_remote
    counter = 0

    data_2 = urllib.request.urlopen("http://"+ address_remote +"/images/json").read()
    output_2 = json.loads(data_2)

    data = urllib.request.urlopen("http://"+ address_remote +"/containers/json?all=true").read()
    output = json.loads(data)

    # container_id = output[counter]['Id'][:12]
    #
    # data1 = urllib.request.urlopen("http://0.0.0.0:2375/containers/" +container_id+ "/top?ps_args=aux").read()
    # output_1 = json.loads(data1)
    # kosong = ("-")

    return render_template("containers.html", len=len(output), output=output,  output_2=output_2,
                           len2=len(output_2))
# output_1=output_1,

@app.route('/containers/run', methods=['GET', 'POST'])
@login_required
def container_run():
    global address_remote
    #client = docker.DockerClient(base_url='tcp://'+ address_remote)
    client= docker.APIClient(base_url='tcp://'+ address_remote)
    form = Container_Run()
    data = urllib.request.urlopen("http://"+ address_remote +"/info").read()
    output = json.loads(data)
    memTotal = output['MemTotal'] / 1000 / 1000
    # image = request.form.get('image')
    # container_name = request.form.get('name')
    # autoremove = request.form.get('auto_remove')
    # command1 = request.form.get('command')
    # entry_point = request.form.get('entryPoint')
    # dir_working = request.form.get('dir_working')
    # user = request.form.get('user')
    # console = request.form.get('console')
    # network = request.form.get('network')
    # hostname_ = request.form.get('hostname')
    # domain = request.form.get('domain_name')
    # mac_addr = request.form.get('mac_address')
    # ipv4 = request.form.get('ipv4')
    # one_dns = request.form.get('prim_dns')
    # sec_dns = request.form.get('sec_dns')
    # host_external = request.form.get('host_external')
    # name_env = request.form.get('name_env')
    # val_env = request.form.get('val_env')
    # name_label = request.form.get('name_label')
    # val_label = request.form.get('val_label')
    # restart_pol = request.form.get('restart')

    # cpu = request.form.get('cpu')
    # memory = request.form.get('memory')
    # mem_res = request.form.get('mem_reservation')



    if form.validate_on_submit:
        image_ = request.form.get('image')
        container_name = request.form.get('name')
        autoremove = request.form.get('auto_remove')
        command1 = request.form.get('command')
        entry_point = request.form.get('entryPoint')
        dir_working = request.form.get('dir_working')
        user = request.form.get('user')
        console = request.form.get('console')
        network = request.form.get('network')
        hostname_ = request.form.get('hostname')
        domain = request.form.get('domain_name')
        mac_addr = request.form.get('mac_address')
        ipv4 = request.form.get('ipv4')
        one_dns = request.form.get('prim_dns')
        sec_dns = request.form.get('sec_dns')
        host_external = request.form.get('host_external')
        name_env = request.form.get('name_env')
        val_env = request.form.get('val_env')
        name_label = request.form.get('name_label')
        val_label = request.form.get('val_label')
        restart_pol = request.form.get('restart')
        
        cpu = request.form.get('cpu')
        # int_cpu = int(cpu)
        memory = request.form.get('memory')
        mem_res = request.form.get('mem_reservation')
        # endpoint_config = client.create_endpoint_config(ipv4_address=ipv4)
        # config_networking = client.create_networking_config(endpoint_config)
        # config_host = client.create_host_config(auto_remove=autoremove, network_mode=network, restart_policy=restart_pol, extra_hosts=host_external, dns=(one_dns,sec_dns), mem_reservation=mem_res, mem_limit=memory, cpu_count=cpu)
        # client.containers.run(image=image, command=command1, name=container_name, auto_remove=autoremove, entrypoint=entry_point, working_dir=dir_working, user=user, network_mode=network, hostname=hostname_, domainname=domain, mac_address=mac_addr)
    
        # client.create_container(image, command=command1, hostname=hostname_, user=user, detach=False, stdin_open=False, tty=False, ports=None, environment=None, volumes=None, network_disabled=False, name=container_name, entrypoint=entry_point, working_dir=dir_working, domainname=domain, host_config=config_host, mac_address=mac_addr, labels=None, stop_signal=None, networking_config=config_networking, healthcheck=None, stop_timeout=None, runtime=None, use_config_proxy=True)
        # client.create_container(image, command=none, hostname=hostname_, user=user, name=container_name, entrypoint=entry_point, working_dir=dir_working, domainname=domain, host_config=config_host, mac_address=mac_addr, networking_config=config_networking)

    print(cpu)

    return render_template("containerrun.html", form=form, output=output, memTotal=memTotal)

@app.route('/containers/<idContainers>', methods=['GET', 'POST'])
@login_required
def page_container(idContainers):
    global address_remote
    container_id_short = idContainers[:12]
    data = urllib.request.urlopen("http://"+ address_remote +"/containers/" + container_id_short + "/json").read()
    output = json.loads(data)
    # data1 = info

    return render_template('idcontainer.html', output=output)


@app.route('/info/data/host-cpu')
@login_required
def cpu_host():
    # Create a PHP array and echo it as JSON
    data = [time() * 1000, psutil.cpu_percent(percpu=False)]

    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response


@app.route('/info/data/host-mem')
@login_required
def mem_host():
    # Create a PHP array and echo it as JSON
    data = [time() * 1000, psutil.virtual_memory().percent]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response


@app.route('/info/data/cpu-container')
@login_required
def cpu_container():
    # Create a PHP array and echo it as JSON
    # container_id_short = index_container.container_id_short

    # data1 = urllib.request.urlopen("http://127.0.0.1:2375/containers/"+index_container.container_id_short+"/top?ps_args=aux").read()
    # output_1 = json.loads(data1)
    data = [time() * 1000, psutil.cpu_percent(interval=1, percpu=False)]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

# @app.route('/run', methods=['post', 'get'])
# @login_required
# def run():
#     client = docker.from_env()
#     # cli = APIClient(base_url='tcp://127.0.0.1:2375')
#     message = ''
#     if request.method == 'POST':
#
#         container = request.form.get('container')
#         if container != None:
#             client.containers.run(container)
#             message = "container '" + container + "' berhasil di jalankan"
#         else:
#             message = "your data must fill"
#     return render_template('run.html', message=message)


@app.route('/host-info')
@login_required
def hostInfo():
    global address_remote
    # kernel = platform.release()
    # osVer = platform.platform()
    # hostname = platform.node()
    # osSystem = platform.system()
    # platformDist = platform.dist()[0] + ' ' + platform.dist()[1] + ' ' + platform.dist()[2]
    # cpuCount = psutil.cpu_count()
    # memSize = bytes2human(psutil.virtual_memory().total, format="%(value).3f %(symbol)s")
    data = urllib.request.urlopen("http://"+ address_remote +"/info").read()
    output = json.loads(data)
    memTotal = bytes2human(output['MemTotal'])

    # return render_template('host-info.html', kernel=kernel, osVer=osVer
    #                        , hostname=hostname, osSystem=osSystem, platformDist=platformDist
    #                        , cpuCount=cpuCount, memSize=memSize)
    return render_template('host-info.html', output=output, memTotal=memTotal)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# @app.route('/change', methods=['GET', 'POST'])
# @login_required
# def change_password():
#     """Change an existing user's password."""
#     form = ChangePasswordForm()
#     if form.validate_on_submit():
#         if current_user.check_password(form.old_password.data):
#             current_user.password = form.new_password2.data
#             db.session.add(current_user)
#             db.session.commit()
#             flash('Your password has been updated.', 'form-success')
#             return redirect(url_for('index'))
#     # form = ChangePasswordForm()
#     # if form.validate_on_submit():
#     #     if form.new_password.data == form.old_password.data:
#     #         flash('password baru tidak boleh sama dengan password lama')
#     #     elif current_user.password == form.old_password.data:
#     #         current_user.password = form.new_password.data
#     #         db.session.add(current_user)
#     #         db.session.commit()
#     #         flash('Change password sucssesful')
#     #         return redirect(url_for('main.index'))
#         else:
#             flash('Original password is invalid.', 'form-error')
#     return render_template('change_password.html', form=form)

@app.route('/cgroup/', methods=['get', 'post'])
@login_required
def cgroup():
    pathSliceCgroup = "/etc/systemd/system/"
    SliceCgroup = "docker_limit.slice"
    f = open(pathSliceCgroup + SliceCgroup, "r")
    content = f.read()
    # f = open("logs.txt", "r+")
    # content = f.read()
    # print(content)
    form = TextForm()
    if form.validate_on_submit():
        text = form.text.data
        f.close()
        f = open(pathSliceCgroup + SliceCgroup, "w+")
        f.write(text)
        f.close()
        return redirect(url_parse('/cgroup'))

    return render_template('cgroup.html', form=form, content=content)

@app.route('/setting', methods=['GET', 'POST'])
@login_required
def setting():
    # flash("All OK")
    # flash("All OK", 'success')
    # flash("All Normal", 'info')
    # flash("Not So OK", 'error')
    # flash("So So", 'warning')
    if request.method == 'POST':
        ip_remote = request.form["ip"]
        print (ip_remote)
    return render_template('setting.html')

@app.route('/loadbalance', methods=['GET', 'POST'])
@login_required
def loadbalance():
    path = "./nginx/nginx.conf"
    f = open(path, "r")
    content = f.read()
    if request.method == 'POST':
        # f = open("logs.txt", "r+")
        # content = f.read()
        # print(content)

        upstream_name = request.form['upstreamName']
        ip_address = request.form['ipAddress_center']

        listen_port = request.form['listen']
        print ("\n" +"upstream " + upstream_name + " {"+ "\n" + "server " + ip_address + ";" + "\n" +
                                            "}" + "\n" + "server " + "{" + "\n" +  listen_port + ";"+ "\n" +  "}" )
    return render_template('loadbalance.html', content=content)

@app.route('/swarm', methods=['GET', 'POST'])
@login_required
def cobacoba():
    client = docker.DockerClient(base_url='tcp://'+ address_remote)
    if request.method == "POST":
        name_service = request.form['service']
        replicas = request.form['replicas']
        port = request.form['port']
        image = request.form['images']
        print (name_service)
        print (replicas)
        print(port)
        print (image)
        os.system('docker service create --name ' + name_service + ' -p ' + port + ' --replicas ' + replicas +' ' + image )
        # client.services.create(image,command=None,)
    return render_template('cobacoba.html')


if os.getuid() == 0:
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
else:
    print("Please run this program using as root")



