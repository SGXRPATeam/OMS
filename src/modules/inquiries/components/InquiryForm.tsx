"use client";

import { useState } from "react";
import type { InquiryType } from "@/types/inquiry";
import {
  inquiryOptions,
  complaintOptions,
  disputeOptions,
} from "@/constants/inquiryOptions";

type Props = {
  type: InquiryType;
  onSubmit: (
    category: string,
    description: string
  ) => void;
};  

export default function InquiryForm({ type , onSubmit,}: Props) {
  const [category, setCategory] = useState("");
  const [description, setDescription] = useState("");

  const getTitle = () => {
    if (type === "complaint") return "Complaint Type";
    if (type === "inquiry") return "Inquiry Type";
    return "Dispute Type";
  };

  const getButtonText = () => {
    if (type === "complaint") return "Submit Complaint";
    if (type === "inquiry") return "Submit Inquiry";
    return "Submit Dispute";
  };

  const getOptions = () => {
    if (type === "complaint") return complaintOptions;
    if (type === "inquiry") return inquiryOptions;
    return disputeOptions;
  };

  const handleSubmit = () => {
    if (!category || !description.trim()) {
      alert("Please fill all required fields");
      return;
    }

            onSubmit(category, description);
alert(`${getButtonText()} successful`);

setCategory("");
setDescription("");
        };

  return (
    <div className="space-y-6">
      {/* Dropdown */}
      <div>
        <label className="block text-sm font-medium mb-2 text-gray-700">
          {getTitle()} *
        </label>

        <select
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          className="w-full border rounded-xl px-4 py-3 outline-none focus:ring-2 focus:ring-primary"
        >
          <option value="">Select {getTitle()}</option>

          {getOptions().map((option) => (
            <option key={option}>{option}</option>
          ))}
        </select>
      </div>

      {/* Description */}
      <div>
        <label className="block text-sm font-medium mb-2 text-gray-700">
          Description *
        </label>

        <textarea
          rows={5}
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Enter details..."
          className="w-full border rounded-xl px-4 py-3 outline-none focus:ring-2 focus:ring-primary resize-none"
        />
      </div>

      {/* Button */}
      <div className="flex justify-end gap-3">
  {/* Cancel */}
  <button
    type="button"
    onClick={() => {
      setCategory("");
      setDescription("");
    }}
    className="px-6 py-3 rounded-xl border border-gray-300 text-gray-700 font-medium hover:bg-gray-50 transition"
  >
    Cancel
  </button>

  {/* Submit */}
  <button
    type="button"
    onClick={handleSubmit}
    className="bg-primary text-white px-6 py-3 rounded-xl font-medium hover:opacity-90 transition"
  >
    {getButtonText()}
  </button>
</div>
    </div>
  );
}