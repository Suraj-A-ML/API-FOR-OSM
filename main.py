from flask import Flask, request
import os

import json

import zipfile
import subprocess
from flask import jsonify
import ast


#coding = utf8
app = Flask(__name__)
def inv_path():
  #path = app.config['UNZIP_FOLDER'] + '/'
  #return os.path.join(path,'inventory.yaml')
  return '/home/ubuntu/osm/inventory.yaml'

def ins_path():
  path = app.config['UPLOAD_FOLDER'] + '/'
  return os.path.join(path,'install_scaling_manager.yaml')
  return '/home/ubuntu/osm/install_scaling_manager.yaml'
  
def pem_path():
  return os.path.abspath("user-dev-aws-ssh.pem")
  

@app.route('/upload', methods=['GET', 'POST'])
def upload_zip():
    if request.method == 'POST':

        if 'file' not in request.files:
            return 'No file uploaded', 400

        file = request.files['file']
        if file.filename == '':
            return 'No file selected', 400


        zip_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(zip_path)


        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for file_info in zip_ref.infolist():
                file_info.filename = os.path.basename(file_info.filename)
                zip_ref.extract(file_info, app.config['UNZIP_FOLDER'])

        return 'File uploaded and unzipped successfully'

    return 'we render ui here for file upload'

@app.route('/populate',methods=['POST'])
def populate():
    master_ip = request.get_json('master_ip')
    os_user = request.get_json('os_user')
    os_pass = request.get_json('os_pass')
    command  = ['sudo', 'ansible-playbook', '-i', inv_path() ,ins_path(), '--tags', "populate_inventory_yaml" ,'-e master_node_ip={}'.format(master_ip),'-e os_user={}'.format(os_user),'-e os_pass={}'.format(os_pass)]
    subprocess.run(command)
    return "Scaling manager population is successful"
    
@app.route('/install')
def install_scaling_manager():

    command = ['sudo', 'ansible-playbook', '-i', inv_path(), ins_path(), '--tags', 'install', '--key-file', pem_path(), '-e', 'src_bin_path="."']
    output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    json_output = json.dumps({'stdout': output.stdout.decode('utf-8')})
    return json_output
    
 
@app.route('/start')
def start_scaling_manager():
    command = ['sudo', 'ansible-playbook', '-i', inv_path() ,ins_path(), '--tags', "start" ,'--key-file',pem_path(),'-e','src_bin_path="."']
    subprocess.run(command)
    return "Started"

@app.route('/stop')
def stop_scaling_manager():
    command = ['sudo', 'ansible-playbook', '-i', inv_path() ,ins_path(), '--tags', "stop" ,'--key-file',pem_path(),'-e','src_bin_path="."']
    subprocess.run(command)
    return 'Scaling manager stopped.'

@app.route('/uninstall')
def uninstall_scaling_manager():
    command = ['sudo', 'ansible-playbook', '-i', inv_path() ,ins_path(), '--tags', "uninstall" ,'--key-file',pem_path(),'-e','src_bin_path="."']
    subprocess.run(command)
    return 'Scaling manager is Uninstalled.'

@app.route('/update_config')
def update_scaling_manager():
    command = ['sudo', 'ansible-playbook', '-i', inv_path() ,ins_path(), '--tags', "update" ,'--key-file',pem_path(),'-e','src_bin_path="."']
    subprocess.run(command)
    return 'Scaling manager is Updated.'

#to develop a status end poin
@app.route('/status')
def status_scaling_manager():
    #inv_path ='/home/ubuntu/osm/inventory.yaml'
    #ins_path ='/home/ubuntu/osm/install_scaling_manager.yaml'
    #pem_path = os.path.abspath("user-dev-aws-ssh.pem")
    command = ['sudo','ansible-playbook', '-i', inv_path() ,ins_path(), '--tags', "status" ,'--key-file',pem_path(),'-e','src_bin_path="."']
    subprocess.run(command)
    return 'Status is returned.'


@app.route('/update_pem')
def updatepem_scaling_manager():
    command = ['sudo', 'ansible-playbook', '-i', inv_path() ,ins_path(), '--tags', "update_pem" ,'--key-file',pem_path(),'-e','src_bin_path="."']
    subprocess.run(command)
    return 'Pem files is updated.'

if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(),"upload")
    app.config['UNZIP_FOLDER'] = os.path.join(os.getcwd(),"unzipped")
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['UNZIP_FOLDER'], exist_ok=True)
    app.run(debug=True,host="0.0.0.0")

