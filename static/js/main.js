       function submitform(){

        req_title = document.getElementById('req_title').value
        req_desc = document.getElementById('req_desc').value
        req_client = document.getElementById('req_client').value
        req_client_priority = document.getElementById('req_client_priority').value
        req_product_area = document.getElementById('req_product_area').value
        req_target_date = document.getElementById('req_target_date').value    
        
        $.ajax({
            type: 'POST',
            url: '/feature_request_list/',
            data: { 
              'title': req_title, 
              'description': req_desc,
              'client': req_client, 
              'client_priority': req_client_priority,
              'product_area': req_product_area, 
              'target_date': req_target_date
            },
            success: function(msg){
                var Table = document.getElementById("feature_req_table");
                Table.innerHTML = "";
                feature_req_list()
                alert('Request submitted successfully');
                // $('#myModal').modal('hide');
                $("#myModal .close").click()
            },
            error: function(data){                
               alert('Request failed');
               $("#myModal .close").click()
            }
      });
    }

    function feature_req_list(){
        $.ajax(
          { 
            url: "/feature_request_list/",
            context: document.body,
            success: function(data){
                if(data==""){
                  var table = document.getElementById("feature_req_table");
                  table.innerHTML="<b>No Feature Request Data</b>"
                }else{
                create_req_table(data)   
                }                           
          }});
    }

    function create_req_table(data) {
            var table = document.getElementById("feature_req_table");
            row_num=1
            var header = table.createTHead();
            var row = header.insertRow(0);
            var cell1 = row.insertCell(0);
            var cell2 = row.insertCell(1);
            var cell3 = row.insertCell(2);
            var cell4 = row.insertCell(3);
            var cell5 = row.insertCell(4);
            var cell6 = row.insertCell(5);
            cell1.innerHTML = "<b>Title</b>";
            cell2.innerHTML = "<b>Description</b>";
            cell3.innerHTML = "<b>Client</b>";
            cell4.innerHTML = "<b>Client Priority</b>";
            cell5.innerHTML = "<b>Date</b>";
            cell6.innerHTML = "<b>Product Area</b>";
            for (i = 0; i < data.length; i++) {   
                var row = table.insertRow(row_num);
                var cell1 = row.insertCell(0);
                var cell2 = row.insertCell(1);
                var cell3 = row.insertCell(2);
                var cell4 = row.insertCell(3);
                var cell5 = row.insertCell(4);
                var cell6 = row.insertCell(5);
                cell1.innerHTML = data[i]['title'];
                cell2.innerHTML = data[i]['description'];
                cell3.innerHTML = data[i]['client_name'];
                cell4.innerHTML = data[i]['client_priority'];
                cell5.innerHTML = data[i]['target_date'];
                cell6.innerHTML = data[i]['product_area_name'];
               
               row_num ++
            } 
    }   
    
    feature_req_list()