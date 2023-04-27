import yaml
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def submit_form():
    if request.method == 'POST':
        # name = request.form['name']
        monitor_with_logs = request.form['monitor_with_logs']
        monitor_with_simulator = request.form['monitor_with_simulator']
        purge_old_docs_after_hours = request.form['purge_old_docs_after_hours']
        recommendation_polling_interval_in_secs = request.form['recommendation_polling_interval_in_secs']
        fetchmetrics_polling_interval_in_secs = request.form['fetchmetrics_polling_interval_in_secs']
        is_accelerated = request.form['is_accelerated']
        user_config = {"monitor_with_logs":monitor_with_logs,
                       "monitor_with_simulator":monitor_with_simulator,
                       "purge_old_docs_after_hours":purge_old_docs_after_hours,
                       "recommendation_polling_interval_in_secs":recommendation_polling_interval_in_secs,
                       "fetchmetrics_polling_interval_in_secs":fetchmetrics_polling_interval_in_secs,
                       "is_accelerated":is_accelerated
                       }
        cluster_name = request.form['cluster_name']
        cloud_type = request.form['cloud_type']
        max_nodes_allowed = request.form['max_nodes_allowed']
        min_nodes_allowed = request.form['min_nodes_allowed']
        launch_template_id = request.form['launch_template_id']
        launch_template_version = request.form['launch_template_version']
        os_user = request.form['os_user']
        os_group = request.form['os_group']
        os_version = request.form['os_version']
        os_home = request.form['os_home']
        domain_name = request.form['domain_name']
        
        os_admin_username = request.form['os_admin_username']
        os_admin_password = request.form['os_admin_password']
        os_credentials = {"os_admin_username":os_admin_username,
                          "os_admin_password":os_admin_password}
        
        pem_file_path = request.form['pem_file_path']
        secret_key = request.form['secret_key']
        access_key = request.form['access_key']
        region = request.form['region']
        role_arn = request.form['role_arn']
        cloud_credentials = {
            "pem_file_path":pem_file_path,
            "secret_key":secret_key,
            "access_key":access_key,
            "region":region,
            "role_arn":role_arn
        }
        jvm_factor = request.form['jvm_factor']
        cluster_details = {
            "cluster_name":cluster_name,
            "cloud_type":cloud_type,
            "max_nodes_allowed":max_nodes_allowed,
            "min_nodes_allowed":min_nodes_allowed,
            "launch_template_id":launch_template_id,
            "launch_template_version":launch_template_version,
            "os_user":os_user,
            "os_group":os_group,
            "os_version":os_version,
            "os_home":os_home,
            "domain_name":domain_name,
            "os_credentials":os_credentials,
            "cloud_credentials":cloud_credentials,
            "jvm_factor":jvm_factor
        }
        rules = []
        task_name = request.form.get('task_name')
        operator = request.form.get('operator')
        if operator == "AND" or "OR":
            metric = request.form.get('metric')
            limit = request.form.get('limit')
            stat = request.form.get('stat')
            decision_period = request.form.get('decision_period')
            occurrences_percent = request.form.get('occurrences_percent')
            rule = {"metric":metric,
             "limit":limit,
             "stat":stat,
             "decision_period":decision_period,
             "occurrences_percent":occurrences_percent}
            rules.append(rule)
            
        elif operator == "EVENT":
            scheduling_time = request.form.get('scheduling_time')
            {"scheduling_time":scheduling_time}
            rules.append(scheduling_time)
        else :
            pass
        task_details = {"task_name":task_name,
                        "operator":operator,
                        "rules":rules}
        config = {"user_config":user_config,
                  "cluster_details":cluster_details,
                  "task_details":task_details}
        with open('config.yaml', 'w') as f:
            yaml.dump(config, f)
    return render_template('config.html')


    
if __name__ == '__main__':
    app.run(debug=True)