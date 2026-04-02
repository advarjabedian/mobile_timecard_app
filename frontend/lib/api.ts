// Change this to your Render backend URL after deploying
const API_BASE = "http://10.0.2.2:8000/api"; // Android emulator -> host machine

export interface Employee {
  id: number;
  number: number;
  first_name: string;
  last_name: string;
  full_name: string;
  job_title: string;
  department: string;
  schedule: {
    [day: string]: { in: string | null; out: string | null };
  };
}

export interface PunchRecord {
  id: number;
  employee_id: number;
  scan_date: string;
  scan_time: string;
  working: boolean;
  punch_type: string;
}

export async function loginByNumber(number: string): Promise<Employee> {
  const res = await fetch(`${API_BASE}/login/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ number }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.error || "Login failed");
  }
  return res.json();
}

export async function punchIn(employeeId: number): Promise<PunchRecord> {
  const res = await fetch(`${API_BASE}/punch-in/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ employee_id: employeeId }),
  });
  if (!res.ok) throw new Error("Punch in failed");
  return res.json();
}

export async function punchOut(employeeId: number): Promise<PunchRecord> {
  const res = await fetch(`${API_BASE}/punch-out/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ employee_id: employeeId }),
  });
  if (!res.ok) throw new Error("Punch out failed");
  return res.json();
}

export async function getTodayPunches(employeeId: number): Promise<PunchRecord[]> {
  const res = await fetch(`${API_BASE}/today/${employeeId}/`);
  if (!res.ok) throw new Error("Failed to load today's punches");
  return res.json();
}

export async function getCurrentStatus(employeeId: number): Promise<{
  is_punched_in: boolean;
  last_punch: PunchRecord | null;
}> {
  const res = await fetch(`${API_BASE}/status/${employeeId}/`);
  if (!res.ok) throw new Error("Failed to get status");
  return res.json();
}
