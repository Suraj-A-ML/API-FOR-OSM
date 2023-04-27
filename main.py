from flask import Flask, request, render_template
import os
import json
import zipfile
import subprocess
from flask import jsonify
import itertools
import re
from flask_cors import CORS

#coding = utf8
app = Flask(__name__)
CORS(app)
def inv_path():
  #path = app.config['UNZIP_FOLDER'] + '/'
  #return os.path.join(path,'inventory.yaml')
  return '/home/ubuntu/osm/inventory.yaml'

def ins_path():
  #path = app.config['UNZIP_FOLDER'] + '/'
  #return os.path.join(path,'install_scaling_manager.yaml')
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
    params = request.get_json(force=True)
    master_ip = params['master_ip']
    os_user = params['os_user']
    os_pass = params['os_pass']
    print(master_ip)
    command  = ['sudo', 'ansible-playbook', '-i', inv_path() ,ins_path(), '--tags', "populate_inventory_yaml" ,'-e master_node_ip={}'.format(master_ip),'-e os_user={}'.format(os_user),'-e os_pass={}'.format(os_pass)]
    output = subprocess.check_output(command)
    
    return output
    
#@app.route('/ans',methods=['GET','POST'])
#def ans():
#       res = subprocess.run(['ansible','--version'])
#       print(res.stdout)
#       print(res.stderr)
#       return "done"

@app.route('/install')
def install_scaling_manager():


    command = ['sudo', 'ansible-playbook', '-i', inv_path(), ins_path(), '--tags', 'install', '--key-file', pem_path(), '-e', 'src_bin_path="."']
    output = subprocess.check_output(command)

    
    return output
    
 
@app.route('/start')
def start_scaling_manager():
    
    command = ['sudo', 'ansible-playbook', '-i', inv_path() ,ins_path(), '--tags', "start" ,'--key-file',pem_path(),'-e','src_bin_path="."']
    output = subprocess.check_output(command)
    

    return output
    

    

@app.route('/stop')
def stop_scaling_manager():
    command = ['sudo', 'ansible-playbook', '-i', inv_path() ,ins_path(), '--tags', "stop" ,'--key-file',pem_path(),'-e','src_bin_path="."']
    output = subprocess.check_output(command)
    
    return output
    
    
    

@app.route('/uninstall')
def uninstall_scaling_manager():
    command = ['sudo', 'ansible-playbook', '-i', inv_path() ,ins_path(), '--tags', "uninstall" ,'--key-file',pem_path(),'-e','src_bin_path="."']
    output = subprocess.check_output(command)
    
    return output
    
@app.route('/update_config')
def update_scaling_manager():
    command = ['sudo', 'ansible-playbook', '-i', inv_path() ,ins_path(), '--tags', "update" ,'--key-file',pem_path(),'-e','src_bin_path="."']
    output = subprocess.check_output(command)
    
    return output
    

#to develop a status end point
@app.route('/status')
def status_scaling_manager():
    #inv_path ='/home/ubuntu/osm/inventory.yaml'
    #ins_path ='/home/ubuntu/osm/install_scaling_manager.yaml'
    #pem_path = os.path.abspath("user-dev-aws-ssh.pem")
    command = ['sudo','ansible-playbook', '-i', inv_path() ,ins_path(), '--tags', "status" ,'--key-file',pem_path(),'-e','src_bin_path="."']
    output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   
    json_output1 = json.dumps(output.stdout.decode('utf-8').splitlines()[36:48],skipkeys=True,indent =4)
    
    
    json_output2= json.dumps(output.stdout.decode('utf-8').splitlines()[50:65],skipkeys=True,indent = 4)
    
   
    json_output3= json.dumps(output.stdout.decode('utf-8').splitlines()[70:95],skipkeys=True,indent = 4)
    
         
    
   
    str1 = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', json_output1).group(0)
    str4 = re.search(r"Active.*",json_output1).group(0)
    str7 = re.search('(?<=: )(\w+)',str4).group(0)
   
    
    
    str2 = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', json_output2).group(0)
    str5= re.search(r"Active.*",json_output2).group(0)
    str8 = re.search('(?<=: )(\w+)',str5).group(0)
   
    str3 = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',json_output3).group(0)
    str6 = re.search(r"Active.*",json_output3).group(0)
    str9 = re.search('(?<=: )(\w+)',str6).group(0)
    
    out = [str1, str2, str3]
    out2 = [str7, str8,str9]
 
    
    
    res = {out[i]: out2[i] for i in range(len(out))}
    finalres = jsonify(res)
              
    
    return finalres
              

@app.route('/update_pem')
def updatepem_scaling_manager():
    command = ['sudo', 'ansible-playbook', '-i', inv_path() ,ins_path(), '--tags', "update_pem" ,'--key-file',pem_path(),'-e','src_bin_path="."']
    output = subprocess.check_output(command)

    return output
    




if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(),"upload")
    app.config['UNZIP_FOLDER'] = os.path.join(os.getcwd(),"unzipped")
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['UNZIP_FOLDER'], exist_ok=True)
    app.run(debug=True,host="0.0.0.0")