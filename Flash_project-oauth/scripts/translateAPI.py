import mimetypes
import time
import os.path

import requests

class translate():
    def generate_auth_token(self):
        URL = 'https://vessel.pfizer.com/api/o/token?grant_type=client_credentials&client_id=Vessel_client&client_secret=xB96s%23aDw@py4Z'
        r = requests.post(url=URL)
        print(r.text)
        json_form = r.json()
        access_token = json_form['access_token']
        bearer_token = 'Bearer ' + access_token
        return bearer_token

    def tranlsate_files(self, bearer_token, file, source_lang, target_lang):
        try:

            print(" + Reading file data...")
            with open(file, 'rb') as b:
                byte_data = b.read()

            mime_type = mimetypes.guess_type(file)[0]
            print("="*200)
            print(mime_type)

            files = {'file': (file, byte_data, mime_type)}
            #print(files)

            headers = {'Authorization': bearer_token}

            # Submitting file for translation
            print("+ Submitting file for translation")
            url = "https://vessel.pfizer.com/api/translation/systran/v1.0/translate_text"
            payload = {"json": "{\"service_request\": {\"oauth_client_id\": \"Vessel_client\", \"async\" : true, \"api_token\": \"cbceb6d2-5230-11e8-8897-3c970e8bbffc\", \"data\": [{\"source\": \""+source_lang+"\",\"target\": \""+target_lang+"\"}]}}"}
            print(f"***************** payload: {payload}")
            response = requests.request("POST", url, headers=headers, data=payload, files=files)
            json_form = response.json()
            print(f"+ Response after submitting file for translation : {json_form}")
            reqid = json_form['service_response']['data'][0]['request_id']

            print(f"+ Request ID received: {reqid}")

            # checking status of file translation
            print("+ Checking status of file translation..")
            headers = {'Content-Type': 'application/json', 'Authorization': bearer_token}

            status = 'in progress'
            while (status == 'in progress'):
                # Added a time delay of 10 seconds
                time.sleep(10)
                url = "https://vessel.pfizer.com/api/translation/systran/v1.0/status"
                payload = "{\r\n    \"service_request\": {\r\n        \"oauth_client_id\": \"Vessel_client\",\r\n        \"api_token\": \"cbceb6d2-5230-11e8-8897-3c970e8bbffc\",\r\n        \"data\": [\r\n            {\r\n                \"request_id\": \"%s\"\r\n            }\r\n        ]\r\n    }\r\n}" % (
                    reqid)

                try:
                    response = requests.request("POST", url, headers=headers, data=payload)
                    print(f"+ Response from Translation status API: {response.text.encode('utf8')}")
                    json_form = response.json()
                    status = json_form['service_response']['data'][0]['status']
                    print(f"+ Status of translation: {status}")
                    if status == "started" or status == "export" or status == "import":
                        status = 'in progress'

                except Exception as e:
                    print(f"Exception: either token expired or something wrong.. \n {e} \n Trying again..")
                    auth_token = self.generate_auth_token()
                    headers = {'Content-Type': 'application/json', 'Authorization': auth_token}
                    url = "https://vessel.pfizer.com/api/translation/systran/v1.0/status"
                    payload = "{\r\n    \"service_request\": {\r\n        \"oauth_client_id\": \"Vessel_client\",\r\n        \"api_token\": \"cbceb6d2-5230-11e8-8897-3c970e8bbffc\",\r\n        \"data\": [\r\n            {\r\n                \"request_id\": \"%s\"\r\n            }\r\n        ]\r\n    }\r\n}" % (
                        reqid)
                    response = requests.request("POST", url, headers=headers, data=payload)
                    print(f"+ Response from Translation status API: {response.text.encode('utf8')}")
                    json_form = response.json()
                    status = json_form['service_response']['data'][0]['status']
                    print(f"+ Status of translation: {status}")
                    if status == "started" or status == "export" or status == "import":
                        status = 'in progress'
                    print(f"+ Status of translation: {status}")

            url = "https://vessel.pfizer.com/api/translation/systran/v1.0/result"
            payload = "{\r\n    \"service_request\": {\r\n        \"oauth_client_id\": \"Vessel_client\",\r\n        \"api_token\": \"cbceb6d2-5230-11e8-8897-3c970e8bbffc\",\r\n        \"data\": [\r\n            {\r\n                \"request_id\": \"%s\"\r\n            }\r\n        ]\r\n    }\r\n}" % (
                reqid)
            response = requests.request("POST", url, headers=headers, data=payload)
            print("+ response: ", response)

            # Changing pdf file to .docx extension
            '''
            split_dest_path = dest_path.split(".")
            if split_dest_path[1].lower() == "pdf":
                split_dest_path[1] = "docx"
                dest_path = ".".join(split_dest_path)
            print("+ dest_path: ", dest_path)
            '''
            file_name = file.split('\\')[-1]
            dest_path = fr"C:\Users\GAURAK02\PycharmProjects\batchOCR\Translated_files\{file_name}"

            # Saving file to local machine
            with open(dest_path, 'wb') as f:
                for chunk in response.iter_content():
                    f.write(chunk)

            error_code = 10 # some dummy value
            try:
                error_code = json_form['service_response']['data'][0]['err_code']
            except:
                pass

            return status

        except:
            return "ERROR"