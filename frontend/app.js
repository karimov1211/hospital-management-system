const API_URL = "http://localhost:8000/api";

// Data State
let doctors = [];
let patients = [];
let queue = [];

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    updateCurrentDate();
    initNavigation();
    fetchAllData();
    setupForms();
});

async function fetchAllData() {
    try {
        const [docsRes, patsRes, queueRes] = await Promise.all([
            fetch(`${API_URL}/doctors/`),
            fetch(`${API_URL}/patients/`),
            fetch(`${API_URL}/queue/`)
        ]);

        doctors = await docsRes.json();
        patients = await patsRes.json();
        queue = await queueRes.json();

        renderAll();
    } catch (error) {
        console.error("Ma'lumotlarni yuklashda xatolik:", error);
    }
}

function updateCurrentDate() {
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    document.getElementById('current-date').innerText = new Date().toLocaleDateString('uz-UZ', options);
}

// Navigation
function initNavigation() {
    const links = document.querySelectorAll('.nav-menu a');
    links.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const sectionId = link.getAttribute('data-section');
            switchSection(sectionId);
        });
    });
}

window.switchSection = (sectionId) => {
    document.querySelectorAll('.nav-menu a').forEach(l => {
        l.classList.remove('active');
        if(l.getAttribute('data-section') === sectionId) l.classList.add('active');
    });
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    document.getElementById(sectionId).classList.add('active');
    window.scrollTo({ top: 0, behavior: 'smooth' });
    if(sectionId !== 'home') fetchAllData();
};

// Render Functions
function renderAll() {
    renderStats();
    renderDoctors();
    renderPatients();
    renderQueue();
    updateSelects();
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
            <td><button class="btn" style="color: var(--accent)" onclick="deleteDoctor(${doc.id})"><i data-lucide="trash-2"></i></button></td>
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
            <td><span class="status-badge status-completed">Ro'yxatda</span></td>
        </tr>
    `).join('');
}

function renderQueue() {
    const fullTbody = document.querySelector('#full-queue-table tbody');
    fullTbody.innerHTML = queue.map((q, index) => `
        <tr>
            <td>#${index + 1}</td>
            <td>${q.patient_name}</td>
            <td>${q.doctor_name}</td>
            <td>${q.time}</td>
            <td>
                <button class="btn" onclick="deleteQueue(${q.id})" style="color: var(--accent)"><i data-lucide="trash-2"></i></button>
            </td>
        </tr>
    `).join('');
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
        qForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const pId = document.getElementById('queue-patient-select').value;
            const dId = document.getElementById('queue-doctor-select').value;
            
            const newItem = {
                patient: parseInt(pId),
                doctor: parseInt(dId),
                time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
                status: 'waiting'
            };

            await fetch(`${API_URL}/queue/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(newItem)
            });
            
            fetchAllData();
            qForm.reset();
        });
    }
}

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
            <div class="input-group"><label>Ism-sharif</label><input id="m-doc-name" type="text"></div>
            <div class="input-group"><label>Mutaxassislik</label><input id="m-doc-spec" type="text"></div>
            <div class="input-group"><label>Xona</label><input id="m-doc-room" type="text"></div>
        `;
    } else {
        mTitle.innerText = "Yangi bemor";
        mContent.innerHTML = `
            <div class="input-group"><label>Ism-sharif</label><input id="m-pat-name" type="text"></div>
            <div class="input-group"><label>Telefon</label><input id="m-pat-phone" type="text"></div>
            <div class="input-group"><label>Yosh</label><input id="m-pat-age" type="number"></div>
        `;
    }
};

window.closeModal = () => { overlay.style.display = 'none'; };

document.getElementById('modal-save-btn').addEventListener('click', async () => {
    let endpoint = currentModalType === 'doctor' ? '/doctors/' : '/patients/';
    let data = {};

    if(currentModalType === 'doctor') {
        data = {
            name: document.getElementById('m-doc-name').value,
            specialty: document.getElementById('m-doc-spec').value,
            room: document.getElementById('m-doc-room').value
        };
    } else {
        data = {
            name: document.getElementById('m-pat-name').value,
            phone: document.getElementById('m-pat-phone').value,
            age: parseInt(document.getElementById('m-pat-age').value)
        };
    }

    if(data.name) {
        await fetch(`${API_URL}${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        fetchAllData();
        closeModal();
    }
});

window.deleteDoctor = async (id) => {
    await fetch(`${API_URL}/doctors/${id}/`, { method: 'DELETE' });
    fetchAllData();
};

window.deleteQueue = async (id) => {
    await fetch(`${API_URL}/queue/${id}/`, { method: 'DELETE' });
    fetchAllData();
};
