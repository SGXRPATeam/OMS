export type InquiryType = "complaint" | "inquiry" | "dispute";

export type InquiryStatus =
  | "Open"
  | "In Progress"
  | "Resolved";

export type Inquiry = {
  id: string;
  type: InquiryType;
  category: string;
  description: string;
  status: InquiryStatus;
  createdAt: string;
};