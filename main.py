from flask import Flask, request, render_template
import os 
import zipfile
import subprocess


app = Flask(__name__)
def inv_path():
  path = app.config['UPLOAD_FOLDER'] + '/'
  return os.path.join(path,'inventory.yaml')

def ins_path():
  path = app.config['UPLOAD_FOLDER'] + '/'
  return os.path.join(path,'install_scaling_manager.yaml')

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
    command  = ['sudo', 'ansible-playbook', '-i', inv_path() ,ins_path(), '--tags', "populate_inventory_yaml" ,'-e master_node_ip={}'.format(master_ip),'-e os_user={}'.format(os_user),'-e os_pass={}'.format(os_pass),'-kK']
    subprocess.run(command)
    return "Scaling manager population is successful"


#@app.route('/ans',methods=['GET','POST'])
#def ans():
#	res = subprocess.run(['ansible','--version'])
#	print(res.stdout)
#	print(res.stderr)
#	return "done"

@app.route('/install')
def install_scaling_manager():	    
    command = ['sudo', 'ansible-playbook', '-i', inv_path() ,ins_path(), '--tags', "install" ,'-kK']
    subprocess.run(command) 
    return 'Scaling manager installation started.'

@app.route('/start')
def start_scaling_manager():    
    command = ['sudo', 'ansible-playbook', '-i', inv_path() ,ins_path(), '--tags', "start" ,'-kK']
    subprocess.run(command) 
    return 'Scaling manager started.'

@app.route('/stop')
def stop_scaling_manager(): 
    command = ['sudo', 'ansible-playbook', '-i', inv_path() ,ins_path(), '--tags', "stop" ,'-kK']
    subprocess.run(command) 
    return 'Scaling manager stopped.'

@app.route('/uninstall')
def uninstall_scaling_manager():    
    command = ['sudo', 'ansible-playbook', '-i', inv_path() ,ins_path(), '--tags', "uninstall" ,'-kK']
    subprocess.run(command) 
    return 'Scaling manager is Uninstalled.'

@app.route('/update')
def update_scaling_manager():
    command = ['sudo', 'ansible-playbook', '-i', inv_path() ,ins_path(), '--tags', "update" ,'-kK']
    subprocess.run(command) 
    return 'Scaling manager is Updated.'
 
#to develop a status end point
@app.route('/status')
def status_scaling_manager():
    command = ['sudo', 'ansible-playbook', '-i', inv_path() ,ins_path(), '--tags', "status" ,'-kK']
    subprocess.run(command) 
    return 'Status is returned.'


    
@app.route('/update_pem')
def updatepem_scaling_manager():    
    command = ['sudo', 'ansible-playbook', '-i', inv_path() ,ins_path(), '--tags', "update_pem" ,'-kK']
    subprocess.run(command) 
    return 'Pem files is updated.'
        
    
    

if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = '/home/ubuntu/flask_app/uploads'
    app.config['UNZIP_FOLDER'] = '/home/ubuntu/flask_app/unzip'
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['UNZIP_FOLDER'], exist_ok=True)
    app.run(debug=True)
