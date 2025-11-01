const BASE_URL = "http://localhost:8000/api";

export async function calculateBalance(inputData) {
  const res = await fetch(`${BASE_URL}/calc`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(inputData),
  });
  return await res.json();
}

export async function getComment(data) {
  const res = await fetch(`${BASE_URL}/comment`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return await res.json();
}
