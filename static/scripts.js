// Define your API endpoint here
//var API_ENDPOINT = "API_ENDPOIND_PASTE_HERE";

// Helper function to create dynamic table headers
function createTableHeaders(tableHeaderId, keys) {
    let headerRow = document.getElementById(tableHeaderId);
    headerRow.innerHTML = ''; // Clear previous headers
    keys.forEach(key => {
        let th = document.createElement('th');
        th.appendChild(document.createTextNode(key));
        headerRow.appendChild(th);
    });
}

// Helper function to create dynamic table rows
function createTableRows(tableBodyId, data) {
    let tableBody = document.getElementById(tableBodyId);
    tableBody.innerHTML = ''; // Clear previous rows
    data.forEach(item => {
        let tr = document.createElement('tr');
        Object.values(item).forEach(value => {
            let td = document.createElement('td');
            td.appendChild(document.createTextNode(value));
            tr.appendChild(td);
        });
        tableBody.appendChild(tr);
    });
}

// AJAX POST request to save student data
document.getElementById("savestudent").onclick = function() {
    var inputData = {
        "Email": $('#Email').val(),
        "Name": $('#Name').val(),
        "Cohort": $('#Cohort').val(),
        "Nationality": $('#Nationality').val(),
        "Sex": $('#Sex').val()
    };

    $.ajax({
        url: "https://3mguhroo78.execute-api.us-east-1.amazonaws.com/prod" ,
        type: 'POST',
        data: JSON.stringify(inputData),
        contentType: 'application/json; charset=utf-8',
        success: function(response) {
            document.getElementById("studentSaved").innerHTML = "Student Data Saved!";
        },
        error: function() {
            alert("Error saving student data.");
        }
    });
}

// AJAX GET request to retrieve all students
document.getElementById("getstudents").onclick = function() {  
    $.ajax({
        url: "https://3mguhroo78.execute-api.us-east-1.amazonaws.com/prod",
        type: 'GET',
        contentType: 'application/json; charset=utf-8',
        success: function(response) {
            $('#studentTable').show();
            createTableHeaders('studentTableHeader', Object.keys(response[0]));
            createTableRows('studentTableBody', response);
        },
        error: function() {
            alert("Error retrieving student data.");
        }
    });
}

// AJAX POST request to save attendance data
document.getElementById("saveAttendance").onclick = function() {
    var inputData = {
        "Email": $('#Email').val(),
        "Name": $('#Name').val(),
        "week1": $('#week1').val(),
        "week2": $('#week2').val(),
        "week3": $('#week3').val(),
        "week4": $('#week4').val(),
        "week5": $('#week5').val(),
        
    };

    $.ajax({
        url: "https://6zx2cuqdw5.execute-api.us-east-1.amazonaws.com/prod" ,
        type: 'POST',
        data: JSON.stringify(inputData),
        contentType: 'application/json; charset=utf-8',
        success: function(response) {
            document.getElementById("attendanceSaved").innerHTML = "Attendance Data Saved!";
        },
        error: function() {
            alert("Error saving attendance data.");
        }
    });
}

// AJAX GET request to retrieve all attendance
document.getElementById("getAttendance").onclick = function() {
    $.ajax({
        url: "https://6zx2cuqdw5.execute-api.us-east-1.amazonaws.com/prod",
        type: 'GET',
        contentType: 'application/json; charset=utf-8',
        success: function(response) {
            $('#attendanceTable').show();
            createTableHeaders('attendanceTableHeader', Object.keys(response[0]));
            createTableRows('attendanceTableBody', response);
        },
        error: function() {
            alert("Error retrieving attendance data.");
        }
    });
}

// AJAX POST request to save assignment data
document.getElementById("saveAssignment").onclick = function() {
    var inputData = {
        "Email": $('Email').val(),
        "Name": $('#Name').val(),
        "week1": $('#week1').val(),
        "week2": $('#week2').val(),
        "week3": $('#week3').val(),
        "week4": $('#week4').val(),
        "week5": $('#week5').val()
    };

    $.ajax({
        url: "https://d9zprnksyj.execute-api.us-east-1.amazonaws.com/prod",
        type: 'POST',
        data: JSON.stringify(inputData),
        contentType: 'application/json; charset=utf-8',
        success: function(response) {
            document.getElementById("assignmentSaved").innerHTML = "Assignment Data Saved!";
        },
        error: function() {
            alert("Error saving assignment data.");
        }
    });
}

// AJAX GET request to retrieve all assignments
document.getElementById("getAssignment").onclick = function() {
    $.ajax({
        url: "https://d9zprnksyj.execute-api.us-east-1.amazonaws.com/prod",
        type: 'GET',
        contentType: 'application/json; charset=utf-8',
        success: function(response) {
            $('#assignmentTable').show();
            createTableHeaders('assignmentTableHeader', Object.keys(response[0]));
            createTableRows('assignmentTableBody', response);
        },
        error: function() {
            alert("Error retrieving assignment data.");
        }
    });
}

// AJAX GET request to retrieve summary
document.getElementById("getSummary").onclick = function() {
    $.ajax({
        url: "https://vw62c5evdh.execute-api.us-east-1.amazonaws.com/prod",
        type: 'GET',
        contentType: 'application/json; charset=utf-8',
        success: function(response) {
            $('#summaryTable').show();
            createTableHeaders('summaryTableHeader', Object.keys(response[0]));
            createTableRows('summaryTableBody', response);
        },
        error: function() {
            alert("Error retrieving summary data.");
        }
    });
}
