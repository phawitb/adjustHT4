// Wait for the DOM to be fully loaded


document.addEventListener("DOMContentLoaded", function () {

    // Get the submit button element
    const submitBtn = document.getElementById("submitBtn");
    const loadBtn = document.getElementById("loadBtn");

    // const element = document.getElementById("id01");
    // element.innerHTML = 123.2;

    loadBtn.addEventListener("click", function () {
        const id = document.getElementById("id").value;
        console.log(id)

        fetch("https://raw.githubusercontent.com/phawitb/adjustHT4/main/adjust_error.txt")
        .then(response => response.text())
        .then(data => {
            
            d = data.split('\n')
            var data_dict = {};
            for (let i = 0, len = d.length, text = ""; i < len; i++) {
                dd = d[i].split(',')
                if(dd.length == 3){
                    // console.log(dd)
                    data_dict[dd[0]] = {
                        adj_temp : dd[1],
                        adj_humid : dd[2]
                    }
                }
            old_data = data_dict;
                
            }
            console.log(data_dict)
            console.log(data_dict[id])
            // console.log(123)
            document.getElementById("adj_temp").value = data_dict[id]['adj_temp'];
            document.getElementById("adj_humid").value = data_dict[id]['adj_humid'];
            document.getElementById("status").innerHTML = "";

            console.log(document.getElementById('submitBtn').style.display)
            if (!document.getElementById('submitBtn').style.display) {
                document.getElementById('H0').style.display = 'block';
                document.getElementById('H1').style.display = 'block';
                document.getElementById('adj_temp').style.display = 'block';
                document.getElementById('adj_humid').style.display = 'block';
                document.getElementById('submitBtn').style.display = 'block';
              }
        
            // element.innerHTML = parseFloat(data_dict[id]['adj_temp']);          

        })
        .catch(error => {
            console.error("Error retrieving data:", error);
            document.getElementById("status").innerHTML = "ID not exist!";
        });


    });

    // Handle button click
    submitBtn.addEventListener("click", function () {
        //get old_data---------------------
        fetch("https://raw.githubusercontent.com/phawitb/adjustHT4/main/adjust_error.txt")
        .then(response => response.text())
        .then(data => {
            // Use the data here
            // console.log(data.split('\n'));
            d = data.split('\n')
            var data_dict = {};
            for (let i = 0, len = d.length, text = ""; i < len; i++) {
                dd = d[i].split(',')
                if(dd.length == 3){
                    // console.log(dd)
                    data_dict[dd[0]] = {
                        adj_temp : dd[1],
                        adj_humid : dd[2]
                    }
                }
            old_data = data_dict;
                
            }
            
        })
        //create content---------------------
        const id = document.getElementById("id").value;
        const adj_temp = document.getElementById("adj_temp").value;
        const adj_humid = document.getElementById("adj_humid").value;
        console.log(id)
        console.log(adj_temp)
        console.log(adj_humid)
        
        old_data[id]['adj_temp'] = adj_temp;
        old_data[id]['adj_humid'] = adj_humid;
        console.log(old_data);
        console.log(Object.keys(old_data));
        d = Object.keys(old_data);
        var content = '';
        for (let i = 0, len = d.length, text = ""; i < len; i++){
            console.log(d[i])
            console.log(old_data[d[i]]['adj_temp'])
            console.log(old_data[d[i]]['adj_humid'])
            if(i==0){
                content += d[i] + ',' + old_data[d[i]]['adj_temp'] + ',' + old_data[d[i]]['adj_humid'];
            }
            else{
                content += '\n' + d[i] + ',' + old_data[d[i]]['adj_temp'] + ',' + old_data[d[i]]['adj_humid'];
            }
        }
        console.log(content)

        //update data---------------------
        // User input values
        const token = "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";
        const owner = "phawitb";
        const repo = "adjustHT4";
        const filePath = "adjust_error.txt";
        // const content = "NEW_FILE_CONTENT";

        // Retrieve the existing file content
        fetch(`https://api.github.com/repos/${owner}/${repo}/contents/${filePath}`, {
            headers: {
                "Authorization": `Bearer ${token}`,
                "Accept": "application/vnd.github.v3+json"
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.content) {
                // Decode the base64 encoded content
                const existingContent = atob(data.content);

                // Modify the existing content
                // const updatedContent = existingContent + "\n" + content;
                const updatedContent = content;

                // Prepare the request payload
                const payload = {
                    message: "Update file",
                    content: btoa(updatedContent), // Encode the updated content as base64
                    sha: data.sha // Include the file's current SHA
                };

                // Send the update request
                fetch(`https://api.github.com/repos/${owner}/${repo}/contents/${filePath}`, {
                    method: "PUT",
                    headers: {
                        "Authorization": `Bearer ${token}`,
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(payload)
                })
                .then(response => response.json())
                .then(data => {
                    if (data.content) {
                        console.log("File updated successfully!");
                        document.getElementById("status2").innerHTML = "updated successfully!";
                    } else {
                        console.log("File update failed!");
                        document.getElementById("status2").innerHTML = "update failed!";
                    }
                })
                .catch(error => console.error("Error:", error));
            } else {
                console.log("File not found!");
                document.getElementById("status2").innerHTML = "File not found!";
                
            }
        })
        .catch(error => console.error("Error:", error));
        document.getElementById("status2").innerHTML = "waiting..";


    });
});
