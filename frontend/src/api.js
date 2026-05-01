import axios from "axios";

export const sendMessage = async (message) => {
  const res = await axios.post("http://127.0.0.1:8000/chat", {
    message,
  });
  return res.data.response;
};