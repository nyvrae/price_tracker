import axios from "./axios";

export const loginUser = async (email: string, password: string) => {
  const res = await axios.post("/auth/login", { username: email, password });
  return res.data;
};

export const registerUser = async (email: string, password: string) => {
  const res = await axios.post("/auth/register", { email, password });
  return res.data;
};

export const getCurrentUser = async () => {
  const res = await axios.get("/auth/me");
  return res.data;
};
