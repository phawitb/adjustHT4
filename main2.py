


import streamlit as st
import requests
from github import Github
from github import Auth
import base64

repo_owner = "phawitb"
repo_name = "adjustHT4"
file_path = "adjust_error.txt"
access_token = "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"

def delete_file():
    # API endpoint for deleting a file
    delete_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
    
    # Headers with authentication
    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Get the current file details
    response = requests.get(delete_url, headers=headers)
    file_data = response.json()
    
    if "message" in file_data and file_data["message"] == "Not Found":
        print("File not found.")
        return
    
    # Delete the file
    delete_payload = {
        "message": "Delete file",
        "sha": file_data["sha"]
    }
    
    response = requests.delete(delete_url, json=delete_payload, headers=headers)
    
    if response.status_code == 200:
        print("File deleted successfully.")
    else:
        print(f"Error deleting file: {response.content.decode('utf-8')}")

def add_file(file_content):
    # file_content = "hellllooooo"  
    # file_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
    headers = {"Authorization": f"token {access_token}"}
    # response = requests.get(file_url, headers=headers)
    # file_data = response.json()

    # print('file_data',file_data)

    new_content = base64.b64encode(file_content.encode('utf-8')).decode('utf-8')
    commit_message = "Update file via web app"
    payload = {
        "message": commit_message,
        "content": new_content,
        # "sha": file_data['sha']
    }
    update_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
    response = requests.put(update_url, json=payload, headers=headers)

    print('response.status_code',response.status_code)

    if response.status_code == 201:
        return True
    else:
        return False

    # if response.status_code == 200:
    #     return True
    # else:
    #     return False

# def update_file(file_content):
#     # file_content = "hellllooooo"  
#     file_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
#     headers = {"Authorization": f"token {access_token}"}
#     response = requests.get(file_url, headers=headers)
#     file_data = response.json()

#     new_content = base64.b64encode(file_content.encode('utf-8')).decode('utf-8')
#     commit_message = "Update file via web app"
#     payload = {
#         "message": commit_message,
#         "content": new_content,
#         "sha": file_data['sha']
#     }
#     update_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
#     response = requests.put(update_url, json=payload, headers=headers)

#     if response.status_code == 200:
#         return True
#     else:
#         return False


def update(contents,id,adj_temp,adj_humid):
    # id = '202306003'
    # adj_temp = 2.3
    # adj_humid = -10.8
    
    contents[id] = {
        'adj_temp' : round(adj_temp,1),
        'adj_humid' : round(adj_humid,1)
    }

    file_content = ''
    for c in contents.keys():
        file_content += f"{c},{contents[c]['adj_temp']},{contents[c]['adj_humid']}\n"
    file_content = file_content[:-1]

    delete_file()
    sta = add_file(file_content)

    # sta = update_file(file_content)
    return sta


    
    # repo = g.get_repo("phawitb/adjustHT4")
    # contents = repo.get_contents("adjust_error.txt", ref="main")
    # a = repo.update_file(contents.path, "from PyGithub", file_content, contents.sha, branch="main")
    # if 'content' in a.keys():
    #     return True
    


# auth = Auth.Token("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")
# auth = Auth.Token("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")
# g = Github(auth=auth)

response = requests.get("https://raw.githubusercontent.com/phawitb/adjustHT4/main/adjust_error.txt")
contents = {}
for i in response.text.split('\n'):
    print(i)

    if i:
        c = i.split(',')
        contents[c[0]] = {
            'adj_temp' : c[1],
            'adj_humid' : c[2]
        }


st.write("# Adjust HT")

serial_number = st.text_input("ID", key="id")

ALL_ID = contents.keys()

if not serial_number:
    pass
elif serial_number in ALL_ID:
    adj_temp = contents[serial_number]['adj_temp']
    adj_humid = contents[serial_number]['adj_humid']
    adj_temp = st.number_input('Adjust temperature',value=round(float(adj_temp),1),step=0.1)
    adj_humid = st.number_input('Adjust humid',value=round(float(adj_humid),1),step=0.1)
    # adj_temp = 0.45
    # adj_humid = st.number_input('Adjust humid',adj_humid)

    if st.button('## SUMMIT'):
        

        sta = update(contents,serial_number,adj_temp,adj_humid)
        if sta:
            st.write(f'#### update complete!')
            st.write('serial_number:',serial_number)
            st.write('adj_temp:',adj_temp)
            st.write('adj_humid:',adj_humid)
        else:
            st.write('error!!')


else:
    st.write('ID not exist!')
# btn = st.button('LOAD')
# if btn:
#     st.write(btn)
#     adj_temp = st.number_input('Adjust temp')
#     adj_humid = st.number_input('Adjust humid')

#     if st.button('Press me2!'):
#         st.write('ssss')



