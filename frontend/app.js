const API_URL = "/api";

let doctors = [];
let patients = [];
let queue = [];

document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    fetchAllData();
    setupForms();
    setupModalSave();
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
        showToast("Server bilan bog'lanishda xatolik!", "error");
    }
}

function initNavigation() {
    const links = document.querySelectorAll('.nav-menu a');
    links.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            switchSection(link.getAttribute('data-section'));
        });
    });
}

window.switchSection = (sectionId) => {
    document.querySelectorAll('.nav-menu a').forEach(l => {
        l.classList.remove('active');
        if (l.getAttribute('data-section') === sectionId) l.classList.add('active');
    });
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    const target = document.getElementById(sectionId);
    if (target) {
        target.classList.add('active');
        target.style.animation = 'none';
        target.offsetHeight;
        target.style.animation = 'fadeInUp 0.4s ease';
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
    fetchAllData();
};

function renderAll() {
    renderDoctors();
    renderPatients();
    renderQueue();
    updateSelects();
    lucide.createIcons();
}

function renderDoctors() {
    const tbody = document.querySelector('#doctors-table tbody');
    document.getElementById('doctors-count').textContent = doctors.length;
    if (doctors.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="empty-row">Shifokorlar ro\'yxati bo\'sh</td></tr>';
        return;
    }
    tbody.innerHTML = doctors.map((doc, i) => `
        <tr>
            <td><span class="row-num">${i + 1}</span></td>
            <td><strong class="person-name">${doc.name}</strong></td>
            <td><span class="specialty-badge">${doc.specialty}</span></td>
            <td><span class="room-badge"><i data-lucide="door-open" style="width:13px;height:13px;vertical-align:middle;margin-right:3px;"></i>${doc.room}-xona</span></td>
            <td>
                <button class="btn-icon btn-delete" onclick="deleteDoctor(${doc.id})" title="O'chirish">
                    <i data-lucide="trash-2"></i>
                </button>
            </td>
        </tr>
    `).join('');
    lucide.createIcons();
}

function renderPatients() {
    const tbody = document.querySelector('#patients-table tbody');
    document.getElementById('patients-count').textContent = patients.length;
    if (patients.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="empty-row">Bemorlar ro\'yxati bo\'sh</td></tr>';
        return;
    }
    tbody.innerHTML = patients.map((p, i) => `
        <tr>
            <td><span class="row-num">${i + 1}</span></td>
            <td><strong class="person-name">${p.name}</strong></td>
            <td>${p.phone}</td>
            <td>${p.age} yosh</td>
            <td>
                <button class="btn-icon btn-delete" onclick="deletePatient(${p.id})" title="O'chirish">
                    <i data-lucide="trash-2"></i>
                </button>
            </td>
        </tr>
    `).join('');
    lucide.createIcons();
}

function renderQueue() {
    const tbody = document.querySelector('#full-queue-table tbody');
    document.getElementById('queue-count').textContent = queue.length;
    if (queue.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="empty-row">Hozircha navbat yo\'q</td></tr>';
        return;
    }
    tbody.innerHTML = queue.map((q, i) => `
        <tr>
            <td><span class="row-num">#${i + 1}</span></td>
            <td><strong class="person-name">${q.patient_name || '—'}</strong></td>
            <td>${q.doctor_name || '—'}</td>
            <td><span class="time-badge"><i data-lucide="clock" style="width:12px;height:12px;vertical-align:middle;margin-right:3px;"></i>${q.time}</span></td>
            <td><span class="status-badge ${q.status === 'kutilmoqda' ? 'status-waiting' : 'status-done'}">${q.status}</span></td>
            <td>
                <button class="btn-icon btn-delete" onclick="deleteQueue(${q.id})" title="O'chirish">
                    <i data-lucide="trash-2"></i>
                </button>
            </td>
        </tr>
    `).join('');
    lucide.createIcons();
}

function updateSelects() {
    const pSelect = document.getElementById('queue-patient-select');
    const dSelect = document.getElementById('queue-doctor-select');
    if (pSelect) pSelect.innerHTML = patients.map(p => `<option value="${p.id}">${p.name}</option>`).join('');
    if (dSelect) dSelect.innerHTML = doctors.map(d => `<option value="${d.id}">${d.name} (${d.specialty})</option>`).join('');
}

function setupForms() {
    const qForm = document.getElementById('queue-form');
    if (qForm) {
        qForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const pId = document.getElementById('queue-patient-select').value;
            const dId = document.getElementById('queue-doctor-select').value;
            const newItem = {
                patient: parseInt(pId),
                doctor: parseInt(dId),
                time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
                status: 'kutilmoqda'
            };
            await fetch(`${API_URL}/queue/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(newItem)
            });
            showToast("Navbatga qo'shildi!", "success");
            fetchAllData();
        });
    }
}

// Modal Logic
let currentModalType = '';

window.showModal = (type) => {
    currentModalType = type;
    const overlay = document.getElementById('modal-overlay');
    const mTitle = document.getElementById('modal-title');
    const mContent = document.getElementById('modal-content');
    overlay.style.display = 'flex';
    if (type === 'doctor') {
        mTitle.innerText = "Yangi Shifokor Qo'shish";
        mContent.innerHTML = `
            <div class="input-group"><label>Ism-sharif</label><input id="m-doc-name" type="text" placeholder="Masalan: Aliyev Baxtiyor Saidovich"></div>
            <div class="input-group"><label>Mutaxassislik</label><input id="m-doc-spec" type="text" placeholder="Masalan: Kardiolog"></div>
            <div class="input-group"><label>Xona raqami</label><input id="m-doc-room" type="text" placeholder="Masalan: 101"></div>
        `;
    } else {
        mTitle.innerText = "Yangi Bemor Qo'shish";
        mContent.innerHTML = `
            <div class="input-group"><label>Ism-sharif</label><input id="m-pat-name" type="text" placeholder="Masalan: Yusupova Malika"></div>
            <div class="input-group"><label>Telefon raqam</label><input id="m-pat-phone" type="text" placeholder="+998 90 000 00 00"></div>
            <div class="input-group"><label>Yoshi</label><input id="m-pat-age" type="number" placeholder="Masalan: 35"></div>
        `;
    }
    lucide.createIcons();
};

window.closeModal = () => {
    document.getElementById('modal-overlay').style.display = 'none';
};

function setupModalSave() {
    document.getElementById('modal-save-btn').addEventListener('click', async () => {
        let endpoint = currentModalType === 'doctor' ? '/doctors/' : '/patients/';
        let data = {};
        if (currentModalType === 'doctor') {
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
        if (data.name) {
            await fetch(`${API_URL}${endpoint}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            showToast("Muvaffaqiyatli saqlandi!", "success");
            fetchAllData();
            closeModal();
        } else {
            showToast("Ism-sharif kiritish shart!", "error");
        }
    });
}

window.deleteDoctor = async (id) => {
    if (!confirm("Shifokorni o'chirishni tasdiqlaysizmi?")) return;
    await fetch(`${API_URL}/doctors/${id}/`, { method: 'DELETE' });
    showToast("Shifokor o'chirildi", "success");
    fetchAllData();
};

window.deletePatient = async (id) => {
    if (!confirm("Bemorni o'chirishni tasdiqlaysizmi?")) return;
    await fetch(`${API_URL}/patients/${id}/`, { method: 'DELETE' });
    showToast("Bemor o'chirildi", "success");
    fetchAllData();
};

window.deleteQueue = async (id) => {
    await fetch(`${API_URL}/queue/${id}/`, { method: 'DELETE' });
    showToast("Navbat o'chirildi", "success");
    fetchAllData();
};

function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast toast-${type} show`;
    setTimeout(() => { toast.className = 'toast'; }, 3000);
}
