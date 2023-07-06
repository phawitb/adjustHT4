


import streamlit as st
import requests
from github import Github
from github import Auth

def update(contents,id,adj_temp,adj_humid):
    # id = '202306003'
    # adj_temp = 2.3
    # adj_humid = -10.8

    auth = Auth.Token("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")
    g = Github(auth=auth)
    
    contents[id] = {
        'adj_temp' : round(adj_temp,1),
        'adj_humid' : round(adj_humid,1)
    }

    file_content = ''
    for c in contents.keys():
        file_content += f"{c},{contents[c]['adj_temp']},{contents[c]['adj_humid']}\n"
    file_content = file_content[:-1]
    
    repo = g.get_repo("phawitb/adjustHT4")
    contents = repo.get_contents("adjust_error.txt", ref="main")
    a = repo.update_file(contents.path, "from PyGithub", file_content, contents.sha, branch="main")
    if 'content' in a.keys():
        return True
    


# auth = Auth.Token("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")
# g = Github(auth=auth)

response = requests.get("https://raw.githubusercontent.com/phawitb/adjustHT4/main/adjust_error.txt")
contents = {}
for i in response.text.split('\n'):
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



