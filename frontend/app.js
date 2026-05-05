// Data State
let doctors = JSON.parse(localStorage.getItem('medcare_doctors')) || [
    { id: 1, name: "Dr. Alisher Vohidov", specialty: "Kardiolog", room: "102" },
    { id: 2, name: "Dr. Malika Ahmedova", specialty: "Nevropatolog", room: "205" }
];

let patients = JSON.parse(localStorage.getItem('medcare_patients')) || [
    { id: 1, name: "Jasur Karimov", phone: "+998 90 123 45 67", age: 28 },
    { id: 2, name: "Olima Ergasheva", phone: "+998 93 987 65 43", age: 45 }
];

let queue = JSON.parse(localStorage.getItem('medcare_queue')) || [];

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    updateCurrentDate();
    initNavigation();
    renderAll();
    setupForms();
});

function updateCurrentDate() {
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    document.getElementById('current-date').innerText = new Date().toLocaleDateString('uz-UZ', options);
}

// Navigation
function initNavigation() {
    const links = document.querySelectorAll('.nav-link');
    links.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const sectionId = link.getAttribute('data-section');
            
            // Toggle active link
            links.forEach(l => l.classList.remove('active'));
            link.classList.add('active');

            // Toggle sections
            document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
            document.getElementById(sectionId).classList.add('active');

            // Update title
            document.getElementById('page-title').innerText = link.innerText.trim();
            
            renderAll();
        });
    });
}

// Render Functions
function renderAll() {
    renderStats();
    renderDoctors();
    renderPatients();
    renderQueue();
    updateSelects();
    localStorage.setItem('medcare_doctors', JSON.stringify(doctors));
    localStorage.setItem('medcare_patients', JSON.stringify(patients));
    localStorage.setItem('medcare_queue', JSON.stringify(queue));
}

function renderStats() {
    document.getElementById('stat-total-patients').innerText = patients.length;
    document.getElementById('stat-total-doctors').innerText = doctors.length;
    document.getElementById('stat-pending').innerText = queue.filter(q => q.status === 'waiting').length;
}

function renderDoctors() {
    const tbody = document.querySelector('#doctors-table tbody');
    tbody.innerHTML = doctors.map(doc => `
        <tr>
            <td><strong>${doc.name}</strong></td>
            <td>${doc.specialty}</td>
            <td>${doc.room}-xona</td>
            <td><button class="btn" style="color: var(--danger)" onclick="deleteDoctor(${doc.id})"><i data-lucide="trash-2"></i></button></td>
        </tr>
    `).join('');
    lucide.createIcons();
}

function renderPatients() {
    const tbody = document.querySelector('#patients-table tbody');
    tbody.innerHTML = patients.map(p => `
        <tr>
            <td><strong>${p.name}</strong></td>
            <td>${p.phone}</td>
            <td>${p.age} yosh</td>
            <td>Bugun</td>
        </tr>
    `).join('');
}

function renderQueue() {
    const dashTbody = document.querySelector('#dashboard-queue-table tbody');
    const fullTbody = document.querySelector('#full-queue-table tbody');

    const queueHtml = queue.map((q, index) => {
        const patient = patients.find(p => p.id == q.patientId) || { name: 'Noma'lum' };
        const doctor = doctors.find(d => d.id == q.doctorId) || { name: 'Noma'lum' };
        
        return {
            html: `
                <tr>
                    <td>${patient.name}</td>
                    <td>${doctor.name}</td>
                    <td>${q.time}</td>
                    <td><span class="status-badge status-${q.status}">${q.status === 'waiting' ? 'Kutilmoqda' : 'Tugallangan'}</span></td>
                </tr>
            `,
            fullHtml: `
                <tr>
                    <td>#${index + 1}</td>
                    <td>${patient.name}</td>
                    <td>${doctor.name}</td>
                    <td>
                        <button class="btn" onclick="completeQueue(${index})" style="color: var(--success)"><i data-lucide="check-circle"></i></button>
                    </td>
                </tr>
            `
        };
    });

    dashTbody.innerHTML = queueHtml.map(x => x.html).join('');
    fullTbody.innerHTML = queueHtml.map(x => x.fullHtml).join('');
    lucide.createIcons();
}

function updateSelects() {
    const pSelect = document.getElementById('queue-patient-select');
    const dSelect = document.getElementById('queue-doctor-select');

    if(pSelect) pSelect.innerHTML = patients.map(p => `<option value="${p.id}">${p.name}</option>`).join('');
    if(dSelect) dSelect.innerHTML = doctors.map(d => `<option value="${d.id}">${d.name} (${d.specialty})</option>`).join('');
}

// Form Logic
function setupForms() {
    const qForm = document.getElementById('queue-form');
    if(qForm) {
        qForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const pId = document.getElementById('queue-patient-select').value;
            const dId = document.getElementById('queue-doctor-select').value;
            
            queue.push({
                patientId: pId,
                doctorId: dId,
                time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
                status: 'waiting'
            });
            
            renderAll();
            qForm.reset();
        });
    }
}

// Actions
window.completeQueue = (index) => {
    queue[index].status = 'completed';
    setTimeout(() => {
        queue.splice(index, 1);
        renderAll();
    }, 500);
    renderAll();
};

window.deleteDoctor = (id) => {
    doctors = doctors.filter(d => d.id !== id);
    renderAll();
};

// Modal Logic
const overlay = document.getElementById('modal-overlay');
const mContent = document.getElementById('modal-content');
const mTitle = document.getElementById('modal-title');
let currentModalType = '';

window.showModal = (type) => {
    currentModalType = type;
    overlay.style.display = 'flex';
    if(type === 'doctor') {
        mTitle.innerText = "Yangi shifokor";
        mContent.innerHTML = `
            <div class="form-group"><label>Ism-sharif</label><input id="m-doc-name" type="text"></div>
            <div class="form-group"><label>Mutaxassislik</label><input id="m-doc-spec" type="text"></div>
            <div class="form-group"><label>Xona</label><input id="m-doc-room" type="text"></div>
        `;
    } else {
        mTitle.innerText = "Yangi bemor";
        mContent.innerHTML = `
            <div class="form-group"><label>Ism-sharif</label><input id="m-pat-name" type="text"></div>
            <div class="form-group"><label>Telefon</label><input id="m-pat-phone" type="text"></div>
            <div class="form-group"><label>Yosh</label><input id="m-pat-age" type="number"></div>
        `;
    }
};

window.closeModal = () => { overlay.style.display = 'none'; };

document.getElementById('modal-save-btn').addEventListener('click', () => {
    if(currentModalType === 'doctor') {
        const name = document.getElementById('m-doc-name').value;
        const spec = document.getElementById('m-doc-spec').value;
        const room = document.getElementById('m-doc-room').value;
        if(name) doctors.push({ id: Date.now(), name, specialty: spec, room });
    } else {
        const name = document.getElementById('m-pat-name').value;
        const phone = document.getElementById('m-pat-phone').value;
        const age = document.getElementById('m-pat-age').value;
        if(name) patients.push({ id: Date.now(), name, phone, age });
    }
    renderAll();
    closeModal();
});
