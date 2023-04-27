# API for OSM

### Overview

We have introduced REST API that allows for more flexible and scalable communication and easy integration for OpenSearch Scaling Manager. 

### Approach

- The older approach required manual execution of Ansible commands via CLI, whereas the new REST API enables the creation of endpoints that can automate and streamline these tasks.
- The adoption of REST API eliminates the need for manual intervention and enables the OpenSearch Scaling Manager to operate more efficiently.

### Architecture

The design includes following components

- Upload and Unzip
- Populate Inventory
- Install
- Start
- Stop
- Update
- Status
- Update PEM

#### Upload and Unzip

- The latest version of artifacts of OSM will be Uploaded.
- The latest build of Scaling Manager artifacts will be available in the OSM GitHub page.
- The code will Unzip the artifacts and store in folder.
- Artifacts is the zip file containing the following components
  1. install_scaling_manager.yaml.
  2. GNUmakefile.
  3. scaling_manager.tar.gz.

#### Populate Inventory

- The master node ip , OpenSearch user and OpenSearch password  is provided.
- Based on the master node details provided, the other details of data nodes of the cluster are populated into inventory.yaml.

#### Install 

- Based on the details provided in ansible file this  API will install all the dependencies in the data node mentioned in inventory file.

#### Start 

- Starts the scaling manager through which metrics will be collected and perform task(Scaleup or Scaledown) accordingly.

#### Stop 

- Stops the Scaling Manager.

#### Update config

- Update the scaling manager with the latest changes done to config file.

#### Update PEM 

- Update done to the PEM will be replaced with older version of PEM.

#### Status 

- Provides the current status of the nodes.
- It will also provides the description of the errors while performing the tasks. 



### API'S

We have the following API's for the Open search Scaling Manager



| Path           | Description                                                 | Method |                       Path Parameters                        | Request Body | Response                |
| -------------- | ----------------------------------------------------------- | ------ | :----------------------------------------------------------: | ------------ | ----------------------- |
| /upload        | Takes the artifacts and unzip it into the specified folder. | POST   |                             NONE                             | File         | {"message"type :string} |
| /populate      | Populates the inventory file.                               | POST   | master ip : string        os_user : string          os_password : string | NONE         | {"message"type :string} |
| /install       | Installs the Scaling Manager .                              | GET    |                             NONE                             | NONE         | {"message"type :string} |
| /start         | Start the Scaling Manager .                                 | GET    |                             NONE                             | NONE         | {"message"type :string} |
| /stop          | Stop the Scaling Manager                                    | GET    |                             NONE                             | NONE         | {"message"type :string} |
| /status        | Returns the status of the nodes.                            | GET    |                             NONE                             | NONE         | {"message"type :string} |
| /update_config | Updates the configuration                                   | GET    |                             NONE                             | NONE         | {"message"type :string} |
| /update_pem    | Updates the PEM file.                                       | GET    |                             NONE                             | NONE         | {"message"type :string} |
| /uninstall     | Uninstall the scaling manager                               | GET    |                             NONE                             | NONE         | {"message"type :string} |



### UI Design

- Home page contains the list of cards of all the endpoints.
- All the cards have description of the endpoints.

#### Upload card

- Upload card has description about how to upload artifacts.

- It has a button where the user uploads the artifacts of OSM.

- Status of upload is displayed along with errors.


#### Populate card

- Populate card has description  to add the details for the following.

  1.master_node_ip.

  2.os_user.

  3.os_password.

- Hovering on Populate provides the form to fill these details.

- Form submission trigger populate functionality.

- Status of populate is displayed along with errors.

```
sudo ansible-playbook -i inventory.yaml install_scaling_manager.yaml --tags "populate_inventory_yaml" -e master_node_ip=0.0.0.0 -e os_user=USERNAME -e os_pass=PASSWORD
```



#### Install card

- Install card has description to install dependencies in data node.

- Hovering install provides button to install dependencies.

```
sudo ansible-playbook -i inventory.yaml install_scaling_manager.yaml --tags "install" --key-file USERPEMFILEPATH.pem -e src_bin_path="."
```



#### Start card

- Start card has description to start the Scaling  manager.

```
sudo ansible-playbook -i inventory.yaml install_scaling_manager.yaml --tags "start" --key-file USERPEMFILEPATH.pem -e src_bin_path="."
```



#### Stop card

- Stop card has the description to stop the Scaling Manager.

```
sudo ansible-playbook -i inventory.yaml install_scaling_manager.yaml --tags "stop" --key-file USERPEMFILEPATH.pem -e src_bin_path="."
```



#### Status card

- Status card has the description about the status of all the nodes.

- It will return the status of all the nodes present in the cluster.

```
sudo ansible-playbook -i inventory.yaml install_scaling_manager.yaml --tags "status" --key-file USERPEMFILEPATH.pem -e src_bin_path="."
```



#### Update_config Card

- Update_config card has the description to update the scaling manager.

```
sudo ansible-playbook -i inventory.yaml install_scaling_manager.yaml --tags "update_config" --key-file USERPEMFILEPATH.pem -e src_bin_path="."
```



#### Update_pem card

- Update_pem card has the description to update the pem file

```
sudo ansible-playbook -i inventory.yaml install_scaling_manager.yaml --tags "update_pem" --key-file USERPEMFILEPATH.pem -e src_bin_path="."
```



#### Uninstall card

- Uninstall card has the description to uninstall the Scaling Manager.

```
sudo ansible-playbook -i inventory.yaml install_scaling_manager.yaml --tags "uninstall" --key-file USERPEMFILEPATH.pem -e src_bin_path="."
```