// 'use client';

// import { useEffect, useState } from 'react';
// import { useSearchParams } from 'next/navigation';
// import { OrderService } from '@/services/order.service';
// import ProductCardList from '@/modules/products/components/ProductCardList';

// const products = [
//   { name: 'Portable ECG Machine', price: 45000 },
//   { name: 'Patient Monitor', price: 85000 },
//   { name: 'Pulse Oximeter', price: 2499 },
//   { name: 'Nebulizer', price: 1999 },
//   { name: 'Infusion Pump', price: 32000 },
//   { name: 'Defibrillator', price: 125000 },
//   { name: 'Ventilator', price: 250000 },
//   { name: 'Wheelchair', price: 8499 },
// ];

// export default function OrderForm() {
//   const searchParams = useSearchParams();
//   const [openProducts, setOpenProducts] = useState(false);

//   const [form, setForm] = useState({
//     account_number: '',
//     product: '',
//     Price: '',
//     quantity: '1',
//     delivery_address: '',
//     order_type: 'STANDARD',
//   });

//   const [unitPrice, setUnitPrice] = useState(0);

//   // URL autofill
//   useEffect(() => {
//     const product = searchParams.get('product') || '';
//     const price = Number(searchParams.get('price')) || 0;

//     if (product && price) {
//       setUnitPrice(price);

//       setForm((prev) => ({
//         ...prev,
//         product,
//         quantity: '1',
//         Price: String(price),
//       }));
//     }
//   }, [searchParams]);

//   // quantity * unit price
//   useEffect(() => {
//     const qty = Number(form.quantity) || 0;
//     const total = qty * unitPrice;

//     setForm((prev) => ({
//       ...prev,
//       Price: total ? String(total) : '',
//     }));
//   }, [form.quantity, unitPrice]);

//   const resetForm = () => {
//     setUnitPrice(0);

//     setForm({
//       account_number: '',
//       product: '',
//       Price: '',
//       quantity: '1',
//       delivery_address: '',
//       order_type: 'STANDARD',
//     });
//   };

//   const handleSubmit = async (e: React.FormEvent) => {
//     e.preventDefault();

//     if (
//       !form.account_number ||
//       !form.product ||
//       !form.quantity ||
//       !form.Price ||
//       !form.delivery_address
//     ) {
//       alert('Please fill all fields');
//       return;
//     }

//     await OrderService.create({
//       ...form,
//       quantity: Number(form.quantity),
//       price: Number(form.Price),
//     });

//     alert('Order created successfully');
//     resetForm();
//   };

//   return (
//     <>
//       <form onSubmit={handleSubmit} className="space-y-5">
//         {/* Account */}
//         <div>
//           <label className="block mb-2 text-sm font-medium">Account Number</label>
//           <input
//             value={form.account_number}
//             placeholder="Account Number"
//             className="w-full border border-gray-300 rounded-xl px-4 py-3"
//             onChange={(e) =>
//               setForm({
//                 ...form,
//                 account_number: e.target.value,
//               })
//             }
//           />
//         </div>

//         {/* Product */}
//         <div>
//           <label className="block mb-2 text-sm font-medium">Product</label>

//           <div
//             onClick={() => setOpenProducts(true)}
//             className="w-full border border-gray-300 rounded-xl px-4 py-3 cursor-pointer bg-white hover:border-primary"
//           >
//             {form.product || 'Select Product'}
//           </div>
//         </div>

//         {/* Quantity */}
//         <div>
//           <label className="block mb-2 text-sm font-medium">Quantity</label>

//           <input
//             value={form.quantity}
//             type="number"
//             min="1"
//             className="w-full border border-gray-300 rounded-xl px-4 py-3"
//             onChange={(e) =>
//               setForm({
//                 ...form,
//                 quantity: e.target.value,
//               })
//             }
//           />
//         </div>

//         {/* Price */}
//         <div>
//           <label className="block mb-2 text-sm font-medium">Total Price</label>

//           <input
//             value={form.Price}
//             readOnly
//             className="w-full border border-gray-300 rounded-xl px-4 py-3 bg-gray-100 font-semibold"
//           />
//         </div>

//         {/* Address */}
//         <div>
//           <label className="block mb-2 text-sm font-medium">Delivery Address</label>

//           <textarea
//             value={form.delivery_address}
//             placeholder="Delivery Address"
//             rows={3}
//             className="w-full border border-gray-300 rounded-xl px-4 py-3 resize-none"
//             onChange={(e) =>
//               setForm({
//                 ...form,
//                 delivery_address: e.target.value,
//               })
//             }
//           />
//         </div>

//         {/* Order Type */}
//         <div>
//           <label className="block mb-2 text-sm font-medium">Order Type</label>

//           <select
//             value={form.order_type}
//             className="w-full border border-gray-300 rounded-xl px-4 py-3"
//             onChange={(e) =>
//               setForm({
//                 ...form,
//                 order_type: e.target.value,
//               })
//             }
//           >
//             <option value="STANDARD">Standard</option>
//             <option value="NON_STANDARD">Non Standard</option>
//           </select>
//         </div>

//         {/* Buttons */}
//         <div className="grid grid-cols-3 gap-3">
//           {/* <button
//             type="button"
//             onClick={resetForm}
//             className="bg-gray-200 text-gray-700 py-3 rounded-xl font-medium"
//           >
//             Refresh
//           </button> */}

//           <button
//             type="button"
//             onClick={resetForm}
//             className="bg-red-500 text-white py-3 rounded-xl font-medium"
//           >
//             Cancel
//           </button>

//           <button type="submit" className="bg-primary text-white py-3 rounded-xl font-medium">
//             Submit
//           </button>
//         </div>
//       </form>

//       {/* Product Popup */}
//       {openProducts && (
//         <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-[999] flex items-center justify-center p-6">
//           <div className="bg-white w-[95vw] max-w-[1400px] h-[85vh] rounded-3xl shadow-2xl overflow-hidden flex flex-col">
//             <div className="flex justify-between items-center mb-5">
//               <h2 className="text-xl font-semibold">Select Product</h2>
//               {openProducts && (
//                 <div className="fixed inset-0 bg-black/40 z-[100] flex items-center justify-center">
//                   <div className="bg-white w-[1000px] rounded-2xl shadow-2xl p-6 max-h-[80vh] overflow-y-auto">
//                     <div className="flex justify-between mb-6">
//                       <h2 className="text-xl font-semibold">Select Product</h2>

//                       <button onClick={() => setOpenProducts(false)}>×</button>
//                     </div>

//                     <ProductCardList
//                       onSelect={(item) => {
//                         setUnitPrice(item.price);

//                         setForm((prev) => ({
//                           ...prev,
//                           product: item.name,
//                           quantity: '1',
//                           Price: String(item.price),
//                         }));

//                         setOpenProducts(false);
//                       }}
//                     />
//                   </div>
//                 </div>
//               )}

//               <button onClick={() => setOpenProducts(false)} className="text-4xl">
//                 ×
//               </button>
//             </div>

//             <div className="grid grid-cols-2 gap-4">
//               {products.map((item) => (
//                 <div
//                   key={item.name}
//                   onClick={() => {
//                     setUnitPrice(item.price);

//                     setForm((prev) => ({
//                       ...prev,
//                       product: item.name,
//                       quantity: '1',
//                       Price: String(item.price),
//                     }));

//                     setOpenProducts(false);
//                   }}
//                 ></div>
//               ))}
//             </div>
//           </div>
//         </div>
//       )}
//     </>
//   );
// }


'use client';

import { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { OrderService } from '@/services/order.service';
import ProductCardList from '@/modules/products/components/ProductCardList';

export default function OrderForm() {
  const searchParams = useSearchParams();
  const [openProducts, setOpenProducts] = useState(false);
  const [unitPrice, setUnitPrice] = useState(0);

  const [form, setForm] = useState({
    account_number: '',
    product: '',
    Price: '',
    quantity: '1',
    delivery_address: '',
    order_type: 'STANDARD',
  });

  // Autofill from URL
  useEffect(() => {
    const product = searchParams.get('product') || '';
    const price = Number(searchParams.get('price')) || 0;

    if (product && price) {
      setUnitPrice(price);

      setForm((prev) => ({
        ...prev,
        product,
        quantity: '1',
        Price: String(price),
      }));
    }
  }, [searchParams]);

  // Calculate total price
  useEffect(() => {
    const qty = Number(form.quantity) || 0;
    const total = qty * unitPrice;

    setForm((prev) => ({
      ...prev,
      Price: total ? String(total) : '',
    }));
  }, [form.quantity, unitPrice]);

  // Reset
  const resetForm = () => {
    setUnitPrice(0);

    setForm({
      account_number: '',
      product: '',
      Price: '',
      quantity: '1',
      delivery_address: '',
      order_type: 'STANDARD',
    });
  };

  // Submit
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (
      !form.account_number ||
      !form.product ||
      !form.quantity ||
      !form.Price ||
      !form.delivery_address
    ) {
      alert('Please fill all fields');
      return;
    }

    await OrderService.create({
      ...form,
      quantity: Number(form.quantity),
      price: Number(form.Price),
    });

    alert('Order created successfully');
    resetForm();
  };

  return (
    <>
      <form onSubmit={handleSubmit} className="space-y-5">
        {/* Account Number */}
        <div>
          <label className="block mb-2 text-sm font-medium">
            Account Number
          </label>

          <input
            value={form.account_number}
            placeholder="Account Number"
            className="w-full border border-gray-300 rounded-xl px-4 py-3 outline-none focus:ring-2 focus:ring-primary"
            onChange={(e) =>
              setForm({
                ...form,
                account_number: e.target.value,
              })
            }
          />
        </div>

        {/* Product */}
        <div>
          <label className="block mb-2 text-sm font-medium">
            Product
          </label>

          <div
            onClick={() => setOpenProducts(true)}
            className="w-full border border-gray-300 rounded-xl px-4 py-3 cursor-pointer bg-white hover:border-primary transition"
          >
            {form.product || 'Select Product'}
          </div>
        </div>

        {/* Quantity */}
        <div>
          <label className="block mb-2 text-sm font-medium">
            Quantity
          </label>

          <input
            value={form.quantity}
            type="number"
            min="1"
            className="w-full border border-gray-300 rounded-xl px-4 py-3 outline-none focus:ring-2 focus:ring-primary"
            onChange={(e) =>
              setForm({
                ...form,
                quantity: e.target.value,
              })
            }
          />
        </div>

        {/* Total Price */}
        <div>
          <label className="block mb-2 text-sm font-medium">
            Total Price
          </label>

          <input
            value={form.Price}
            readOnly
            className="w-full border border-gray-300 rounded-xl px-4 py-3 bg-gray-100 font-semibold"
          />
        </div>

        {/* Delivery Address */}
        <div>
          <label className="block mb-2 text-sm font-medium">
            Delivery Address
          </label>

          <textarea
            value={form.delivery_address}
            placeholder="Delivery Address"
            rows={3}
            className="w-full border border-gray-300 rounded-xl px-4 py-3 resize-none outline-none focus:ring-2 focus:ring-primary"
            onChange={(e) =>
              setForm({
                ...form,
                delivery_address: e.target.value,
              })
            }
          />
        </div>

        {/* Order Type */}
        <div>
          <label className="block mb-2 text-sm font-medium">
            Order Type
          </label>

          <select
            value={form.order_type}
            className="w-full border border-gray-300 rounded-xl px-4 py-3 outline-none focus:ring-2 focus:ring-primary"
            onChange={(e) =>
              setForm({
                ...form,
                order_type: e.target.value,
              })
            }
          >
            <option value="STANDARD">Standard</option>
            <option value="NON_STANDARD">Non Standard</option>
          </select>
        </div>

        {/* Buttons */}
        <div className="grid grid-cols-2 gap-3">
          <button
            type="button"
            onClick={resetForm}
            className="bg-red-500 hover:bg-red-600 text-white py-3 rounded-xl font-medium transition"
          >
            Cancel
          </button>

          <button
            type="submit"
            className="bg-primary hover:opacity-90 text-white py-3 rounded-xl font-medium transition"
          >
            Submit Order
          </button>
        </div>
      </form>

      {/* Product Modal */}
      {openProducts && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-[999] flex items-center justify-center p-6">
          <div className="bg-white w-[95vw] max-w-[1400px] h-[85vh] rounded-3xl shadow-2xl overflow-hidden flex flex-col">
            {/* Header */}
            <div className="flex justify-between items-center px-8 py-6 border-b bg-white">
              <h2 className="text-2xl font-bold text-slate-900">
                Select Product
              </h2>

              <button
                onClick={() => setOpenProducts(false)}
                className="text-4xl text-gray-500 hover:text-black"
              >
                ×
              </button>
            </div>

            {/* Body */}
            <div className="flex-1 overflow-y-auto p-8 bg-slate-50">
              <ProductCardList
                onSelect={(item) => {
                  setUnitPrice(item.price);

                  setForm((prev) => ({
                    ...prev,
                    product: item.name,
                    quantity: '1',
                    Price: String(item.price),
                  }));

                  setOpenProducts(false);
                }}
              />
            </div>
          </div>
        </div>
      )}
    </>
  );
}
