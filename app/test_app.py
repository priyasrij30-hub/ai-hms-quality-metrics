"""
Correctness & Reliability tests for QuickMed (AI-enabled HMS project)
Place this file in the SAME folder as app.py (QuickMed\\app) and run:  pytest -v

Tests marked  # EXPECTED DEFECT  check behaviour the app SHOULD have.
If they fail, the app has a real defect -> record it for defect density.
"""
import uuid
import pytest
from app import app as flask_app, init_db


def unique_user():
    u = uuid.uuid4().hex[:8]
    return {
        "firstname": "Test",
        "lastname": "User",
        "email": f"test_{u}@example.com",
        "number": "9876543210",
        "password": "Test@1234",
    }


PATIENT = {
    "name": "Ravi Kumar",
    "dob": "1980-05-12",
    "contact": "9876543210",
    "medical-history": "Diabetes",
}

PROTECTED_PAGES = [
    "/",
    "/register-patient",
    "/appointments",
    "/patient-list",
    "/staff-management",
    "/view-appointments",
    "/view-staff",
]


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


@pytest.fixture
def logged_in_client(client):
    user = unique_user()
    client.post("/signup", data=user)
    client.post("/login", data={"email": user["email"], "password": user["password"]})
    return client


def is_logged_in(client):
    with client.session_transaction() as s:
        return "user_id" in s


# ================= 1. Page availability =================
@pytest.mark.parametrize("url", ["/login", "/signup"])
def test_public_pages_load(client, url):
    assert client.get(url).status_code == 200


def test_unknown_page_returns_404(client):
    assert client.get("/no-such-page").status_code == 404


# ================= 2. Authentication =================
def test_signup_redirects_to_login(client):
    res = client.post("/signup", data=unique_user())
    assert res.status_code == 302 and "/login" in res.headers["Location"]


def test_duplicate_email_signup_is_handled(client):
    user = unique_user()
    client.post("/signup", data=user)
    res = client.post("/signup", data=user)
    assert res.status_code == 200          # stays on signup page, no crash


def test_signup_missing_field_does_not_crash(client):
    res = client.post("/signup", data={"email": "x@example.com"})
    assert res.status_code != 500


def test_login_correct_password(client):
    user = unique_user()
    client.post("/signup", data=user)
    client.post("/login", data={"email": user["email"], "password": user["password"]})
    assert is_logged_in(client)


def test_login_wrong_password_rejected(client):
    user = unique_user()
    client.post("/signup", data=user)
    client.post("/login", data={"email": user["email"], "password": "wrong"})
    assert not is_logged_in(client)


def test_login_empty_fields_rejected(client):
    client.post("/login", data={})
    assert not is_logged_in(client)


def test_logout_clears_session(logged_in_client):
    logged_in_client.get("/logout")
    assert not is_logged_in(logged_in_client)


def test_password_stored_hashed(client):
    import sqlite3
    user = unique_user()
    client.post("/signup", data=user)
    conn = sqlite3.connect("quickmed.db")
    stored = conn.execute("SELECT password FROM users WHERE email=?",
                          (user["email"],)).fetchone()[0]
    conn.close()
    assert stored != user["password"]


# ================= 3. Access control =================
@pytest.mark.parametrize("url", PROTECTED_PAGES)
def test_protected_page_redirects_without_login(client, url):
    res = client.get(url)
    assert res.status_code == 302 and "/login" in res.headers["Location"]


@pytest.mark.parametrize("url", PROTECTED_PAGES)
def test_protected_page_opens_after_login(logged_in_client, url):
    assert logged_in_client.get(url).status_code == 200


# ================= 4. Core features =================
def test_register_patient(logged_in_client):
    res = logged_in_client.post("/register-patient", data=PATIENT)
    assert res.status_code == 302


def test_add_staff(logged_in_client):
    res = logged_in_client.post("/staff-management",
                                data={"staff-name": "Dr. Meena", "role": "Doctor"})
    assert res.status_code == 302


def test_added_staff_appears_in_list(logged_in_client):
    name = f"Staff_{uuid.uuid4().hex[:6]}"
    logged_in_client.post("/staff-management", data={"staff-name": name, "role": "Nurse"})
    assert name.encode() in logged_in_client.get("/view-staff").data


def test_schedule_appointment(logged_in_client):
    logged_in_client.post("/register-patient", data=PATIENT)
    res = logged_in_client.post("/appointments",
                                data={"patient-id": "1", "date": "2026-11-01", "time": "10:30"})
    assert res.status_code == 302


def test_patient_missing_field_does_not_crash(logged_in_client):
    res = logged_in_client.post("/register-patient", data={"name": "Only Name"})
    assert res.status_code != 500


# ================= 5. Expected defects (validation & reliability) =================
def count_rows(sql, params=()):
    import sqlite3
    conn = sqlite3.connect("quickmed.db")
    n = conn.execute(sql, params).fetchone()[0]
    conn.close()
    return n


def test_empty_patient_name_rejected(logged_in_client):          # EXPECTED DEFECT
    before = count_rows("SELECT COUNT(*) FROM patients WHERE name = ''")
    logged_in_client.post("/register-patient", data={**PATIENT, "name": ""})
    after = count_rows("SELECT COUNT(*) FROM patients WHERE name = ''")
    assert after == before, "Patient with empty name was saved"


def test_invalid_dob_rejected(logged_in_client):                 # EXPECTED DEFECT
    bad = f"bad-date-{uuid.uuid4().hex[:6]}"
    logged_in_client.post("/register-patient", data={**PATIENT, "dob": bad})
    assert count_rows("SELECT COUNT(*) FROM patients WHERE dob = ?", (bad,)) == 0, \
        "Patient with invalid date of birth was saved"


def test_appointment_for_nonexistent_patient_rejected(logged_in_client):  # EXPECTED DEFECT
    before = count_rows("SELECT COUNT(*) FROM appointments WHERE patient_id = 999999")
    logged_in_client.post("/appointments",
                          data={"patient-id": "999999", "date": "2026-11-01", "time": "10:30"})
    after = count_rows("SELECT COUNT(*) FROM appointments WHERE patient_id = 999999")
    assert after == before, "Appointment saved for a patient that does not exist"


def test_users_survive_app_restart(client):                      # EXPECTED DEFECT
    user = unique_user()
    client.post("/signup", data=user)
    init_db()                       # same thing that happens when the app restarts
    client.post("/login", data={"email": user["email"], "password": user["password"]})
    assert is_logged_in(client)
