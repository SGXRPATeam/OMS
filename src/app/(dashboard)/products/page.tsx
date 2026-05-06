// 'use client';
// import { useRouter } from 'next/navigation';

// const products = [
//   {
//     id: 1,
//     name: 'Portable ECG Machine',
//     category: 'Diagnostic',
//     description: 'Compact ECG machine with high resolution display and accurate readings.',
//     price: 45000,
//     oldPrice: 60000,
//     rating: 4.6,
//     reviews: 128,
//     discount: '25% OFF',
//     image: 'https://images.unsplash.com/photo-1581595219315-a187dd40c322?w=800',
//   },
//   {
//     id: 2,
//     name: 'Patient Monitor',
//     category: 'Monitoring',
//     description: 'Advanced patient monitor for real-time vital signs monitoring.',
//     price: 85000,
//     oldPrice: 105000,
//     rating: 4.7,
//     reviews: 156,
//     discount: '19% OFF',
//     image: 'https://images.unsplash.com/photo-1579154204601-01588f351e67?w=800',
//   },
//   {
//     id: 3,
//     name: 'Pulse Oximeter',
//     category: 'Monitoring',
//     description: 'Accurate SpO2 and pulse rate monitoring in a compact design.',
//     price: 2499,
//     oldPrice: 3200,
//     rating: 4.5,
//     reviews: 98,
//     discount: '22% OFF',
//     image: 'https://images.unsplash.com/photo-1584515933487-779824d29309?w=800',
//   },
//   {
//     id: 4,
//     name: 'Nebulizer',
//     category: 'Respiratory',
//     description: 'Efficient nebulizer for effective respiratory therapy.',
//     price: 1999,
//     oldPrice: 2800,
//     rating: 4.4,
//     reviews: 87,
//     discount: '29% OFF',
//     image: 'https://images.unsplash.com/photo-1603398938378-e54eab446dde?w=800',
//   },
//   {
//     id: 5,
//     name: 'Infusion Pump',
//     category: 'ICU Equipment',
//     description: 'Reliable infusion pump for precise fluid delivery.',
//     price: 32000,
//     oldPrice: 40000,
//     rating: 4.6,
//     reviews: 73,
//     discount: '20% OFF',
//     image: 'https://images.unsplash.com/photo-1580281657527-47d1d8f8dbe3?w=800',
//   },
//   {
//     id: 6,
//     name: 'Defibrillator',
//     category: 'Emergency Care',
//     description: 'Advanced defibrillator for emergency cardiac care.',
//     price: 125000,
//     oldPrice: 160000,
//     rating: 4.8,
//     reviews: 112,
//     discount: '22% OFF',
//     image: 'https://images.unsplash.com/photo-1586773860418-d37222d8fce3?w=800',
//   },
//   {
//     id: 7,
//     name: 'Ventilator',
//     category: 'Critical Care',
//     description: 'High performance ventilator for critical care and ICU.',
//     price: 250000,
//     oldPrice: 320000,
//     rating: 4.7,
//     reviews: 63,
//     discount: '22% OFF',
//     image: 'https://images.unsplash.com/photo-1587351021759-3e566b6af7cc?w=800',
//   },
//   {
//     id: 8,
//     name: 'Wheelchair',
//     category: 'Mobility',
//     description: 'Durable and comfortable wheelchair for mobility support.',
//     price: 8499,
//     oldPrice: 10999,
//     rating: 4.3,
//     reviews: 54,
//     discount: '23% OFF',
//     image: 'https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?w=800',
//   },
// ];

// export default function MedicalProductsPage() {
//   const router = useRouter();
//   return (
//     <div className="min-h-screen bg-slate-50 px-6 py-10">
//       {/* Header */}
//       <div className="max-w-7xl mx-auto mb-10">
//         <h1 className="text-5xl font-bold text-slate-900">Medical Devices</h1>
//         <p className="text-slate-500 mt-3 text-lg">Browse premium healthcare equipment</p>

//         {/* Features */}
//         <div className="flex flex-wrap gap-8 mt-6 text-sm font-medium text-slate-700">
//           <span>🛡 100% Certified</span>
//           <span>🚚 Fast Delivery</span>
//           <span>✅ 1 Year Warranty</span>
//         </div>
//       </div>

//       {/* Grid */}
//       <div className="max-w-7xl mx-auto grid gap-8 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
//         {products.map((product) => (
//           <div
//             key={product.id}
//             className="bg-white rounded-3xl border border-slate-200 shadow-sm hover:shadow-xl transition duration-300 overflow-hidden group"
//           >
//             {/* Image */}
//             <div className="h-64 bg-white p-6">
//               <img
//                 src={product.image}
//                 alt={product.name}
//                 className="w-full h-full object-contain group-hover:scale-105 transition duration-500"
//               />
//             </div>

//             {/* Content */}
//             <div className="p-5">
//               {/* Category */}
//               <span className="inline-block px-3 py-1 rounded-full text-xs font-semibold bg-blue-100 text-blue-700">
//                 {product.category}
//               </span>

//               {/* Title */}
//               <h2 className="mt-3 text-xl font-bold text-slate-900">{product.name}</h2>

//               {/* Description */}
//               <p className="mt-2 text-sm text-slate-500 leading-6">{product.description}</p>

//               {/* Rating */}
//               <div className="mt-3 flex items-center gap-2 text-sm">
//                 <span className="text-yellow-500">★</span>
//                 <span className="font-semibold text-slate-700">{product.rating}</span>
//                 <span className="text-slate-400">({product.reviews})</span>
//               </div>

//               {/* Price */}
//               <div className="mt-4 flex items-center gap-3 flex-wrap">
//                 <span className="text-2xl font-bold text-blue-600">
//                   ₹{product.price.toLocaleString()}
//                 </span>

//                 <span className="text-sm line-through text-slate-400">
//                   ₹{product.oldPrice.toLocaleString()}
//                 </span>

//                 <span className="bg-green-100 text-green-700 px-2 py-1 rounded-full text-xs font-semibold">
//                   {product.discount}
//                 </span>
//               </div>

//               {/* Button */}
//               <button
//                 onClick={() =>
//                   router.push(
//                     `/orders?product=${encodeURIComponent(product.name)}&price=${product.price}`
//                   )
//                 }
//                 className="mt-5 w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-xl font-semibold transition"
//               >
//                 Order Device
//               </button>
//             </div>
//           </div>
//         ))}
//       </div>
//     </div>
//   );
// }


'use client';

import { useRouter } from 'next/navigation';
import ProductCardList from '@/modules/products/components/ProductCardList';

export default function MedicalProductsPage() {
  const router = useRouter();

  return (
    <div className="min-h-screen bg-slate-50 px-6 py-10">
      <div className="max-w-7xl mx-auto mb-10">
        <h1 className="text-5xl font-bold text-slate-900">
          Medical Devices
        </h1>
      </div>

      <div className="max-w-7xl mx-auto">
        <ProductCardList
          onSelect={(product) =>
            router.push(
              `/orders?product=${encodeURIComponent(product.name)}&price=${product.price}`
            )
          }
        />
      </div>
    </div>
  );
}