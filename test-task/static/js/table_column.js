
/////////////////////////////////////////////////////
// Fucntion for get table columns
/////////////////////////////////////////////////////
function show_table_column(input) {
    // const table_name = parseInt(document.getElementById("table_id").value);  // parseFloat, Number
    // alert("Table_Name: "+input)

    const baseURL = "http://127.0.0.1:8000/";
    const midURL = "maker/api/dbcolumns/"; 
    let theUrl = baseURL+midURL+input+"/";
    // alert("URL: "+theUrl)

    let xhr = new XMLHttpRequest();
    let res_str = "";
    xhr.open("GET", theUrl, true);
    xhr.onload = function (e) {
    if (xhr.readyState === 4) {
        if (xhr.status === 200) {
            res_str = xhr.responseText
           
            try {
                let json_data = JSON.parse(xhr.responseText);
                
                // $('#column_id').empty().append('<option selected="selected" value="">--- Select One ---</option>')
                // for (const property in json_data.response) {
                //     $('#column_id').append($('<option>', { 
                //         value: property,
                //         text : json_data.response[property]
                //     }));
                // }
                
                let select1 = document.getElementById("column_id");
                let length = select1.options.length;
                for (i = length-1; i >= 1; i--) {
                    select1.options[i] = null;
                }

                let select = document.getElementById('column_id');
                for (const property in json_data.response){
                    var opt = document.createElement('option');
                    opt.value = property;
                    opt.innerHTML = json_data.response[property];
                    select.appendChild(opt);
                }

            }catch(err) {

                console.log(err);
                
            }   
        } else {
            console.error(xhr.statusText);
        }
    }
    };
    xhr.onerror = function (e) {
        console.error(xhr.statusText);
    };
    xhr.send(null);
    // alert("GET request sucess full")
    console.log(input)  
}

