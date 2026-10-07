const studentForm = document.getElementById("studentForm");

const rollNo = document.getElementById("rollNo");
const studentName = document.getElementById("studentName");
const email = document.getElementById("email");

const studentMessage = document.getElementById("studentMessage");

const attendanceStudent =
    document.getElementById("attendanceStudent");

const attendanceDate =
    document.getElementById("attendanceDate");

const attendanceStatus =
    document.getElementById("attendanceStatus");

const attendanceMessage =
    document.getElementById("attendanceMessage");

const studentsTableBody =
    document.getElementById("studentsTableBody");

const summaryTableBody =
    document.getElementById("summaryTableBody");

const recordsTableBody =
    document.getElementById("recordsTableBody");

const recordDate =
    document.getElementById("recordDate");

const markAttendanceBtn =
    document.getElementById("markAttendanceBtn");

const loadRecordsBtn =
    document.getElementById("loadRecordsBtn");

const loadAllRecordsBtn =
    document.getElementById("loadAllRecordsBtn");


/* Set today's date */

const today = new Date().toISOString().split("T")[0];

attendanceDate.value = today;


/* Load students */

async function loadStudents() {

    const response = await fetch("/api/students");

    const students = await response.json();

    studentsTableBody.innerHTML = "";

    attendanceStudent.innerHTML =
        '<option value="">Select Student</option>';


    students.forEach(student => {

        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${student.roll_no}</td>
            <td>${student.name}</td>
            <td>${student.email || "-"}</td>
        `;

        studentsTableBody.appendChild(row);


        const option = document.createElement("option");

        option.value = student.id;

        option.textContent =
            `${student.roll_no} - ${student.name}`;

        attendanceStudent.appendChild(option);

    });

}


/* Register student */

studentForm.addEventListener("submit", async function(event) {

    event.preventDefault();


    const data = {

        roll_no: rollNo.value,

        name: studentName.value,

        email: email.value

    };


    const response = await fetch(
        "/api/students",
        {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(data)

        }
    );


    const result = await response.json();


    if (response.ok) {

        studentMessage.textContent =
            result.message;

        studentMessage.style.color = "green";


        studentForm.reset();


        await loadStudents();

        await loadSummary();

    } else {

        studentMessage.textContent =
            result.error;

        studentMessage.style.color = "red";

    }

});


/* Mark attendance */

markAttendanceBtn.addEventListener(
    "click",
    async function() {

        const data = {

            student_id:
                attendanceStudent.value,

            attendance_date:
                attendanceDate.value,

            status:
                attendanceStatus.value

        };


        const response = await fetch(
            "/api/attendance",
            {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(data)

            }
        );


        const result = await response.json();


        if (response.ok) {

            attendanceMessage.textContent =
                result.message;

            attendanceMessage.style.color =
                "green";


            await loadSummary();

            await loadRecords();

        } else {

            attendanceMessage.textContent =
                result.error;

            attendanceMessage.style.color =
                "red";

        }

    }
);


/* Load attendance summary */

async function loadSummary() {

    const response =
        await fetch("/api/summary");

    const summary =
        await response.json();


    summaryTableBody.innerHTML = "";


    summary.forEach(student => {

        const row =
            document.createElement("tr");


        row.innerHTML = `

            <td>${student.roll_no}</td>

            <td>${student.name}</td>

            <td>${student.total}</td>

            <td>${student.present}</td>

            <td>${student.percentage}%</td>

        `;


        summaryTableBody.appendChild(row);

    });

}


/* Load attendance records */

async function loadRecords(selectedDate = "") {

    let url = "/api/records";


    if (selectedDate) {

        url +=
            "?date=" +
            encodeURIComponent(selectedDate);

    }


    const response =
        await fetch(url);

    const records =
        await response.json();


    recordsTableBody.innerHTML = "";


    records.forEach(record => {

        const row =
            document.createElement("tr");


        row.innerHTML = `

            <td>${record.attendance_date}</td>

            <td>${record.roll_no}</td>

            <td>${record.name}</td>

            <td>${record.status}</td>

        `;


        recordsTableBody.appendChild(row);

    });

}


/* Load records for selected date */

loadRecordsBtn.addEventListener(
    "click",
    function() {

        loadRecords(recordDate.value);

    }
);


/* Load all records */

loadAllRecordsBtn.addEventListener(
    "click",
    function() {

        recordDate.value = "";

        loadRecords();

    }
);


/* Initial page loading */

async function initializeApp() {

    await loadStudents();

    await loadSummary();

    await loadRecords();

}


initializeApp();