// 'use client';

// import { useEffect, useState } from 'react';
// import { Bell, Search, ChevronDown } from 'lucide-react';
// import { usePathname, useRouter } from 'next/navigation';
// import { apiFetch } from '@/lib/api';

// export default function Header() {
//   const pathname = usePathname();
//   const router = useRouter();

//   const [open, setOpen] = useState(false);
//   const [tenantOpen, setTenantOpen] = useState(false);

//   const showSearch = pathname === '/dashboard';
//   const tenants =
//     typeof window !== 'undefined' ? JSON.parse(localStorage.getItem('tenants') || '[]') : [];

//   const activeTenant =
//     typeof window !== 'undefined'
//       ? JSON.parse(localStorage.getItem('activeTenant') || 'null')
//       : null;

//   const displayName = typeof window !== 'undefined' ? localStorage.getItem('display_name') : '';

//   const tenantName =
//     tenants.find((t: any) => t.tenantid === activeTenant?.tenantid)?.tenant_name || '';

//   const switchTenant = async (tenantid: string) => {
//     try {
//       const data = await apiFetch('/auth/switch-tenant', {
//         method: 'POST',
//         body: JSON.stringify({
//           tenantid,
//         }),
//       });

//       localStorage.setItem('token', data.access_token);

//       localStorage.setItem('role', data.role);

//       localStorage.setItem('tenantid', data.tenantid);

//       localStorage.setItem(
//         'activeTenant',
//         JSON.stringify({
//           tenantid: data.tenantid,
//           role: data.role,
//         })
//       );

//       setTenantOpen(false);
//       setOpen(false);

//       router.refresh();
//     } catch (error) {
//       console.error(error);
//     } 
//   };
//  // const displayName = typeof window !== 'undefined' ? localStorage.getItem('display_name') : '';

//   const handleLogout = () => {
//     localStorage.clear();
//     router.push('/');
//   };

//   return (
//     <header className="h-20 bg-white border-b px-8 flex items-center justify-between relative z-50">
//       {/* Left */}
//       <div className="flex items-center">
//         {showSearch && (
//           <div className="relative w-[420px]">
//             <Search size={18} className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" />

//             <input
//               type="text"
//               placeholder="Search..."
//               className="w-full pl-11 pr-4 py-3 border rounded-2xl outline-none focus:ring-2 focus:ring-primary"
//             />
//           </div>
//         )}
//       </div>

//       {/* Right */}
//       <div className="flex items-center gap-6">
//         {/* Bell */}
//         <div className="relative cursor-pointer">
//           <Bell size={22} className="text-gray-600" />

//           <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-red-500 rounded-full animate-pulse" />
//         </div>

//         {/* Profile */}
//         <div className="relative">
//           <div onClick={() => setOpen(!open)} className="flex items-center gap-3 cursor-pointer">
//             {displayName
//               ? displayName
//                   .split(' ')
//                   .map((n) => n[0])
//                   .join('')
//                   .slice(0, 2)
//                   .toUpperCase()
//               : ''}

//             <div className="leading-tight">
//               <p className="font-medium text-gray-900">{displayName || 'User'}</p>
//               <p className="text-sm text-gray-500">
//                 {tenants.find((t: any) => t.tenantid === activeTenant?.tenantid)?.tenant_name ||
//                   'No Tenant'}
//               </p>
//             </div>

//             <ChevronDown size={18} className={`transition ${open ? 'rotate-180' : ''}`} />
//           </div>

//           {/* Dropdown */}

//           {/* profile dropdown  */}
//           {open && (
//             <div className="absolute right-0 mt-4 w-60 bg-white rounded-2xl border shadow-xl overflow-hidden">
//               <button
//                 onClick={() => {
//                   setOpen(false);
//                   router.push('/profile');
//                 }}
//                 className="w-full text-left px-5 py-4 hover:bg-gray-50"
//               >
//                 My Profile
//               </button>

//               <button
//                 onClick={() => setTenantOpen(!tenantOpen)}
//                 className="w-full flex items-center justify-between px-5 py-4 hover:bg-gray-50"
//               >
//                 <span>Switch Tenant</span>

//                 <ChevronDown size={16} className={`transition ${tenantOpen ? 'rotate-180' : ''}`} />
//               </button>

//               {tenantOpen && (
//                 <div className="border-t bg-gray-50">
//                   {tenants.map((tenant: any) => (
//                     <button
//                       key={tenant.tenantid}
//                       onClick={() => switchTenant(tenant.tenantid)}
//                       className={`w-full text-left px-8 py-3 hover:bg-white ${
//                         activeTenant?.tenantid === tenant.tenantid
//                           ? 'font-semibold text-primary'
//                           : ''
//                       }`}
//                     >
//                       {tenant.tenant_name} ({tenant.role})
//                     </button>
//                   ))}
//                 </div>
//               )}

//               {/* admin cann be added here to register new users, but for now we are skipping this part */}

//               {/* <button
//                 onClick={() => {
//                   setOpen(false);
//                   router.push(
//                     "/users/register"
//                   );
//                 }}
//                 className="w-full text-left px-5 py-4 hover:bg-gray-50"
//               >
//                 Register User
//               </button> */}

//               <button
//                 onClick={handleLogout}
//                 className="w-full text-left px-5 py-4 hover:bg-red-50 text-red-500 border-t"
//               >
//                 Logout
//               </button>
//             </div>
//           )}
//         </div>
//       </div>
//     </header>
//   );
// }


'use client';

import { useEffect, useState } from 'react';
import { Bell, Search, ChevronDown } from 'lucide-react';
import { usePathname, useRouter } from 'next/navigation';
import { apiFetch } from '@/lib/api';

export default function Header() {
  const pathname = usePathname();
  const router = useRouter();

  const [open, setOpen] =
    useState(false);

  const [tenantOpen, setTenantOpen] =
    useState(false);

  const [tenants, setTenants] =
    useState<any[]>([]);

  const [activeTenant, setActiveTenant] =
    useState<any>(null);

  const [displayName, setDisplayName] =
    useState('');

  const showSearch =
    pathname === '/dashboard';

  useEffect(() => {
    const storedTenants =
      JSON.parse(
        localStorage.getItem(
          'tenants'
        ) || '[]'
      );

    const storedActiveTenant =
      JSON.parse(
        localStorage.getItem(
          'activeTenant'
        ) || 'null'
      );

    const storedDisplayName =
      localStorage.getItem(
        'display_name'
      ) || '';

    setTenants(storedTenants);

    setActiveTenant(
      storedActiveTenant
    );

    setDisplayName(
      storedDisplayName
    );
  }, []);

  const tenantName =
    tenants.find(
      (t: any) =>
        t.tenantid ===
        activeTenant?.tenantid
    )?.tenant_name || '';

  const switchTenant = async (
    tenantid: string
  ) => {
    try {
      const data =
        await apiFetch(
          '/auth/switch-tenant',
          {
            method: 'POST',
            body: JSON.stringify({
              tenantid,
            }),
          }
        );

      localStorage.setItem(
        'token',
        data.access_token
      );

      localStorage.setItem(
        'role',
        data.role
      );

      localStorage.setItem(
        'tenantid',
        data.tenantid
      );

      localStorage.setItem(
        'activeTenant',
        JSON.stringify({
          tenantid: data.tenantid,
          role: data.role,
        })
      );

      setActiveTenant({
        tenantid: data.tenantid,
        role: data.role,
      });

      setTenantOpen(false);
      setOpen(false);

      router.refresh();
    } catch (error) {
      console.error(error);
    }
  };

  const handleLogout = () => {
    localStorage.clear();
    router.push('/');
  };

  return (
    <header className="h-20 bg-white border-b px-8 flex items-center justify-between relative z-50">
      {/* Left */}
      <div className="flex items-center">
        {showSearch && (
          <div className="relative w-[420px]">
            <Search
              size={18}
              className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"
            />

            <input
              type="text"
              placeholder="Search..."
              className="w-full pl-11 pr-4 py-3 border rounded-2xl outline-none focus:ring-2 focus:ring-primary"
            />
          </div>
        )}
      </div>

      {/* Right */}
      <div className="flex items-center gap-6">
        {/* Bell */}
        <div className="relative cursor-pointer">
          <Bell
            size={22}
            className="text-gray-600"
          />

          <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-red-500 rounded-full animate-pulse" />
        </div>

        {/* Profile */}
        <div className="relative">
          <div
            onClick={() =>
              setOpen(!open)
            }
            className="flex items-center gap-3 cursor-pointer"
          >
            {/* Avatar */}
            <div className="w-12 h-12 rounded-full bg-primary text-white flex items-center justify-center font-semibold text-lg">
              {displayName
                ? displayName
                    .split(' ')
                    .map(
                      (n) => n[0]
                    )
                    .join('')
                    .slice(0, 2)
                    .toUpperCase()
                : 'U'}
            </div>

            {/* Name + Tenant */}
            <div className="leading-tight">
              <p className="font-medium text-gray-900">
                {displayName ||
                  'User'}
              </p>

              <p className="text-sm text-gray-500">
                {tenantName ||
                  'No Tenant'}
              </p>
            </div>

            <ChevronDown
              size={18}
              className={`transition ${
                open
                  ? 'rotate-180'
                  : ''
              }`}
            />
          </div>

          {/* Dropdown */}
          {open && (
            <div className="absolute right-0 mt-4 w-72 bg-white rounded-2xl border shadow-xl overflow-hidden">
              <button
                onClick={() => {
                  setOpen(false);
                  router.push(
                    '/profile'
                  );
                }}
                className="w-full text-left px-5 py-4 hover:bg-gray-50"
              >
                My Profile
              </button>

              {/* Tenant Switch */}
              <button
                onClick={() =>
                  setTenantOpen(
                    !tenantOpen
                  )
                }
                className="w-full flex items-center justify-between px-5 py-4 hover:bg-gray-50 border-t"
              >
                <span>
                  Switch Tenant
                </span>

                <ChevronDown
                  size={16}
                  className={`transition ${
                    tenantOpen
                      ? 'rotate-180'
                      : ''
                  }`}
                />
              </button>

              {tenantOpen && (
                <div className="border-t bg-gray-50">
                  {tenants.map(
                    (
                      tenant: any
                    ) => (
                      <button
                        key={
                          tenant.tenantid
                        }
                        onClick={() =>
                          switchTenant(
                            tenant.tenantid
                          )
                        }
                        className={`w-full text-left px-8 py-3 hover:bg-white ${
                          activeTenant?.tenantid ===
                          tenant.tenantid
                            ? 'font-semibold text-primary'
                            : ''
                        }`}
                      >
                        {
                          tenant.tenant_name
                        }{' '}
                        (
                        {tenant.role}
                        )
                      </button>
                    )
                  )}
                </div>
              )}

              {/* Logout */}
              <button
                onClick={
                  handleLogout
                }
                className="w-full text-left px-5 py-4 hover:bg-red-50 text-red-500 border-t"
              >
                Logout
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}