"use client";

import { MessageCircleQuestion, AlertTriangle, Scale } from "lucide-react";
import { Inquiry, InquiryType } from "@/types/inquiry";

type Props = {
  activeType: InquiryType | null;
  setActiveType: (type: InquiryType) => void;
};

const cards = [
  {
    id: "complaint" as InquiryType,
    title: "Raise a Complaint",
    subtitle: "Report an issue or problem",
    icon: AlertTriangle,
    gradient: "from-orange-500 to-red-500",
    border: "border-red-200",
    activeBorder: "border-red-400 ring-2 ring-red-100",
  },
  {
    id: "inquiry" as InquiryType,
    title: "Inquiry",
    subtitle: "Ask a question or request information",
    icon: MessageCircleQuestion,
    gradient: "from-blue-500 to-cyan-500",
    border: "border-blue-200",
    activeBorder: "border-blue-400 ring-2 ring-blue-100",
  },
  {
    id: "dispute" as InquiryType,
    title: "Dispute",
    subtitle: "Dispute an order or transaction",
    icon: Scale,
    gradient: "from-purple-500 to-pink-500",
    border: "border-purple-200",
    activeBorder: "border-purple-400 ring-2 ring-purple-100",
  },
];

export default function InquiryCards({
  activeType,
  setActiveType,
}: Props) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {cards.map((card) => {
        const Icon = card.icon;
        const active = activeType === card.id;

        return (
          <button
            key={card.id}
            onClick={() => setActiveType(card.id)}
            className={`
              bg-white rounded-2xl border p-8 text-left
              shadow-sm hover:shadow-md transition-all duration-300
              ${active ? card.activeBorder : card.border}
            `}
          >
            <div
              className={`
                w-16 h-16 rounded-2xl mb-6
                bg-gradient-to-r ${card.gradient}
                flex items-center justify-center
                shadow-lg
              `}
            >
              <Icon className="w-8 h-8 text-white" />
            </div>

            <h3 className="text-2xl font-semibold text-gray-900 mb-3">
              {card.title}
            </h3>

            <p className="text-gray-500 text-lg">
              {card.subtitle}
            </p>
          </button>
        );
      })}
    </div>
  );
}