"use client";

import { useState } from "react";
import { UserPlus, RotateCcw } from "lucide-react";

export default function RegisterUserPage() {
  const [form, setForm] = useState({
    first_name: "",
    last_name: "",
    display_name: "",
    email: "",
    phone: "",
    employee_code: "",
    department: "",
    designation: "",
    role_code: "USER",
    password: "",
    confirmPassword: "",
  });

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLSelectElement
    >
  ) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const resetForm = () => {
    setForm({
      first_name: "",
      last_name: "",
      display_name: "",
      email: "",
      phone: "",
      employee_code: "",
      department: "",
      designation: "",
      role_code: "USER",
      password: "",
      confirmPassword: "",
    });
    setMessage("");
    setError("");
  };

  const handleSubmit = async (
    e: React.FormEvent
  ) => {
    e.preventDefault();

    setMessage("");
    setError("");

    if (form.password !== form.confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    try {
      setLoading(true);

      const res = await fetch(
        "http://127.0.0.1:8000/users/register",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            first_name: form.first_name,
            last_name: form.last_name,
            display_name: form.display_name,
            email: form.email,
            phone: form.phone,
            employee_code: form.employee_code,
            department: form.department,
            designation: form.designation,
            role_code: form.role_code,
            password: form.password,
          }),
        }
      );

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || "Registration failed");
      }

      setMessage(
        `User created successfully (${data.userid})`
      );

      resetForm();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fields = [
    ["First Name", "first_name"],
    ["Last Name", "last_name"],
    ["Display Name", "display_name"],
    ["Email Address", "email"],
    ["Phone Number", "phone"],
    ["Employee Code", "employee_code"],
    ["Department", "department"],
    ["Designation", "designation"],
  ];

  return (
    <div className="max-w-7xl mx-auto space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-semibold text-gray-900">
          Register User
        </h1>

        <p className="mt-2 text-gray-500 text-base">
          Create and onboard new OMS users
        </p>
      </div>

      {/* Card */}
      <div className="bg-white rounded-3xl border border-gray-200 shadow-[0_10px_40px_rgba(0,0,0,0.06)] overflow-hidden">
        {/* top strip */}
        <div className="px-8 py-6 border-b bg-gradient-to-r from-blue-50 to-indigo-50">
          <h2 className="text-xl font-semibold text-gray-900">
            User Information
          </h2>
          <p className="text-sm text-gray-500 mt-1">
            Fill in user details below
          </p>
        </div>

        {/* form */}
        <form
          onSubmit={handleSubmit}
          className="p-8 space-y-8"
        >
          {/* fields */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {fields.map(([label, name]) => (
              <ModernInput
                key={name}
                label={label}
                name={name}
                value={
                  form[name as keyof typeof form]
                }
                onChange={handleChange}
              />
            ))}

            {/* role */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Role
              </label>

              <select
                name="role_code"
                value={form.role_code}
                onChange={handleChange}
                className="w-full h-12 px-4 rounded-xl border border-gray-300 bg-white outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition"
              >
                <option value="USER">User</option>
                <option value="TENANT_ADMIN">
                  Tenant Admin
                </option>
                <option value="SUPER_ADMIN">
                  Super Admin
                </option>
              </select>
            </div>

            <ModernInput
              label="Password"
              name="password"
              type="password"
              value={form.password}
              onChange={handleChange}
            />

            <ModernInput
              label="Confirm Password"
              name="confirmPassword"
              type="password"
              value={form.confirmPassword}
              onChange={handleChange}
            />
          </div>

          {/* alerts */}
          {error && (
            <div className="rounded-2xl border border-red-200 bg-red-50 px-5 py-4 text-red-600 text-sm">
              {error}
            </div>
          )}

          {message && (
            <div className="rounded-2xl border border-green-200 bg-green-50 px-5 py-4 text-green-700 text-sm font-medium">
              {message}
            </div>
          )}

          {/* actions */}
          <div className="flex gap-4 pt-2">
            <button
              type="submit"
              disabled={loading}
              className="inline-flex items-center gap-2 bg-primary text-white px-7 h-12 rounded-xl font-medium shadow-md hover:opacity-90 transition"
            >
              <UserPlus size={18} />
              {loading
                ? "Creating..."
                : "Create User"}
            </button>

            <button
              type="button"
              onClick={resetForm}
              className="inline-flex items-center gap-2 border border-gray-300 bg-white text-gray-700 px-7 h-12 rounded-xl font-medium hover:bg-gray-50 transition"
            >
              <RotateCcw size={16} />
              Reset
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

function ModernInput({
  label,
  name,
  value,
  onChange,
  type = "text",
}: any) {
  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-2">
        {label}
      </label>

      <input
        type={type}
        name={name}
        value={value}
        onChange={onChange}
        className="w-full h-12 px-4 rounded-xl border border-gray-300 bg-white outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition"
      />
    </div>
  );
}