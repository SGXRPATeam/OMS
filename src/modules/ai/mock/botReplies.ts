export function getBotReply(message: string) {
  const msg = message.toLowerCase();

  if (msg.includes("track")) {
    return "Please share your Order ID (example: ORD001) to track status.";
  }

  if (msg.includes("create")) {
    return "Click 'Create Order' on dashboard or provide order details here.";
  }

  if (msg.includes("complaint")) {
    return "Please provide Order ID and issue details. I'll help raise a complaint.";
  }

  if (msg.includes("ord001")) {
    return "Order ORD001 is currently Processing and expected delivery is Apr 26.";
  }

  return "I can help you track orders, create orders, or raise complaints.";
}