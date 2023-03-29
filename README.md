## API FOR OPENSEARCH SCALING MANAGER

- We have introduced REST API that allows for more flexible and scalable communication and easy integration for open Search Scaling Manager.

  

### PRE-REQUISITES



- Flask 

- Python version>3

   



### API'S

We have the following API's for the Open search Scaling Manager



| Path           | Description                                                 | Method |                       Path Parameters                        | Request Body | Response                |
| -------------- | ----------------------------------------------------------- | ------ | :----------------------------------------------------------: | ------------ | ----------------------- |
| /upload        | Takes the artifacts and unzip it into the specified folder. | POST   |                             NONE                             | File         | {"message"type :string} |
| /populate      | Populates the inventory file.                               | POST   | master ip : string                                             os_user : string          os_password : string | NONE         | {"message"type :string} |
| /install       | Installs the Scaling Manager .                              | GET    |                             NONE                             | NONE         | {"message"type :string} |
| /start         | Start the Scaling Manager .                                 | GET    |                             NONE                             | NONE         | {"message"type :string} |
| /stop          | Stop the Scaling Manager                                    | GET    |                             NONE                             | NONE         | {"message"type :string} |
| /status        | Returns the status of the nodes.                            | GET    |                             NONE                             | NONE         | {"message"type :string} |
| /update_config | Updates the configuration                                   | GET    |                             NONE                             | NONE         | {"message"type :string} |
| /update_pem    | Updates the PEM file.                                       | GET    |                             NONE                             | NONE         | {"message"type :string} |
| /uninstall     | Uninstall the scaling manager                               | GET    |                             NONE                             | NONE         | {"message"type :string} |

